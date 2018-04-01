from django.http import Http404
from rest_framework.response import Response

from flytrap.base.view import BaseModeView
from flytrap.base.tools.decorators import cache_response

from .models import People
from .serializers import PeopleSerializer
from .filter import PeopleFilter


# Create your views here.
class GradeView(BaseModeView):
    serializer_class = PeopleSerializer
    queryset = People.objects.select_related('grade')
    filter_class = PeopleFilter
    permission_classes = ()

    def get_object(self):
        if self.action == 'first':
            obj = self.queryset.order_by('id').first()
            if obj:
                return obj
            raise Http404
        return super(GradeView, self).get_object()

    def filter_queryset(self, queryset):
        if self.action == 'query':
            return People.objects.query_people(self.request.GET.get('name'))
        return super(GradeView, self).filter_queryset(queryset)

    def get_serializer(self, *args, **kwargs):
        if self.action == 'query':
            return [super(GradeView, self).get_serializer(queryset, many=True).data for queryset in args[0]]
        return super(GradeView, self).get_serializer(*args, **kwargs)

    @cache_response(365)
    def list(self, request, *args, **kwargs):
        """获取门人列表"""
        return super(GradeView, self).list(request, *args, **kwargs)

    def first(self, request, *args, **kwargs):
        """获取根节点"""
        return self.retrieve(request, *args, **kwargs)

    # @cache_response(365)
    def retrieve(self, request, *args, **kwargs):
        """获取指定人"""
        return super(GradeView, self).retrieve(request, *args, **kwargs)

    @cache_response(365 * 24)
    def query(self, request, *args, **kwargs):
        """搜索人"""
        queryset = People.objects.query_people(self.request.GET.get('name'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = [super(GradeView, self).get_serializer(queryset, many=True).data for queryset in page]
            return self.get_paginated_response(data)

        data = [super(GradeView, self).get_serializer(queryset, many=True).data for queryset in page]
        return Response(data)
