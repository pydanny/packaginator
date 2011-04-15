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

from core.models import BaseModel, FetchModel
from package.repos import github
from pypackage.pypi import fetch_releases
from package.repos import get_repo_for_repo_url
from package.signals import signal_fetch_latest_metadata

repo_url_help_text = settings.PACKAGINATOR_HELP_TEXT['REPO_URL']
pypi_url_help_text = settings.PACKAGINATOR_HELP_TEXT['PYPI_URL']
category_help_text = settings.PACKAGINATOR_HELP_TEXT['CATEGORY']



class Category(BaseModel):
    
    title = models.CharField(_("Title"), max_length="50")
    slug  = models.SlugField(_("slug"))
    description = models.TextField(_("description"), blank=True)
    title_plural = models.CharField(_("Title Plural"), max_length="50", blank=True) 
    show_pypi = models.BooleanField(_("Show pypi stats & version"), default=True)
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.title
        
class Package(BaseModel):
    
    title           = models.CharField(_("Title"), max_length="100")
    slug            = models.SlugField(_("Slug"), help_text="Slugs will be lowercased", unique=True)
    category        = models.ForeignKey(Category, verbose_name="Installation", help_text=category_help_text)
    repo_description= models.TextField(_("Repo Description"), blank=True)
    repo_url        = models.URLField(_("repo URL"), help_text=repo_url_help_text, blank=True,unique=True)
    repo_watchers   = models.IntegerField(_("repo watchers"), default=0)
    repo_forks      = models.IntegerField(_("repo forks"), default=0)
    repo_commits    = models.IntegerField(_("repo commits"), default=0)
    pypi_url        = models.URLField(_("PyPI slug"), help_text=pypi_url_help_text, blank=True, default='')
    related_packages    = models.ManyToManyField("self", blank=True)
    participants    = models.TextField(_("Participants"),
                        help_text="List of collaborats/participants on the project", blank=True)
    usage           = models.ManyToManyField(User, blank=True)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name="creator")    
    last_modified_by = models.ForeignKey(User, blank=True, null=True, related_name="modifier")

    @property
    def last_updated(self):
        try:
            last_commit = self.commit_set.latest('commit_date')
            if last_commit: 
                return last_commit.commit_date
        except ObjectDoesNotExist:
            pass

        return None

    @property
    def repo(self):
        handler = get_repo_for_repo_url(self.repo_url)
        return handler

    def active_examples(self):
        return self.packageexample_set.filter(active=True)
    
    def grids(self):
        
        return (x.grid for x in self.gridpackage_set.all())
    
    def repo_name(self):
        return re.sub(self.repo.url_regex, '', self.repo_url)
    
    def participant_list(self):
        
        return self.participants.split(',')
    
    def get_usage_count(self):
        return self.usage.count()
    
    def commits_over_52(self):
        now = datetime.now()
        commits = Commit.objects.filter(
            package=self,
            commit_date__gt=now - timedelta(weeks=52),
        ).values_list('commit_date', flat=True)

        weeks = [0] * 52
        for cdate in commits:
            age_weeks = (now - cdate).days // 7
            if age_weeks < 52:
                weeks[age_weeks] += 1

        return ','.join(map(str,reversed(weeks)))
    
    def fetch_metadata(self, *args, **kwargs):
        
        # run fetch() method on any FetchModels attached to this.
        # FetchModels should be things defined in settings.PACKAGE_EXTENDERS
        # TODO - this is dirt slow. Need to figure out how to speed it up
        for obj_name in dir(self):
            obj = getattr(self, obj_name, None)
            if isinstance(obj, FetchModel):
                obj.fetch_metadata()
        
        self.repo.fetch_metadata(self)
        signal_fetch_latest_metadata.send(sender=self)
        self.save()        

    class Meta:
        ordering = ['title']
    
    def __unicode__(self):
        
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ("package", [self.slug])
        

class PackageExample(BaseModel):
    
    package = models.ForeignKey(Package)
    title = models.CharField(_("Title"), max_length="100")
    url = models.URLField(_("URL"))
    active = models.BooleanField(_("Active"), default=True, help_text="Moderators have to approve links before they are provided")
    
    class Meta:
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class Commit(BaseModel):
    
    package      = models.ForeignKey(Package)
    commit_date  = models.DateTimeField(_("Commit Date"))
    
    class Meta:
        ordering = ['-commit_date']
        
    def __unicode__(self):
        return "Commit for '%s' on %s" % (self.package.title, unicode(self.commit_date))