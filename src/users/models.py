from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from grade.models import People

User = get_user_model()


# Create your models here.
class UserProfile(models.Model):
    SEX_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )
    user = models.OneToOneField(User, verbose_name="用户", on_delete=False)

    nick = models.CharField('昵称', max_length=32, default='')
    phone = models.CharField(u'手机号', max_length=25, blank=True, null=True, default='')
    sex = models.CharField('性别', choices=SEX_CHOICES, max_length=8, default="male")
    birth = models.DateField(u'生日', null=True, blank=True, auto_now_add=True)

    avatar = models.ImageField("头像", null=True, blank=True, upload_to='avatar')

    people = models.ForeignKey(People, on_delete=False, null=True, blank=True)
    info = models.TextField(verbose_name='个人简介', default='', null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} {}'.format(self.user_id, self.nick)
