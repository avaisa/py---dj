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
BASE_DIR = os.path.dirname(__file__)

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
    INSTALLED_APPS=(
        'django.contrib.staticfiles',

    ),
    TEMPLATES=(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': (os.path.join(BASE_DIR, 'templates'),),

        },
    ),
    STATICFILES_DIRS=(
        os.path.join(BASE_DIR, 'static'),

    ),
    STATIC_URL='/static/',
)

from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django import forms
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.cache import cache
import hashlib
from django.views.decorators.http import etag
from django.core.urlresolvers import reverse
from django.shortcuts import render


class ImageForm(forms.Form):
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format='PNG'):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '{}.{}.{}'.format(width, height, image_format)

        content = cache.get(key)
        if content is None:

            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{}*{}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft, texttop), text, fill=(255, 255, 255))

            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60 * 60)
        return content


def index(request):
    # 这个example=/image/50x50/
    example = reverse('placeholder', kwargs={'width': 50, 'height': 50})
    context = {
        # 展示全路径http://localhost:8000/image/50x50/
        'example': request.build_absolute_uri(example)
    }
    return render(request, 'home.html', context)


def generate_etag(request, width, height):
    content = 'Placeholder:{0}x{1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(generate_etag)
def placeholder(request, width, height):
    # 校验输入的数据
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid Image Request')


# url配置
urlpatterns = (
    url(r'^$', index, name='index'),
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder')
)
# 使用wsgi
application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
