import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capnet_apps.settings")

application = get_wsgi_application()
