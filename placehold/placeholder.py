# coding=utf-8
# base django
import os
import sys
from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
# 在模板里面配置的{{secret_key}} 再次生成时，就变成了随机的
SECRET_KEY = os.environ.get('SECRET_KEY', '!$s&*ys1cnb-73!t()w0$#%(brh)_bvt2ucqjv+^lv)rr)^@d-')
ALLOWED_HOST = os.environ.get("ALLOWED_HOST", "localhost").split(',')
# 设置
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


# url配置
urlpatterns = (
    url(r'^$', index),
)
# 使用wsgi
application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
