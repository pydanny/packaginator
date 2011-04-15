from package.models import Category, Package

def make():
    
    category, created = Category.objects.get_or_create(
        title="App",
        slug="apps",
        description="Small components used to build projects."
    )
    category.save()
    
    package, created = Package.objects.get_or_create(
        category = category,
        participants = "malcomt,jacobian",
        repo_description = "Increase your testing ability with this steroid free supplement.",
        repo_url = "https://github.com/pydanny/django-la-facebook",
        slug = "testability",
        title="Testability"
    )
    package.save()
    package, created = Package.objects.get_or_create(
        category = category,
        participants = "thetestman",
        repo_description = "Test everything under the sun with one command!",
        repo_url = "https://github.com/pydanny/django-uni-form",
        slug = "supertester",
        title="Supertester"
    )
    package.save()
    package, created = Package.objects.get_or_create(
        category = category,
        participants = "pydanny",
        repo_description = "Make testing as painless as waxing your legs.",
        repo_url = "https://github.com/cartwheelweb/packaginator",
        slug = "serious-testing",
        title="Serious Testing"
    )
    package.save()    
    package, created = Package.objects.get_or_create(
        category = category,
        participants = "pydanny",
        repo_description = "Yet another test package, with no grid affiliation.",
        repo_url = "https://github.com/djangopackages/djangopackages",
        slug = "another-test",
        title="Another Test"
    )
    package.save()