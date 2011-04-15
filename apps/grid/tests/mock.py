from core.test_utils.mock import make as core_make

from grid.models import Feature, Grid, GridPackage
from package.models import Package

def make():
    
    core_make()
    
    #-------------grids
    grid1, created = Grid.objects.get_or_create(
        slug='testing',
        title='Testing',
        description='A grid for testing.'
    )
    grid1.save()

    grid2, created = Grid.objects.get_or_create(
        slug='another-testing',
        title='Another Testing',
        description='Another grid for testing.'
    )
    grid2.save()
    
    
    #-------------grid packages
    package1 = Package.objects.all()[0]
    package2 = Package.objects.all()[1]
    package3 = Package.objects.all()[2]        
        
    gp, created = GridPackage.objects.get_or_create(
        grid=grid1,
        package=package1,        
    )
    gp.save()

    gp, created = GridPackage.objects.get_or_create(
        grid=grid1,
        package=package3,
    )
    gp.save()

    gp, created = GridPackage.objects.get_or_create(
        grid=grid1,
        package=package3, 
    )
    gp.save()

    gp, created = GridPackage.objects.get_or_create(
        grid=grid1,
        package=package2,
    )
    gp.save()

    gp, created = GridPackage.objects.get_or_create(
        grid=grid2,
        package=package3,
    )
    gp.save()
    
    #------------------features
    
    feature, created = Feature.objects.get_or_create(
        title = "Has tests?",
        description = "Does this package come with tests?",
        grid = grid1
    )
    feature.save()
    feature, created = Feature.objects.get_or_create(
        title = "Coolness?",
        description = "Is this package cool?",
        grid = grid1
    )
    feature.save()