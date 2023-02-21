from django.contrib import admin, messages
from django import forms
from django.conf import settings
from django.shortcuts import render
from .models import Device8
import pandas as pd
from django.urls import path, reverse
from sqlalchemy import create_engine, URL
from django.http import HttpResponseRedirect


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class Device8Admin(admin.ModelAdmin):
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, "Wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)
            
            colnames = ['time', 'PM1', 'PM10', 'PM25','RH','T']
            data = pd.read_csv((csv_file),names=colnames, header=None, parse_dates = ['time'], low_memory=False)
            data = data.tail(-1)	
            url_object = URL.create(
                "mysql",
                username= settings.DATABASES['default']['USER'],
                password= settings.DATABASES['default']['PASSWORD'],  
                host= settings.DATABASES['default']['HOST'],
                database= settings.DATABASES['default']['NAME'],
            )
            engine = create_engine(url_object)
            data.to_sql(Device8._meta.db_table, if_exists='append', con=engine, index =False)
            
            url = reverse('admin:index')
            return HttpResponseRedirect(url)
        
        form = CsvImportForm()
        data = {"form": form}
        return render(request, 'admin/csv_upload.html', data)
	
admin.site.register(Device8, Device8Admin)


