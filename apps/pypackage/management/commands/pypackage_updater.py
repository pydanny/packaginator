from socket import error as socket_error
from sys import stdout
from time import sleep, gmtime, strftime
from xml.parsers.expat import ExpatError
from xmlrpclib import ProtocolError

from django.conf import settings
from django.core.management.base import CommandError, NoArgsCommand

from pypackage.models import PyPackage

class Command(NoArgsCommand):
    
    help = "Updates all the pypackages in the system by fetching info off of PyPI"    
    
    def handle(self, *args, **options):
        
        print >> stdout, "Commencing pypackage updating now at %s " % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        
        for index, pypackage in enumerate(PyPackage.objects.all()):
            try:
                try:
                    pypackage.fetch_metadata()
                except socket_error, e:
                    print >> stdout, "For '%s', threw a socket.error: %s" % (package, e)
                    continue
            except RuntimeError, e:
                message = "For '%s', too many requests issued to repo threw a RuntimeError: %s" % (package, e)
                print >> stdout, message
                continue
            except UnicodeDecodeError, e:
                message = "For '%s', UnicodeDecodeError: %s" % (package, e)
                print >> stdout, message
                continue
            except ProtocolError, e:
                message = "For '%s', xmlrpc.ProtocolError: %s" % (package, e)
                print >> stdout, message
                continue
            except ExpatError, e:
                message = "For '%s', ExpatError: %s" % (package, e)
                print >> stdout, message
                continue                
                

        print >> stdout, "-" * 40
        print >> stdout, "Finished at %s" % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
