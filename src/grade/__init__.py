from django.apps import AppConfig


class GradeConfig(AppConfig):
    name = 'grade'
    verbose_name = '门人管理'


default_app_config = 'grade.GradeConfig'
