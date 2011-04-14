from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.date_based import archive_index
from django.views.generic.simple import direct_to_template



urlpatterns = patterns("",

    (
        r"^$",
        direct_to_template,
        {"template_name":"package/package_list.html"},
        "pypackages",
    ),
)