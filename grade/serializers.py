#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from flytrap.base.serializer import BaseModelSerializer, serializers
from .models import People, Grade


class GradeSerializer(BaseModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class SimplePeopleSerializer(BaseModelSerializer):
    grade = GradeSerializer(many=False)
    has_child = serializers.SerializerMethodField(method_name='_har_child')

    class Meta:
        model = People
        exclude = ('childes', 'user')

    @staticmethod
    def _har_child(obj):
        return obj.childes.exists()


class PeopleSerializer(SimplePeopleSerializer):
    childes = SimplePeopleSerializer(many=True)

    class Meta:
        model = People
        exclude = ('user',)
