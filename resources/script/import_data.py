#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '../../')
sys.path.insert(0, '../../src/')
print(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xym.settings')
application = get_wsgi_application()

from grade.models import People, Grade
from resources.script.cultural import ParserPdf


class ImportData:
    @classmethod
    def import_data(cls, pdf_path):
        People.objects.all().delete()
        parser = ParserPdf(pdf_path)
        parser.parser()
        print('parser ok')
        parent = None
        for k, lines in parser.grade_dict.items():
            for line in lines:
                if isinstance(line, str):
                    if isinstance(parent, People):
                        for p in parent.childes.all():
                            if p.name == parent.master_name:
                                parent.childes.remove(p)
                        parent.save()
                    parent = cls.get_create_people(line, k - 1)
                elif isinstance(line, list):
                    for name in line:
                        child = cls.get_create_people(name, k, parent)
                        if isinstance(parent, People):
                            parent.childes.add(child)

    @staticmethod
    def get_create_grade(num):
        """辈份"""
        title = '第 {} 代门人'.format(num)
        grade, _ = Grade.objects.get_or_create(code=int(num), title=title)
        return grade

    @classmethod
    def get_create_people(cls, name, num=None, parent=None):
        """门人有则获取，无则创建，标准是代和姓名"""
        master_name = parent.name if parent else ''
        if name == '':
            return
        # 获取门人条件
        get_data = {
            'name': name
        }
        # 附加信息，更新
        update_date = {
            'master_name': master_name,
        }
        new_name = None
        # 获得生卒时间，如果有
        if '［' in name or '[' in name:
            import re
            birth_death = re.search('\d{4}－\d{4}', name)
            if birth_death:
                update_date['birth_death'] = birth_death.group()
                new_name = name.split('［')[0].split('[')[0]
        # 出生地获取，如果有
        if len(name) > 4 and '〔' in name and '〕' in name:
            new_name2, address = name.replace('〕', '').split('〔')
            new_name = new_name if new_name else new_name2
            update_date['address'] = address
        # 与师傅关系获取，如果有
        if len(name) > 4 and '（' in name:
            new_name2 = name.replace('）', '').replace(')', '').split('（')[0].split('(')[0]
            new_name = new_name if new_name else new_name2
            update_date['desc'] = '{}之{}'.format(
                master_name, name.replace('）', '').replace(')', '').split('（')[-1].split('(')[-1])
        get_data['name'] = new_name if new_name else name
        get_data['name'] = get_data['name'].replace(' ', '').strip()

        if num:
            grade = cls.get_create_grade(num)
            get_data['grade'] = grade
        people, _ = People.objects.get_or_create(**get_data)
        for k, v in update_date.items():
            if v and not getattr(people, k):
                setattr(people, k, v)
        if parent and not people.parents.filter(id=parent.id).exists():
            people.parents.add(parent)
        people.save()
        return people


if __name__ == '__main__':
    file_path = sys.argv[-1]
    if os.path.isfile(file_path):
        file_path = '/Users/flytrap/code/github/xym/people/xym.pdf'
        ImportData.import_data(file_path)
    else:
        print('file not found')
