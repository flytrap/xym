#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '../../')
sys.path.insert(0, '../../src/')
print(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xym.settings')
application = get_wsgi_application()

from grade.models import People, Grade
from django.test import TestCase


class TestImport(TestCase):
    pass
