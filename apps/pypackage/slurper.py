#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyPI interface (see http://wiki.python.org/moin/PyPiXmlRpc)
"""

from datetime import datetime
import itertools
import re
import sys
from xml.parsers.expat import ExpatError
import xmlrpclib

from django.conf import settings
from django.template.defaultfilters import slugify

from package.models import Category, Package
from package.repos import get_repo_for_repo_url
from pypackage.models import PyPackage, Version
from pypackage.versioning import highest_version

base_url = "http://pypi.python.org/pypi/"
PYPI = xmlrpclib.Server(base_url)

class Slurper(object):
    
    def __init__(self, package_name):
        self.package_name = package_name
        self.dumb_category, created = Category.objects.get_or_create(
                                title='Python', slug='python')
        self.dumb_category.save()
        
    def get_latest_version_number(self, package_name, versions=None):
        if versions:
            return highest_version(versions)
        else:
            try:
                releases = PYPI.package_releases(package_name)
            except ExpatError as e:
                if settings.DEBUG:
                    # TODO - convert to log
                    print >> sys.stderr, "Threw an EXPAT error on getting version for '%s'" % package_name
                return ""
            return highest_version(releases)
        
    def get_or_create_package(self, package_name, version):
        data = PYPI.release_data(package_name, version)
        pypi_url = base_url + package_name
        package, created = Package.objects.get_or_create(
            title           = data['name'],
            slug            = slugify(package_name),
            category        = self.dumb_category,
            pypi_url        = base_url + data['name']
        )
        package.repo_description = data['summary'] or data['description']
        
        # Now add the package in
        pypackage, created = PyPackage.objects.get_or_create(
            package=package,
            pypi_url=base_url + data['name']
        )
        pypackage.save()
        """
        # TODO - How should this be broken out?
        # TODO -    Its both PyPackage and RepoPackage item
        if not package.repo_url:
            url = data.get("home_page", None) or data.get('project_url',"") or pypi_url
            repo_pattern = '((?:http|https|git)://github.com/[^/]*/[^/]*)/{0,1}'
            match = re.match(repo_pattern, url)
            if match and match.group(1):
                package.repo_url = match.group(1)
            else:
                # TODO do we want to assume this is a repo url?
                # should there be more checking for repo patterns?
                package.repo_url = url
        """
        package.save()
        package.fetch_metadata()
        return (package, created)