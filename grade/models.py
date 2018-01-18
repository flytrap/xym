from django.contrib.auth import get_user_model
from django.db import models
from .managers import PeopleManager

# Create your models here.

User = get_user_model()


class Grade(models.Model):
    title = models.CharField('辈份', max_length=32, default='')
    code = models.IntegerField('辈份代码', unique=True)
    desc = models.TextField('描述', null=True, blank=True)

    class Meta:
        verbose_name = '辈份'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} {}'.format(self.id, self.title)


class People(models.Model):
    user = models.ForeignKey(User, verbose_name='系统关联', on_delete=False, null=True, blank=True)
    grade = models.ForeignKey(Grade, verbose_name='辈份', on_delete=False, null=True, blank=True)
    master_name = models.CharField('师承于', max_length=64, default='')
    birth_death = models.CharField('生卒', max_length=32, default='')
    name = models.CharField('姓名', max_length=64)
    address = models.CharField('地址', max_length=256, default='')
    desc = models.TextField('介绍', null=True, blank=True)

    childes = models.ManyToManyField('self', symmetrical=False, verbose_name='弟子')

    objects = PeopleManager()

    class Meta:
        verbose_name = '传人'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} {}'.format(self.id, self.name)
