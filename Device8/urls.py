from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import path
from .views import home
from Device8 import views

#app_name='home'

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', home, name='home'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),  
    path('login_user', views.login_user, name="login"),
]