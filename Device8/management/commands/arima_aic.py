from django.core.management.base import BaseCommand
import pandas as pd
from pmdarima.arima import auto_arima


class Command(BaseCommand):
    help = "A command to find the best ARIMA model based on AIC value"

    def handle(self, *args, **options):  
        csv_file = 'device8-2-2020.csv'
        colnames = ['time', 'PM1', 'PM10', 'PM25','RH','T']
        data = pd.read_csv((csv_file),names = colnames, parse_dates = ['time'],low_memory=False)
        data = data.tail(-1)
        model = auto_arima(data['PM1'], start_p=1, start_q=1,
                           max_p=2, max_q=1, m=7,
                           start_P=1,max_P=2, seasonal=True,
                           d=1, D=1, max_d = 2, max_D=2,trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
        print(model.aic())
