from django.core.management.base import BaseCommand
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import math

class Command(BaseCommand):
    help = "A command to find the best ARIMA model based on AIC value"

    def handle(self, *args, **options): 
        csv_file = 'device8-2-2020.csv'
        colnames = ['time', 'PM1', 'PM10', 'PM25','RH','T']
        data = pd.read_csv((csv_file),names = colnames, parse_dates = ['time'],low_memory=False)
        data = data.tail(-1)

        # Applying Seasonal ARIMA model to forecast the data 
        mod = sm.tsa.SARIMAX(data['PM1'], trend='n', order=(2,1,1), seasonal_order=(2,1,0,7))
        results = mod.fit()
        print(results.summary())

        results.plot_diagnostics(figsize=(15,12))
        plt.show()