#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from rest_framework.exceptions import ValidationError

from flytrap.base.serializer import BaseModelSerializer, serializers
from .models import People, Grade


class GradeSerializer(BaseModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class SimplePeopleSerializer(BaseModelSerializer):
    grade = GradeSerializer(many=False)
    has_child = serializers.SerializerMethodField(method_name='_har_child')
    child_count = serializers.SerializerMethodField(method_name='_child_count')

    class Meta:
        model = People
        exclude = ('childes', 'user', 'parents')

    @staticmethod
    def _har_child(obj):
        return obj.childes.exists()

    @staticmethod
    def _child_count(obj):
        return obj.childes.count()


class PeopleSerializer(SimplePeopleSerializer):
    childes = SimplePeopleSerializer(many=True, required=False, read_only=True)
    parents = SimplePeopleSerializer(many=True, required=False, read_only=True)
    grade = GradeSerializer(required=False)

    class Meta:
        model = People
        exclude = ('user',)

    def is_valid(self, raise_exception=False):
        people = self.get_people()
        if not people:
            raise ValidationError('must bind user')
        return super(PeopleSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        people = self.get_people()
        validated_data['master_name'] = people.name
        validated_data['grade'] = Grade.objects.get_create_grade(people.grade.code + 1)
        validated_data['parents'] = [people]
        instance = super(PeopleSerializer, self).create(validated_data)
        people.childes.add(instance)
        people.save()
        return instance

    def get_people(self):
        if hasattr(self, '_people') and self._people:
            return self._people
        self._people = People.objects.filter(user=self.context.get('request').user).first()
        return self._people
