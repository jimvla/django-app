from django.core.management.base import BaseCommand
import numpy as np
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from Device8.models import Device8


class Command(BaseCommand):
    help = "A command to find the number of samples by day of the week"

    def handle(self, *args, **options): 

        data = Device8.objects.all()
        df = pd.DataFrame(data)

        # group data by date and count number of samples each day
        daily_count = df.groupby(df['time'].dt.dayofweek)['time'].count()

        # map day of week numbers to day names
        day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

        # get day names for each slice of the pie chart
        labels = [day_names[idx] for idx in daily_count.index]

        # plot pie chart
        plt.rcParams['figure.facecolor'] = 'white'
        plt.pie(daily_count, labels=labels, autopct='%1.1f%%')
        #plt.legend(title='Days of the Week', loc='best')
        plt.show()