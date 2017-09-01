#coding=utf-8
#base django
import os
import sys
from django.conf import settings
DEBUG=os.environ.get('DEBUG','on')=='on'

SECRET_KEY=os.environ.get('SECRET_KEY','{{secret_key}}')
ALLOWED_HOST=os.environ.get("ALLOWED_HOST","localhost").split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOST=ALLOWED_HOST,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',


    ),
)


from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

def index(request):
    return HttpResponse("nana")

urlpatterns=(
    url(r'^$',index),
)

application=get_wsgi_application()
if __name__=="__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

