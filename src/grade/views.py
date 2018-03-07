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

    @cache_response(365)
    def list(self, request, *args, **kwargs):
        """获取门人列表"""
        return super(GradeView, self).list(request, *args, **kwargs)

    # @cache_response(365)
    def retrieve(self, request, *args, **kwargs):
        """获取指定人"""
        return super(GradeView, self).retrieve(request, *args, **kwargs)

    @cache_response(365)
    def query(self, request, *args, **kwargs):
        """搜索人"""
        queryset_list = People.objects.query_people(request.GET.get('name'))
        data = [self.get_serializer(queryset, many=True).data for queryset in queryset_list]
        return Response(data)
