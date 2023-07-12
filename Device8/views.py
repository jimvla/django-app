from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Device8.models import Device8
from Device8.forms import DateForm
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import ta.trend as ta

# Home view for our page
def home(request):
    if request.method=="POST":
        
        # Get Inputs

        dropdown = request.POST.get('dropdown') # Value of Data
        radio = request.POST.get('inlineRadioOptions') # Frequency Selection
        MA = request.POST.get('inlineCheckbox1') # MA Flag
        EMA = request.POST.get('inlineCheckbox2')   # EMA Flag
        Boll = request.POST.get('inlineCheckbox3')  # Boll Flag
        Sar = request.POST.get('inlineCheckbox4')  # Sar Flag
        rolling_window = int(request.POST.get('typeNumber')) # Rolling Window Size
        start_date = request.POST.get('start_date')  # Starting Date of the plot
        end_date = request.POST.get('end_date') # Ending Date of the plot
        outliers = request.POST.get('inlineRadioOptions1') # Keep or Delete Outliers

        #How to make substraction with datetime 
        #new = pd.to_datetime(start_date) - timedelta(days=rolling_window)
        #print(start_date)
        #print(new)

        # Get Query from DB
        Queryset = Device8.objects.filter(time__range=[start_date, end_date]).values()

        # Check if user provides dates that exist in our data
        if (end_date < start_date):
            # Check if start date is earlier of end date
            plot_div = "Start date has to be earlier from the end date. Please try different dates."

            context = {
                'plot_div': plot_div
            }
            return render(request, "home.html", context) 
        
        elif (len(Queryset) == 0):
            # Check if we have available data for that specific range
            plot_div = "No Data found for that range of dates. Please try different dates."

            context = {
                'plot_div': plot_div
            }
            return render(request, "home.html", context) 
        
        else:

            # Make our pandas Dataframe
            data = pd.DataFrame(Queryset)
            data['time'] = pd.to_datetime(data['time'])

            # Remove Outliers
            if outliers == "True":
                # Checking and Drop Outliers
                Q1 = data[dropdown].quantile(0.25)
                Q3 = data[dropdown].quantile(0.75)

                IQR = Q3 - Q1

                # Upper bound
                upper = np.where(data[dropdown] >= (Q3+1.5*IQR))
                # Lower bound
                lower = np.where(data[dropdown] <= (Q1-1.5*IQR))
                
                # Removing the Outliers
                data.drop(upper[0], inplace = True)
                data.drop(lower[0], inplace = True)

                # New DataFrame for the Candlestick Plot
                if dropdown == 'PM1':
                    new_df = pd.DataFrame({
                    'date': data.groupby(pd.Grouper(key='time', freq=radio))['time'].first(),
                    'open': data.groupby(pd.Grouper(key='time', freq=radio))['PM1'].first(),
                    'close': data.groupby(pd.Grouper(key='time', freq=radio))['PM1'].last(),
                    'high': data.groupby(pd.Grouper(key='time', freq=radio))['PM1'].max(),
                    'low': data.groupby(pd.Grouper(key='time', freq=radio))['PM1'].min(),
                    })
                    trends = pd.DataFrame({
                        'date': data.groupby(pd.Grouper(key='time', freq='1H'))['time'].first(),
                        'mean': data.groupby(pd.Grouper(key='time', freq='1H'))['PM1'].mean(),
                    })
                elif dropdown == 'PM25':
                    new_df = pd.DataFrame({
                    'date': data.groupby(pd.Grouper(key='time', freq=radio))['time'].first(),
                    'open': data.groupby(pd.Grouper(key='time', freq=radio))['PM25'].first(),
                    'close': data.groupby(pd.Grouper(key='time', freq=radio))['PM25'].last(),
                    'high': data.groupby(pd.Grouper(key='time', freq=radio))['PM25'].max(),
                    'low': data.groupby(pd.Grouper(key='time', freq=radio))['PM25'].min(),
                    })
                    trends = pd.DataFrame({
                        'date': data.groupby(pd.Grouper(key='time', freq='1H'))['time'].first(),
                        'mean': data.groupby(pd.Grouper(key='time', freq='1H'))['PM25'].mean(),
                    })
                elif dropdown == 'PM10':
                    new_df = pd.DataFrame({
                    'date': data.groupby(pd.Grouper(key='time', freq=radio))['time'].first(),
                    'open': data.groupby(pd.Grouper(key='time', freq=radio))['PM10'].first(),
                    'close': data.groupby(pd.Grouper(key='time', freq=radio))['PM10'].last(),
                    'high': data.groupby(pd.Grouper(key='time', freq=radio))['PM10'].max(),
                    'low': data.groupby(pd.Grouper(key='time', freq=radio))['PM10'].min(),
                    })
                    trends = pd.DataFrame({
                        'date': data.groupby(pd.Grouper(key='time', freq='1H'))['time'].first(),
                        'mean': data.groupby(pd.Grouper(key='time', freq='1H'))['PM10'].mean(),
                    })    
                elif dropdown == 'RH':
                    new_df = pd.DataFrame({
                    'date': data.groupby(pd.Grouper(key='time', freq=radio))['time'].first(),
                    'open': data.groupby(pd.Grouper(key='time', freq=radio))['RH'].first(),
                    'close': data.groupby(pd.Grouper(key='time', freq=radio))['RH'].last(),
                    'high': data.groupby(pd.Grouper(key='time', freq=radio))['RH'].max(),
                    'low': data.groupby(pd.Grouper(key='time', freq=radio))['RH'].min(),
                    })
                    trends = pd.DataFrame({
                        'date': data.groupby(pd.Grouper(key='time', freq='1H'))['time'].first(),
                        'mean': data.groupby(pd.Grouper(key='time', freq='1H'))['RH'].mean(),
                    })  
                elif dropdown == 'T':
                    new_df = pd.DataFrame({
                    'date': data.groupby(pd.Grouper(key='time', freq=radio))['time'].first(),
                    'open': data.groupby(pd.Grouper(key='time', freq=radio))['T'].first(),
                    'close': data.groupby(pd.Grouper(key='time', freq=radio))['T'].last(),
                    'high': data.groupby(pd.Grouper(key='time', freq=radio))['T'].max(),
                    'low': data.groupby(pd.Grouper(key='time', freq=radio))['T'].min(),
                    })
                    trends = pd.DataFrame({
                        'date': data.groupby(pd.Grouper(key='time', freq='1H'))['time'].first(),
                        'mean': data.groupby(pd.Grouper(key='time', freq='1H'))['T'].mean(),
                    })

                # Reset index of the new DataFrame
                new_df = new_df.reset_index(drop=True)
                trends = trends.reset_index(drop=True)

                # Candlestick Trace and Layout
                trace = go.Candlestick(
                    x=new_df['date'],
                    open=new_df['open'],
                    high=new_df['high'],
                    low=new_df['low'],
                    close=new_df['close'],
                    name='Candestick'
                )

                layout = go.Layout(
                    title='Trend Line of '+ dropdown + ' over time',
                    xaxis_title='Time',
                    yaxis_title= dropdown ,
                    xaxis=dict(rangeslider=dict(visible=False)),
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="White"
                    ),
                    template = 'plotly_dark'
                )
                    
                candle = [trace]

                # Plot Figure + Trend Lines using MA, EMA, Bollinger Bands and PSAR
                fig = go.Figure(data=candle, layout=layout)
                if MA:      
                    trends['ma'] = trends['mean'].rolling(window=rolling_window).mean()
                    fig.add_trace(go.Scatter(x=trends['date'], y=trends['ma'], line=dict(color = 'yellow'), name= "Moving Average"))
                if EMA:
                    trends['ema'] = trends['mean'].ewm(span=rolling_window).mean()
                    fig.add_trace(go.Scatter(x=trends['date'], y=trends['ema'], line=dict(color = 'blue'), name= "Exponential MA"))
                if Boll:      
                    trends['rolling_mean'] = trends['mean'].rolling(window=rolling_window).mean()
                    trends['std'] = trends['mean'].rolling(window=rolling_window).std()
                    trends['UpperBand'] = trends['rolling_mean'] + 2 * trends['std']
                    trends['LowerBand'] = trends['rolling_mean'] - 2 * trends['std']
                    fig.add_trace(go.Scatter(x=trends['date'], y=trends['UpperBand'], line=dict(color = 'pink'), name= "Upper Bollinger Band"))
                    fig.add_trace(go.Scatter(x=trends['date'], y=trends['LowerBand'], line=dict(color = 'purple'), name= "Lower Bollinger Band"))
                if Sar:
                    new_df['parabolic_sar_up'] = ta.psar_up(new_df['high'], new_df['low'], new_df['close'], step=0.02, max_step=0.2)
                    new_df['parabolic_sar_down'] = ta.psar_down(new_df['high'], new_df['low'], new_df['close'], step=0.02, max_step=0.2)
                    fig.add_trace(go.Scatter(x=new_df['date'], y=new_df['parabolic_sar_up'], mode='markers', line=dict(color = 'green'), name= "Up Trend"))   
                    fig.add_trace(go.Scatter(x=new_df['date'], y=new_df['parabolic_sar_down'], mode='markers', line=dict(color = 'orange'), name= "Down Trend"))

                plot_div = plot(fig, output_type='div')

                #print(tabulate(new_df, headers = 'keys', tablefmt = 'psql'))
                new_df.to_excel("candlestick.xlsx")
                trends.to_excel("output.xlsx")


                #Add plot to home html page
                context = {
                        'plot_div': plot_div
                }
                    
                return render(request, "home.html", context)
    else:
        # Homepage initial message before plotting the graph
        plot_div = "Your Plot is going here!"

        context = {
            'plot_div': plot_div,
            }
        return render(request, "home.html", context)

# View for User Login and Authentication
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There was an error login in, try again"))
            return redirect("login")
    else:
        return render(request, 'registration/login.html', {})
