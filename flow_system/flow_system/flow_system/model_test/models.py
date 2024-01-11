from datetime import datetime
from django.db import models

# Create your models here.
class TlsRes(models.Model):
    name = models.CharField(max_length=1000)
    result = models.CharField(max_length=10, default='none')
    
    def __str__(self):
        return self.name

class FlowRes(models.Model):
    name = models.CharField(max_length=1000)
    result = models.CharField(max_length=10, default='none')

    def __str__(self):
        return self.name


class ImageRes(models.Model):
    name = models.CharField(max_length=1000)
    result = models.CharField(max_length=10, default='none')
    def __str__(self):
        return self.name
    
class HeartbeatRes(models.Model):
    domain = models.CharField(max_length=128, default=None, null=True)
    is_http = models.BooleanField(default=None, null=True)
    sequence_len = models.IntegerField(default=None, null=True)
    sequence_mean = models.DecimalField(max_digits=20, decimal_places=10, default=None, null=True)
    create_time = models.DateField(default=datetime.now)
    # update_time = models.DateField()


