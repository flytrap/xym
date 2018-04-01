#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from django.conf.urls import url
from .views import GradeView

urlpatterns = [
    url('^$', GradeView.as_view({'get': 'list', 'post': 'create'}), ),
    url('^first/$', GradeView.as_view({'get': 'first'}), ),
    url('^query/$', GradeView.as_view({'get': 'query'}), ),
    url('^(?P<pk>\d+)$', GradeView.as_view({'get': 'retrieve'}), ),
]
