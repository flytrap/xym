from base.view import BaseModeView

from .models import People
from .serializers import PeopleSerializer
from .filter import PeopleFilter


# Create your views here.
class GradeView(BaseModeView):
    serializer_class = PeopleSerializer
    queryset = People.objects.all()
    filter_class = PeopleFilter
    permission_classes = ()

    def list(self, request, *args, **kwargs):
        return super(GradeView, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(GradeView, self).retrieve(request, *args, **kwargs)
