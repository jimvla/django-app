import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings
from Device8.models import Device8
from sqlalchemy import create_engine, URL


class Command(BaseCommand):
    help = "A command to add .csv file data to the database"

    def handle(self, *args, **options):
        csv_file = 'device8-2-2020.csv'
        colnames = ['time', 'PM1', 'PM10', 'PM25','RH','T']
        data = pd.read_csv((csv_file),names = colnames, parse_dates = ['time'],low_memory=False)
        data = data.tail(-1)
                
        url_object = URL.create(
            "mysql",
            username= settings.DATABASES['default']['USER'],
            password= settings.DATABASES['default']['PASSWORD'],  
            host= settings.DATABASES['default']['HOST'],
            database= settings.DATABASES['default']['NAME'],
        )

        engine = create_engine(url_object)
        data.to_sql(Device8, if_exists='append', con=engine, index =False)
