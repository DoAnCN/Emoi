import json
import requests
import pytz

from django.template.response import TemplateResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from requests.auth import HTTPBasicAuth
from manager.models import Host
from monitor.models import Network

# Create your views here.
def dashboard(request):
    hosts_data = Host.objects.filter(monitor='a').values('ip', 'name', 'os', 'monitor',
     'date_add', 'last_alive', 'id_agent')
    data = {
        'hosts_value' :list(hosts_data),
        'memory_value' :[],
    }
    
    auth = HTTPBasicAuth('foo', 'bar')

    for host in hosts_data:
        memory = requests.get('http://127.0.0.1:55000/syscollector/{0}/'
                                'hardware?pretty&select=ram_free,scan_time,'
                                'ram_usage,cpu_name,ram_total'.format(host["id_agent"]),auth=auth)
        obj_hw=memory.json()
        info_memory=[
            host['name'],
            obj_hw['data']['ram']['usage'],
            obj_hw['data']['ram']['free'],
        ]
        data['memory_value'].append(info_memory)

    return render(request,'index.html',{'data':json.dumps(data)})

def network(request,host_name):
    data = {
        'hosts_value': list(Host.objects.filter(monitor='a').values('name')),
        'network_value': [],
        'network_value_packet': [],
    }
    
    auth = HTTPBasicAuth('foo', 'bar')

    host = Host.objects.get(name=host_name, monitor='a')
    if host:
        network = requests.get(
            'http://127.0.0.1:55000/syscollector/{0}/netiface?pretty&'
            'select=scan_time,tx_packets,tx_bytes,tx_dropped,tx_errors,'
            'rx_packets,rx_bytes,rx_dropped,rx_errors'.format(
                host.id_agent), auth=auth)
        obj=network.json()
        Network.objects.create(id_agent=host.id_agent,
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
        timezone=pytz.timezone('Asia/Ho_Chi_Minh')

        network_data = Network.objects.filter(id_agent=host.id_agent)

        for network in network_data:
            info_network=[
                network.n_scan_time.astimezone(timezone).strftime('%Y/%m/%d %H:%M:%S'),
                network.tx_bytes,network.tx_errors,
                network.rx_bytes,network.rx_errors,
            ]
            data['network_value'].append(info_network)

            info_network_packet=[
                network.n_scan_time.astimezone(timezone).strftime('%Y/%m/%d %H:%M:%S'),
                network.tx_packets,network.tx_dropped,
                network.rx_packets,network.rx_dropped,
            ]
            data['network_value_packet'].append(info_network_packet)

    return TemplateResponse(request,'network_agent.html', {'data':json.dumps(data)})

