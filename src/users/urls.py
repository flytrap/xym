#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from django.conf.urls import url
from .views import UserProfileView, BindPeopleView

urlpatterns = [
    url('^profile$', UserProfileView.as_view({'get': 'me', 'post': 'create', 'put': 'update'}), ),
    url('^bind/people$', BindPeopleView.as_view({'post': 'create'}), ),
]
