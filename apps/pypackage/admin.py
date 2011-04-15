from django.contrib import admin

from pypackage.models import PyPackage, Version

admin.site.register(PyPackage)
admin.site.register(Version)