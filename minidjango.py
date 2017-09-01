#coding=utf-8
#base django
import os
import sys
from django.conf import settings
DEBUG=os.environ.get('DEBUG','on')=='on'

SECRET_KEY=os.environ.get('SECRET_KEY','{{secret_key}}')
ALLOWED_HOST=os.environ.get("ALLOWED_HOST","localhost").split(',')

