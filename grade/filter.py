#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from django_filters.rest_framework import FilterSet
from .models import People


class PeopleFilter(FilterSet):
    class Meta:
        model = People
        fields = {
            'name': {'contains'}
        }
