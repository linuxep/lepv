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
from backend.MethodMap import MethodMap

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


def showHomepage(request, config='release'):
    template = get_template('index.html')
    
    if (config != 'debug'):
        config = 'release'

    html = template.render(Context({
        'request': request,
        'languages': Languages().getLanguagePackForCN(),
        'config': config
    }));

    return HttpResponse(html)

def showTestPage(request):
    template = get_template('test.html')

    html = template.render(Context({
        'request': request
    }))
        
    return HttpResponse(html)


def showSanityTestPage(request):
    template = get_template('sanityTest.html')

    html = template.render(Context({
        'request': request
    }))

    return HttpResponse(html)

def showLepdPerformanceTestPage(request):
    template = get_template('lepdPerformanceTesting.html')

    html = template.render(Context({
        'request': request
    }))

    return HttpResponse(html)

def getComponentStatus(request, component='', server='', requestId='', config='release'):
    if( request.method != 'GET' ):
        return

    try:
        if( component == '' or server == ""):
            return

        startTime = datetime.datetime.now()
        
        responseData = {}
        if (component == "cpu"):
            monitor = CPUMonitor(server=server, config=config)
            responseData = monitor.getStatus()
        elif (component == 'iotop'):
            responseData = IOMonitor(server=server, config=config).getIoTopData()
        elif (component == "memory"):
            responseData = MemoryMonitor(server=server, config=config).getStatus()
        elif (component == "io"):
            responseData = IOMonitor(server=server, config=config).getStatus()
        elif (component == "avgload"):
            responseData = CPUMonitor(server=server, config=config).getAverageLoad()

        responseData['requestId'] = requestId
        endTime = datetime.datetime.now()
        duration = "%.1f" % ((endTime - startTime).total_seconds())
        responseData['djangoViewTotalDuration'] = duration
        
        return JSONResponse(responseData)
    
    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)

def pingServer(request, server='', requestId='', config='release'):
    if( request.method != 'GET' ):
        return

    try:
        if( server == '' ):
            print("LEPD serer is not specified!")
            return
        
        print("LEPD address: " + server)
        client = LepDClient(server=server, config=config)
        
        result = {}
        result['connected'] = client.ping()
        
        if (result['connected']):
            # get cpu count
            cpuMonitor = CPUMonitor(server=server, config=config)
            cpuCapacityData = cpuMonitor.getCapacity()
            result['cpuCoreCount'] = cpuCapacityData['data']['coresCount']
            
            memMonitor = MemoryMonitor(server=server, config=config)
            memoryCapacityData = memMonitor.getCapacity()
            result['memoryTotal'] = memoryCapacityData['data']['capacity']

        return JSONResponse(result)
    except Exception as ex:
        return HttpResponse(status=404)

def runCommand(request, server, command):
    if( request.method != 'GET' ):
        return

    try:
        if( server == '' ):
            print("LEPD serer is not specified!")
            return

        print("LEPD address: " + server)
        client = LepDClient(server=server, config='debug')

        return JSONResponse(client.sendRequest(command))
    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)


def getComponentCapacity(request, component='', server='', requestId='', config='release'):
    if( request.method != 'GET' ):
        return

    try:
        if( component == '' ):
            return

        if (component == "cpu"):
            monitor = CPUMonitor(server, config)
            return JSONResponse(monitor.getCapacity())
        elif (component == "memory"):
            monitor = MemoryMonitor(server, config)
            return JSONResponse(monitor.getCapacity())
        elif (component == "io"):
            monitor = IOMonitor(server, config)
            return JSONResponse(monitor.getCapacity())
    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)

def getCpuStat(request, server='', requestId='', config='release'):
    if( request.method != 'GET' ):
        return

    try:
        monitor = CPUMonitor(server, config)
        return JSONResponse(monitor.getStat())

    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)

def getPerfCpuClockData(request, server='', requestId='', config='release'):
    if( request.method != 'GET' ):
        return

    try:
        monitor = PerfMonitor(server, config)
        return JSONResponse(monitor.getPerfCpuClock())

    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)

def getCpuTopData(request, server='', requestId='', config='release'):
    if( request.method != 'GET' ):
        return

    try:
        monitor = CPUMonitor(server, config)
        return JSONResponse(monitor.getTopOutput())

    except Exception as ex:
        return HttpResponse(status=404)


def getProcrank(request, server='', requestId='', config='release'):
    if( request.method != 'GET' ):
        return

    try:
        monitor = MemoryMonitor(server, config)
        return JSONResponse(monitor.getProcrank())

    except Exception as ex:
        # print(ex)
        return HttpResponse(status=404)

def getMethodMap(request):
    if( request.method != 'GET' ):
        return

    try:
        methodMap = MethodMap()
        return JSONResponse(methodMap.getMap())
    except Exception as ex:
        return HttpResponse(status=404)
