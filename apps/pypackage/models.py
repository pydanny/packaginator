# TODO - cleanup regex to do proper string subs

import logging
import os
import re
import sys
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from distutils.version import LooseVersion as versioner

from core.fields import CreationDateTimeField, ModificationDateTimeField
from package.models import Package
from pypackage.pypi import fetch_releases

pypi_url_help_text = settings.PACKAGINATOR_HELP_TEXT['PYPI_URL']

class NoPyPiVersionFound(Exception):
    pass

class BaseModel(models.Model):
    """ Base abstract base class to give creation and modified times """
    created     = CreationDateTimeField(_('created'))
    modified    = ModificationDateTimeField(_('modified'))
    
    class Meta:
        abstract = True
        
class PyPackage(BaseModel):
    
    package = models.OneToOneField(Package, related_name='package')    
    pypi_url        = models.URLField(_("PyPI url for project"), help_text=pypi_url_help_text, blank=True, default='')
    pypi_slug        = models.SlugField(_("PyPI slug project"), help_text=_("pypi slug"), blank=True, default='')
    pypi_downloads  = models.IntegerField(_("Pypi downloads"), default=0)
    pypi_owner_email  = models.EmailField(_("PyPI Owner Email"), default=0)    
    
    @property
    def pypi_version(self):
        string_ver_list = self.version_set.values_list('number', flat=True)
        if string_ver_list:
            vers_list = [versioner(v) for v in string_ver_list]
            latest = sorted(vers_list)[-1]
            return str(latest)
        return ''

    @property     
    def pypi_name(self):
        """ return the pypi name of a package"""
        
        if not self.pypi_url.strip():
            return ""
            
        name = self.pypi_url.replace("http://pypi.python.org/pypi/","")
        if "/" in name:
            return name[:name.index("/")]
        return name

    @property
    def last_updated(self):
        try:
            last_commit = self.commit_set.latest('commit_date')
            if last_commit: 
                return last_commit.commit_date
        except ObjectDoesNotExist:
            pass

        return None
    
    def fetch_metadata(self, *args, **kwargs):
        
        # Get the downloads from pypi
        if self.pypi_url.strip() and self.pypi_url != "http://pypi.python.org/pypi/":
            
            total_downloads = 0
            
            for release in fetch_releases(self.pypi_name):
            
                version, created = Version.objects.get_or_create(
                    package = self,
                    number = release.version
                )

                # add to total downloads
                total_downloads += release.downloads

                # add to versions
                version.downloads = release.downloads
                version.license = release.license
                version.hidden = release._pypi_hidden                
                version.save()
            
            self.pypi_downloads = total_downloads
        
        self.repo.fetch_metadata(self)
        self.save()
        
    def save(self, *args, **kwargs):
        self.pypi_slug = self.pypi_name
        super(PyPackage, self).save(*args, **kwargs)        

    class Meta:
        ordering = ['pypi_slug']
    
    def __unicode__(self):
        
        return self.pypi_slug
        
    #@models.permalink
    #def get_absolute_url(self):
    #    return ("pypi_detau", [self.slug])
        
class VersionManager(models.Manager):
    def by_version(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return sorted(qs,key=lambda v: versioner(v.number))

class Version(BaseModel):
    
    pypackage = models.ForeignKey(PyPackage, blank=True, null=True)
    number = models.CharField(_("Version"), max_length="100", default="", blank="")
    downloads = models.IntegerField(_("downloads"), default=0)
    license = models.CharField(_("license"), max_length="100")
    hidden = models.BooleanField(_("hidden"), default=False)    
    
    objects = VersionManager()

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if len(self.license) > 20:
            self.license = "Custom"
        super(Version, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s: %s" % (self.package.title, self.number)
    
