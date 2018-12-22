from django.db import models

# Create your models here.
class BasicInfo(models.Model):
    id_agent=models.IntegerField(primary_key=True)
    sys_name=models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    arch = models.CharField(max_length=255)
    os_name =models.CharField(max_length=255)
    os_version =models.CharField(max_length=255)
   

    def __str__(self):
        return self.sys_name

class Hardware(models.Model):
    id_agent = models.IntegerField(primary_key=True)
    total = models.IntegerField()
    usage = models.IntegerField()
    free = models.IntegerField()
    cpu_name = models.CharField(max_length=255)
    hw_scan_time = models.DateField()

    def __str__(self):
        return self.id_agent

class Network(models.Model):
    id_agent = models.IntegerField(primary_key=True)
    n_scan_time = models.DateField()
    mac = models.CharField(max_length=255)
    tx_packets= models.IntegerField()
    tx_bytes= models.IntegerField()
    tx_errors= models.IntegerField()
    tx_dropped= models.IntegerField()
    rx_packets= models.IntegerField()
    rx_bytes= models.IntegerField()
    rx_errors= models.IntegerField()
    rx_dropped= models.IntegerField()

    def __str__(self):
        return self.id_agent