__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
from LepViewer.views import *

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    # url(r'^status/$', getComponentStatus),
    url(r'^status/(?P<component>.+)/(?P<server>.+)/(?P<requestId>\d+)/$', getComponentStatus),
    url(r'^status/(?P<component>.+)/(?P<server>.+)/$', getComponentStatus),

    url(r'^cpustat/$', getCpuStat),
    url(r'^cpustat/(?P<server>.+)/$', getCpuStat),

    url(r'^cputop/$', getCpuTopData),
    url(r'^cputop/(?P<server>.+)/$', getCpuTopData),

    url(r'^perfcpu/$', getPerfCpuClockData),
    url(r'^perfcpu/(?P<server>.+)/$', getPerfCpuClockData),

    url(r'^memstat/$', getMemoryStat),
    url(r'^memstat/(?P<server>.+)/$', getMemoryStat),

    url(r'^ping/(?P<server>.+)/$', pingServer),

    url(r'^capacity/$', getComponentCapacity),
    url(r'^capacity/(?P<component>.+)/(?P<server>.+)/$', getComponentCapacity),

    url(r'^test/$', showTestPage),
    url(r'^test/(?P<server>.+)/$', showTestPage),

    url(r'^$', showHomepage),
    url(r'^(?P<server>.+)/$', showHomepage),
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
