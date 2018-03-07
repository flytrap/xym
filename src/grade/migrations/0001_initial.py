# Generated by Django 2.0.2 on 2018-02-22 10:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=32, verbose_name='辈份')),
                ('code', models.IntegerField(unique=True, verbose_name='辈份代码')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '辈份',
                'verbose_name_plural': '辈份',
            },
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master_name', models.CharField(default='', max_length=64, verbose_name='师承于')),
                ('birth_death', models.CharField(default='', max_length=32, verbose_name='生卒')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('address', models.CharField(default='', max_length=256, verbose_name='地址')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='介绍')),
                ('childes', models.ManyToManyField(related_name='child', to='grade.People', verbose_name='弟子')),
                ('grade', models.ForeignKey(blank=True, null=True, on_delete=False, to='grade.Grade', verbose_name='辈份')),
                ('parents', models.ManyToManyField(related_name='parent', to='grade.People', verbose_name='师父')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=False, to=settings.AUTH_USER_MODEL, verbose_name='系统关联')),
            ],
            options={
                'verbose_name': '传人',
                'verbose_name_plural': '传人',
            },
        ),
    ]