from django.db import models
#from django.utils import timezone

# Create your models here.

class Device8 (models.Model):
    time = models.DateTimeField(('time'), auto_now=False)
    PM1 = models.FloatField(('PM1(ug/m3)'))
    PM10 = models.FloatField(('PM10(ug/m3)'))
    PM25 = models.FloatField(('PM2.5(ug/m3)'))    
    RH = models.FloatField(('RH(%)'))
    T = models.FloatField(('T(C)'))

    class Meta:
        verbose_name = ("Device8")
        verbose_name_plural = ("Device8 Data")

    def __str__(self):
        return "{} - {}".format(self.time, self.PM1)
