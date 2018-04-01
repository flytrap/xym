#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from flytrap.base.serializer import BaseSerializer, BaseModelSerializer, serializers

from .models import UserProfile
from grade.serializers import PeopleSerializer

User = get_user_model()


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserProfileSerializer(BaseModelSerializer):
    user = UserSerializer(read_only=True)
    people = PeopleSerializer(read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def save(self, **kwargs):
        if self.initial_data.get('email'):
            user = getattr(self.context.get('request'), 'user')
            user.email = self.initial_data.get('email')
            user.save()
        return super(UserProfileSerializer, self).save(**kwargs)


class BindSerializer(BaseSerializer):
    people_id = serializers.IntegerField(label='传人id', required=True)
    user_id = serializers.IntegerField(label='用户id', required=True)

    def create(self, validated_data):
        self.instance, _ = UserProfile.objects.get_or_create(user=self.data.get('user'))
        parent_people = getattr(self.context.get('request'), 'people')
        people = self.data.get('people')
        if parent_people and parent_people.childes.filter(id=people.id).exists():
            self.instance.people = people
            self.instance.save()
            return self.instance
        raise ValidationError({'people': '没有找到该弟子'})

    def is_valid(self, raise_exception=False):
        people_id = self.initial_data.get('people_id')
        user_id = self.initial_data.get('user_id')

        from grade.models import People
        people = People.objects.filter(id=people_id).first()
        user = User.objects.filter(id=user_id).first()
        if not people:
            self.errors['people_id'] = '门人不存在'
        if not user:
            self.errors['user_id'] = '用户不存在'
        self.data['user'] = user
        self.data['people'] = people
        return super(BindSerializer, self).is_valid(raise_exception)
