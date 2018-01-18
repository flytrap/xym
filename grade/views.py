from rest_framework.response import Response

from flytrap.base.view import BaseModeView

from .models import People
from .serializers import PeopleSerializer
from .filter import PeopleFilter


# Create your views here.
class GradeView(BaseModeView):
    serializer_class = PeopleSerializer
    queryset = People.objects.select_related('grade')
    filter_class = PeopleFilter
    permission_classes = ()

    def list(self, request, *args, **kwargs):
        return super(GradeView, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(GradeView, self).retrieve(request, *args, **kwargs)

    def query(self, request, *args, **kwargs):
        queryset_list = People.objects.query_people(request.GET.get('name'))
        data = [self.get_serializer(queryset, many=True).data for queryset in queryset_list]
        return Response(data)
