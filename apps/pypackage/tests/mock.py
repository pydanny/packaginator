from core.test_utils.mock import make as core_make

from package.models import Category, Package
from pypackage.models import PyPackage, Version

def make():
    
    core_make()
    
    category = Category.objects.all()[0]
    package, created = Package.objects.get_or_create(
        category = category,
        participants = "chrisglass,digi604,erobit,fivethreeo,ojii,stefanfoulis,pcicman,DrMeers,brightwhitefox,FlashJunior,philomat,jezdez,havan,acdha,m000,hedberg,piquadrat,spookylukey,izimobil,ulope,emiquelito,aaloy,lasarux,yohanboniface,aparo,jsma,johbo,ionelmc,quattromic,almost,specialunderwear,mitar,yml,pajusmar,diofeher,marcor,cortextual,hysia,dstufft,ssteinerx,oversize,jalaziz,tercerojista,eallik,f4nt,kaapa,mbrochh,srj55,dz,mathijs-dumon,sealibora,cyberj,adsworth,tokibito,DaNmarner,IanLewis,indexofire,bneijt,tehfink,PPvG,seyhunak,pigletto,fcurella,gleb-chipiga,beshrkayali,kinea,lucasvo,jordanjambazov,tonnzor,centralniak,arthur-debert,bzed,jasondavies,nimnull,limpbrains,pvanderlinden,sleytr,sublimevelo,netpastor,dtt101,fkazimierczak,merlex,mrlundis,restless,eged,shanx,ptoal",
        repo_description = "An Advanced Django CMS.",
        repo_url = "https://github.com/divio/django-cms",
        pypi_url = "http://pypi.python.org/pypi/django-cms",
        slug = "django-cms",
        title="Django CMS"
    )
    package.save()
    pypackage, created = PyPackage.objects.get_or_create(
        package = package,
        pypi_url = "http://pypi.python.org/pypi/django-cms",        
    )
    pypackage.save()
    
    
    versions = ["2.0.0", "2.1.0.rc2","2.1.0", "2.1.3", "2.1.2", "2.1.1", "2.1.0.rc3", "2.1.0.rc1"]
    downloads = ["1062",726, 1613, 1904, 715, 906, 850, 299]
    for version, download in zip(versions, downloads):
        version, created = Version.objects.get_or_create(
            pypackage = pypackage,
            license="BSD",
            number=version,
            downloads=download
        )
        version.save()
