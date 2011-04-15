from django.test import TestCase

from package.models import Package
from pypackage.models import PyPackage, Version, versioner
from pypackage.tests import mock

class VersionTests(TestCase):
    
    def setUp(self):
        
        mock.make()

    #fixtures = ['versioner_test_fixture.json',
    #            'versioner_versions_fixture.json']

    def test_version_order(self):
        
        package = Package.objects.get(slug='django-cms')
        versions = package.pypackage.version_set.by_version()
        expected_values = [ u'2.0.0', 
                            u'2.1.0', 
                            u'2.1.0.rc1', 
                            u'2.1.0.rc2', 
                            u'2.1.0.rc3', 
                            u'2.1.1', 
                            u'2.1.2', 
                            u'2.1.3']
        returned_values = [v.number for v in versions]
        self.assertEquals(returned_values,expected_values)

    def test_version_license_length(self):
        v = Version.objects.all()[0]
        v.license = "x"*50
        v.save()
        self.assertEquals(v.license,"Custom")