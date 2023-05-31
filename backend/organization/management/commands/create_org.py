from django.core.management.base import BaseCommand
from films.constants import DEFAULT_CATEGORIES, DEFAULT_GENRES
from films.services import create_categories_from_names, create_genres_from_names
from organization.models import Organization

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            "--name", dest="name", type=str, required=True, help="Org name"
        )
        parser.add_argument(
            "--code", dest="code", type=str, required=True, help="Org code"
        )
        parser.add_argument(
            "--domain", dest="domain", type=str, required=True, help="Org domain"
        )

    def handle(self, *args, **options):
        org = Organization.objects.create(
            name=options["name"],
            code=options["code"],
            is_active=True,
            domain=options["domain"],
        )
        create_genres_from_names(org=org, genre_names=DEFAULT_GENRES)
        create_categories_from_names(org=org, category_names=DEFAULT_CATEGORIES)
        print("Org with id %s was created" % org.id)
        self.stdout.write(self.style.SUCCESS('Org with id %s was created' % org.id))
