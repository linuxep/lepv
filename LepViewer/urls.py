__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
from LepViewer.views import *

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    # url(r'^status/$', getComponentStatus),
    url(r'^status/(?P<component>.+)/(?P<server>.+)/(?P<requestId>\d+)/(?P<config>.+)/$', getComponentStatus),
    url(r'^status/(?P<component>.+)/(?P<server>.+)/(?P<requestId>\d+)/$', getComponentStatus),
    url(r'^status/(?P<component>.+)/(?P<server>.+)/$', getComponentStatus),

    url(r'^cpustat/(?P<server>.+)/(?P<requestId>\d+)/(?P<config>.+)/$', getCpuStat),
    url(r'^cpustat/(?P<server>.+)/(?P<config>.+)/$', getCpuStat),
    url(r'^cpustat/(?P<server>.+)/$', getCpuStat),
    url(r'^cpustat/$', getCpuStat),

    url(r'^cputop/(?P<server>.+)/(?P<requestId>\d+)/(?P<config>.+)/$', getCpuTopData),
    url(r'^cputop/(?P<server>.+)/(?P<config>.+)/$', getCpuTopData),
    url(r'^cputop/(?P<server>.+)/$', getCpuTopData),
    url(r'^cputop/$', getCpuTopData),

    url(r'^perfcpu/(?P<server>.+)/(?P<requestId>\d+)/(?P<config>.+)/$', getPerfCpuClockData),
    url(r'^perfcpu/(?P<server>.+)/(?P<config>.+)/$', getPerfCpuClockData),
    url(r'^perfcpu/(?P<server>.+)/$', getPerfCpuClockData),
    url(r'^perfcpu/$', getPerfCpuClockData),

    url(r'^procrank/(?P<server>.+)/(?P<requestId>\d+)/(?P<config>.+)/$', getProcrank),
    url(r'^procrank/(?P<server>.+)/(?P<config>.+)/$', getProcrank),
    url(r'^procrank/(?P<server>.+)/$', getProcrank),
    url(r'^procrank/$', getProcrank),

    url(r'^ping/(?P<server>.+)/(?P<requestId>\d+)/(?P<config>.+)/$', pingServer),
    url(r'^ping/(?P<server>.+)/(?P<config>.+)/$', pingServer),
    url(r'^ping/(?P<server>.+)/$', pingServer),
    url(r'^ping/$', pingServer),

    url(r'^command/(?P<server>.+)/(?P<command>.+)/$', runCommand),

    url(r'^processorcount/(?P<server>.+)/$', getProcessorCount),
    
    url(r'^capacity/(?P<component>.+)/(?P<server>.+)/(?P<requestId>\d+)/(?P<config>.+)/$', getComponentCapacity),
    url(r'^capacity/(?P<component>.+)/(?P<server>.+)/(?P<config>.+)/$', getComponentCapacity),
    url(r'^capacity/(?P<component>.+)/(?P<server>.+)/$', getComponentCapacity),
    url(r'^capacity/$', getComponentCapacity),

    url(r'^test/$', showTestPage),
    url(r'^test/sanity/$', showSanityTestPage),
    url(r'^test/lepdperformance/$', showLepdPerformanceTestPage),

    url(r'^methodmap/$', getMethodMap),

    url(r'^(?P<config>.+)/$', showHomepage),
    url(r'^$', showHomepage),
    url(r'm/^$', showHomepage),
]

# Here is the code for Serving files in development (DEBUG is True)
# Or temp run secure mode when production env (DEBUG is False)
#   python manage.py runserver --insecure
# Please see: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#runserver
#
# Or let others(uwsgi/ngnix/apache) to serve static file
from django.conf import settings
from django.views.static import serve
if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
            'show_indexes': True,
        }),
    ]
