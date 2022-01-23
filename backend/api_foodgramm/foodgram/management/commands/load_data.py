import csv

from django.core.management import BaseCommand
from foodgram.models import Ingredients


class Command(BaseCommand):
    help = 'Load a data csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['file']
        path = '/data/'+path
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            obj_list = []
            for row in reader:
                obj = Ingredients(name=row[0], measurement_unit=row[1])
                obj_list.append(obj)

            Ingredients.objects.bulk_create(reversed(obj_list))

