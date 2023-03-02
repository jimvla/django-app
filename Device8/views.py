from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Device8.models import Device8
from Device8.forms import DateForm
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
from django.db import connection


# Create your views here.
def home(request):
    if request.method=="POST":
        dropdown = request.POST.get('dropdown')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        Queryset = Device8.objects.filter(time__range=[start_date, end_date]).values()
        data = pd.DataFrame(Queryset)
        
        fig = go.Figure([go.Scatter(x=data['time'], y=data[dropdown])])
        fig.update_layout(title='Trend Line of '+ dropdown + '(ug/m3) over time')
        plot_div = plot(fig, output_type='div')

        context = {
                'plot_div': plot_div
        }
            
        return render(request, "home.html", context)
    else:
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
