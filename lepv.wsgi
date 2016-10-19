import os
import sys	
sys.path.append('/opt/deploy_lepv/LepViewer/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'LepViewer.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()