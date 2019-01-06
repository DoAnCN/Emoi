from django.db import models

# Create your models here.
class Hardware(models.Model):
    id_agent = models.CharField('ID Agent',max_length=255,null=True)
    total = models.IntegerField('Total Memory',null=True)
    usage = models.IntegerField('Usage Memory',null=True)
    free = models.IntegerField('Free Memory',null=True)
    cpu_name = models.CharField('CPU Name',max_length=255,null=True)
    hw_scan_time = models.DateTimeField('Ram Scan Time',null=True)

    def __str__(self):
        return self.id_agent

class Network(models.Model):
    id_agent = models.CharField('ID Agent',max_length=255,null=True)
    n_scan_time = models.DateTimeField('Network Scan Time',null=True)
    tx_packets= models.IntegerField('Transmit Packets',null=True)
    tx_bytes= models.IntegerField('Transmit Bytes',null=True)
    tx_errors= models.IntegerField('Transmit Errors',null=True)
    tx_dropped= models.IntegerField('Transmit Dropped',null=True)
    rx_packets= models.IntegerField('Receive Packets',null=True)
    rx_bytes= models.IntegerField('Receive Bytes',null=True)
    rx_errors= models.IntegerField('Receive Errors',null=True)
    rx_dropped= models.IntegerField('Receive Dropped',null=True)

    def __str__(self):
        return self.id_agent
