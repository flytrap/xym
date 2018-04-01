from rest_framework.permissions import IsAuthenticated
from flytrap.base.view import BaseViewSet, BaseModeView
from flytrap.base.response import SimpleResponse
from grade.models import People
from .models import UserProfile
from .serializers import UserProfileSerializer, BindSerializer


# Create your views here.
class UserProfileView(BaseModeView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        if self.action in ['me', 'create', 'update']:
            obj, _ = self.get_queryset().get_or_create(user=self.request.user)
        else:
            obj = super(UserProfileView, self).get_object()
        return obj

    def me(self, request, *args, **kwargs):
        """个人中心"""
        serializer = self.get_serializer(self.get_object())
        return SimpleResponse(serializer.data)

    def create(self, request, *args, **kwargs):
        """添加用户信息"""
        self.clean_data()
        return super(UserProfileView, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """修改用户信息"""
        self.clean_data()
        return super(UserProfileView, self).update(request, *args, **kwargs)

    def register(self):
        """用户注册"""


class BindPeopleView(BaseModeView):
    serializer_class = BindSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """绑定用户"""
        profile = self.get_object()
        if profile.people:
            request.data['people'] = profile.people
            return super(BindPeopleView, self).create(request, *args, **kwargs)
        return self.resp_failed('请先关联族谱')
