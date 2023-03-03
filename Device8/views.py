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

# Create your views here.
def home(request):
    if request.method=="POST":
        dropdown = request.POST.get('dropdown')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        Queryset = Device8.objects.filter(time__range=[start_date, end_date]).values()
        data = pd.DataFrame(Queryset)
        data['time'] = pd.to_datetime(data['time'])

        #Check if user provide correct dates
        if data.empty:
            plot_div = "No Data Found for that Date Range. Please try different values"

            context = {
                'plot_div': plot_div
            }
            return render(request, "home.html", context)
        
        #Checking and Drop Outliers
        Q1 = data[dropdown].quantile(0.25)
        Q3 = data[dropdown].quantile(0.75)

        IQR = Q3 - Q1

        # Upper bound
        upper = np.where(data[dropdown] >= (Q3+3*IQR))
        # Lower bound
        lower = np.where(data[dropdown] <= (Q1-3*IQR))
        
        # Removing the Outliers
        data.drop(upper[0], inplace = True)
        data.drop(lower[0], inplace = True)

        new_df = pd.DataFrame({
        'date': data['time'].dt.date.unique(),
        'open': data.groupby(data['time'].dt.date)['PM1'].first(),
        'close': data.groupby(data['time'].dt.date)['PM1'].last(),
        'high': data.groupby(data['time'].dt.date)['PM1'].max(),
        'low': data.groupby(data['time'].dt.date)['PM1'].min(),
        })

        # Reset index of the new dataframe
        new_df = new_df.reset_index(drop=True)

        trace = go.Candlestick(
            x=new_df['date'],
            open=new_df['open'],
            high=new_df['high'],
            low=new_df['low'],
            close=new_df['close'],
            name='Candestick'
        )

        layout = go.Layout(
            title='Trend Line of '+ dropdown + '(ug/m3) over time',
            xaxis_title='Time',
            yaxis_title= dropdown + '(ug/m3)',
            xaxis=dict(rangeslider=dict(visible=False)),
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            ),
            template = 'plotly_dark'
        )
               
        #Calculate Rolling Mean
        #rolling_mean = data[dropdown].rolling(window=100).mean()
        ema10 = data[dropdown].ewm(span=10).mean()
        #ema25 = data[dropdown].ewm(span=25).mean()
        #ema99 = data[dropdown].ewm(span=99).mean()    
        #trace1 = go.Scatter(x=data['time'], y=data[dropdown], name=dropdown)
        trace2 = go.Scatter(x=data['time'], y=ema10, line=dict(color='yellow', width=1), name='TREND')
        #fig.add_scatter(x=data['time'], y=ema25, line=dict(color='pink', width=2), name='EMA(25)')
        #fig.add_scatter(x=data['time'], y=ema99, line=dict(color='purple', width=2), name='EMA(99)')
        candle = [trace, trace2]
        #traces = [trace1, trace2]
        #Plot
        fig = go.Figure(data=candle, layout=layout)
        
        plot_div = plot(fig, output_type='div')

        context = {
                'plot_div': plot_div
        }
            
        return render(request, "home.html", context)
    else:
        #Homepage initial message
        plot_div = "Your Plot is going here! Just choose a Start Date and an End Date to plot your chart"

        context = {
            'plot_div': plot_div,
            }
        return render(request, "home.html", context)

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
