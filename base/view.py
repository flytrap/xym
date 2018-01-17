#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from django.http.response import HttpResponseBase
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet

from base.execption import FlytrapException

from .response import SimpleResponse
from .serializer import BaseSerializer


class ViewMixin(object):
    serializer_class = BaseSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        """封装响应"""
        if not isinstance(response, HttpResponseBase):
            response = SimpleResponse(self.resp_ok(response))
        super_instance = super(ViewMixin, self)
        if hasattr(super_instance, 'finalize_response'):
            return super_instance.finalize_response(request, response, *args, **kwargs)

    def resp(self, data, status):
        if isinstance(data, dict):
            data["status"] = status
            return SimpleResponse(data)
        if isinstance(data, str):
            return SimpleResponse({"results": data, "status": status})
        if hasattr(self, 'get_serializer'):
            return SimpleResponse(self.get_serializer(data).data)

    def resp_ok(self, data):
        return self.resp(data, 'ok')

    def resp_failed(self, data):
        return self.resp(data, 'error')


class BaseModeView(ViewMixin, ModelViewSet):
    def handle_exception(self, exc):
        if isinstance(exc, FlytrapException):
            return SimpleResponse({"status": "error", "message": exc.message})
        return super(BaseModeView, self).handle_exception(exc)


class BaseViewSet(ViewMixin, GenericAPIView):
    pass


class BaseMongoViewSet(ViewMixin, MongoModelViewSet):
    pass
