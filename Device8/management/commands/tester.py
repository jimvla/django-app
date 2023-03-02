from Device8.models import Device8
import plotly.express as px
from django.core.management.base import BaseCommand
import pandas as pd

class Command(BaseCommand):
    help = "A command to add .csv file data to the database"

    def handle(self, *args, **options):
        sql_query = Device8.objects.all().values()
        data = pd.DataFrame(sql_query)
        print(data)