__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from django.http import HttpResponse
from django.shortcuts import render

import datetime

# Create your views here.
from django.template import Context
from django.template.loader import get_template
from backend.LepDClient import LepDClient
from backend.MemoryMonitor import MemoryMonitor
from backend.CPUMonitor import CPUMonitor
from backend.IOMonitor import IOMonitor
from backend.Languages import Languages
from backend.PerfMonitor import PerfMonitor

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def showHomepage(request, server=None):
    template = get_template('index.html')
    
    html = None
    if (server == None):
        html = template.render(Context({
            'request': request,
            'languages': Languages().getLanguagePackForCN(),
        }))
    else:
        html = template.render(Context({
            'request': request,
            'languages': Languages().getLanguagePackForCN(),
            'server': server
        }))

    return HttpResponse(html)

def showTestPage(request, server=''):
    template = get_template('test.html')

    html = template.render(Context({
        'request': request,
        'server': server
    }))
        
    return HttpResponse(html)

def getComponentStatus(request, component='', server='', requestId=''):
    if( request.method != 'GET' ):
        return

    try:
        if( component == '' or server == ""):
            return

        # Send JSON RPC request to the server, and get the JSON response.
        # now. I'm mocking the data here
        if (component == "cpu"):
            monitor = CPUMonitor(server)
            return JSONResponse(monitor.getStatus())
        elif (component == 'iotop'):
            monitor = IOMonitor(server)
            return JSONResponse(monitor.getIoTopData())
        elif (component == "memory"):
            monitor = MemoryMonitor(server)
            return JSONResponse(monitor.getStatus())
        elif (component == "io"):
            startTime = datetime.datetime.now()
            responseData = IOMonitor(server).getStatus()
            responseData['requestId'] = requestId
            endTime = datetime.datetime.now()
            duration = "%.1f" % ((endTime - startTime).total_seconds())
            responseData['djangoViewTotalDuration'] = duration
            return JSONResponse(responseData)
        elif (component == "avgload"):
            monitor = CPUMonitor(server)
            return JSONResponse(monitor.getAverageLoad())
    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)

def pingServer(request, server=''):
    if( request.method != 'GET' ):
        return

    try:
        if( server == '' ):
            print("LEPD serer is not specified!")
            return
        
        print("LEPD address: " + server)
        client = LepDClient(server)
        
        result = {}
        result['result'] = client.ping()
        
        if (result['result']):
            # get cpu count
            cpuMonitor = CPUMonitor(server)
            result['cpuCoreCount'] = cpuMonitor.getCapacity()['coresCount']
            
            memMonitor = MemoryMonitor(server)
            result['memoryTotal'] = memMonitor.getCapacity()['capacity']

        return JSONResponse(result)
    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)


def getComponentCapacity(request, component='', server=''):
    if( request.method != 'GET' ):
        return

    try:
        if( component == '' ):
            return

        if (component == "cpu"):
            monitor = CPUMonitor(server)
            return JSONResponse(monitor.getCapacity())
        elif (component == "memory"):
            monitor = MemoryMonitor(server)
            return JSONResponse(monitor.getCapacity())
        elif (component == "io"):
            monitor = IOMonitor(server)
            return JSONResponse(monitor.getCapacity())
    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)

def getCpuStat(request, server=''):
    if( request.method != 'GET' ):
        return

    try:
        monitor = CPUMonitor(server)
        return JSONResponse(monitor.getStat())

    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)

def getPerfCpuClockData(request, server=''):
    if( request.method != 'GET' ):
        return

    try:
        monitor = PerfMonitor(server)
        return JSONResponse(monitor.getPerfCpuClock())

    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)

def getCpuTopData(request, server=''):
    if( request.method != 'GET' ):
        return

    try:
        monitor = CPUMonitor(server)
        return JSONResponse(monitor.getTopOutput())

    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)


def getMemoryStat(request, server=''):
    if( request.method != 'GET' ):
        return

    try:
        monitor = MemoryMonitor(server)
        return JSONResponse(monitor.getMemoryStat())

    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)


# def getProcMemInfo(request, server=''):
#     if( request.method != 'GET' ):
#         return
# 
#     try:
#         monitor = MemoryMonitor(server)
#         return JSONResponse(monitor.getMemInfo())
# 
#     except Exception as ex:
#         print(ex)
#         return HttpResponse(status=404)
