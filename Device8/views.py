from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def home(request):
    # query the database for the data to plot
    SQLdata = Device8.objects.values_list('time', 'PM1')

    # format the data for the Plotly chart
    x = [row[0] for row in SQLdata]
    y = [row[1] for row in SQLdata]
    plot_data = [go.Scatter(x=x, y=y)]
    
    # create a Plotly chart
    layout = go.Layout(title="Plotly Chart")
    figure = go.Figure(data=plot_data, layout=layout)

    # render the chart and other content in the home.html template
    return render(request, 'home.html', {'figure': figure})

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
