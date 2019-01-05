import json
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
import requests
from requests.auth import HTTPBasicAuth
from manager.models import Host
from monitor.models import Network
import pytz

# Create your views here.
def dashboard(request):
    hosts_data = Host.objects.all()
    network_data = Network.objects.all()
    data = {
        'hosts_value' :[],
        'network_value' :[],
        'network_value_2':[],
        'network_value_3':[],
        'hardware_value' :[],
    }
    auth = HTTPBasicAuth('foo', 'bar')

    for host in hosts_data:
        network = requests.get('http://192.168.102.142:55000/syscollector/{0}/netiface?pretty&select=scan_time,tx_packets,tx_bytes,tx_dropped,tx_errors,rx_packets,rx_bytes,rx_dropped,rx_errors'.format(host.id_agent),auth=auth)
        obj=network.json()
        Network.objects.create(id_agent='{0}'.format(host.id_agent),
                                n_scan_time=parse_datetime(obj['data']['items'][0]['scan_time'].replace('/','-')),
                                tx_bytes=obj['data']['items'][0]['tx']['bytes'],
                                tx_packets=obj['data']['items'][0]['tx']['packets'],
                                tx_errors=obj['data']['items'][0]['tx']['errors'],
                                tx_dropped=obj['data']['items'][0]['tx']['dropped'],
                                rx_bytes=obj['data']['items'][0]['rx']['bytes'],
                                rx_packets=obj['data']['items'][0]['rx']['packets'],
                                rx_errors=obj['data']['items'][0]['rx']['errors'],
                                rx_dropped=obj['data']['items'][0]['rx']['dropped'],
                          )

        hardware = requests.get('http://192.168.102.142:55000/syscollector/{0}/hardware?pretty&select=ram_free,scan_time,ram_usage,cpu_name,ram_total'.format(host.id_agent),auth=auth)
        obj_hw=hardware.json()
        info_hardware=[
            host.name,
            obj_hw['data']['ram']['usage'],
            obj_hw['data']['ram']['free'],
        ]
        data['hardware_value'].append(info_hardware)

        info_host={
            'ip':host.ip,
            'name': host.name,
            'os': host.os,
            'status':host.monitor,
            'date_add': host.date_add,
            'last_alive': host.last_alive,
        }
        data['hosts_value'].append(info_host)

    timezone=pytz.timezone('Asia/Ho_Chi_Minh')

    for network in network_data:
        if network.id_agent == '004':
            info_network=[
                network.n_scan_time.astimezone(timezone).strftime('%Y/%m/%d %H:%M:%S') ,
                network.tx_bytes,network.tx_errors,
                network.rx_bytes,network.rx_errors,
            ]
            data['network_value'].append(info_network)

        if network.id_agent == '007':
            info_network_2=[
                network.n_scan_time.astimezone(timezone).strftime('%Y/%m/%d %H:%M:%S') ,
                network.tx_bytes,network.tx_errors,
                network.rx_bytes,network.rx_errors,
            ]
            data['network_value_2'].append(info_network_2)

        if network.id_agent == '008':
            info_network_3=[
                network.n_scan_time.astimezone(timezone).strftime('%Y/%m/%d %H:%M:%S') ,
                network.tx_bytes,network.tx_errors,
                network.rx_bytes,network.rx_errors,
            ]
            data['network_value_3'].append(info_network_3)

    return render(request,'index.html',{'data':json.dumps(data)})

def agent(request,id_agent):
    return TemplateResponse(request,'agent.html')
