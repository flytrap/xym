#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from django.conf.urls import url
from .views import GradeView

urlpatterns = [
    url('^bi$', GradeView.as_view({'get': 'list'}), ),
    url('^people/$', GradeView.as_view({'get': 'list'}), ),
    url('^people/(?P<pk>\d+)', GradeView.as_view({'get': 'retrieve'}), ),
]
