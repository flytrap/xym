#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
import os
import sys
import re
import time

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '../../')
sys.path.insert(0, '../../src/')
print(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xym.settings')
application = get_wsgi_application()

from django.conf import settings
from django.core.cache import cache
from grade.models import People, Grade
from resources.script.cultural import ParserPdf


class ImportData(object):
    # 关键标记
    birth_death_tag = ['［', '］']
    nick_tag = ['〔', '〕']
    address_tag = ['＜', '＞']
    relate_tag = ['（', '）']
    all_tags = [birth_death_tag, nick_tag, address_tag, relate_tag]
    check_tags = list(zip(*all_tags))
    name_re = re.compile('.+?(?=[［|〔|＜|（$])')

    grads = {}  # 缓存备份, 减少数据库查询
    peoples = {}
    re_tags = {}

    @classmethod
    def get_re(cls, tags: list):
        """获取编译好的re对象"""
        key = str(tags)
        if key in cls.re_tags:
            return cls.re_tags.get(key)
        re_tag = re.compile('(?<={}).+(?={})'.format(*tags))
        cls.re_tags[key] = re_tag
        return re_tag

    @staticmethod
    def parser(pdf_path):
        data = cache.get('pdf_parser')
        if not data:
            People.objects.all().delete()
            parser = ParserPdf(pdf_path)
            parser.parser()
            data = parser.grade_dict
            cache.set('pdf_parser', data, 60 * 60 * 24)
        return data

    @classmethod
    def check_name(cls, text):
        """师父名字切分"""
        names = text.strip().split()
        if len(names) == 1:
            return names
        del_index = []
        flag = False
        for index, name in enumerate(names):
            if flag:
                flag = False
                continue
            for i, tag in enumerate(cls.check_tags[0]):
                if tag in name and cls.check_tags[1][i] not in name:
                    if cls.check_tags[1][i] in names[index + 1]:
                        # 正常情况下一定会有，所以先不判断
                        flag = True
                        names[index] += names[index + 1]
                        del_index.append(index + 1)
                    break
            if len(name) == 1:
                flag = True
                names[index] += names[index + 1]
                del_index.append(index + 1)
        for i in del_index[::-1]:
            del names[i]
        return names

    @classmethod
    def import_data(cls, pdf_path):
        data = cls.parser(pdf_path)
        print('parser ok')
        # parent = None
        parents = []
        parent_name = None
        for k, lines in data.items():
            for line in lines:
                if isinstance(line, str):
                    parent_name = line
                    names = cls.check_name(line)
                    parents = cls.get_create_peoples(names, None, k - 1)
                elif isinstance(line, list):
                    cls.get_create_peoples(line, parents, k, parent_name)

    @classmethod
    def get_create_grade(cls, num):
        """辈份"""
        if num in cls.grads:
            return cls.grads[num]
        title = '第 {} 代门人'.format(num)
        grade, _ = Grade.objects.get_or_create(code=int(num), title=title)
        cls.grads[num] = grade
        return grade

    @classmethod
    def get_create_people(cls, data: dict):
        key = str(data)
        if key in cls.peoples:
            return cls.peoples.get(key)
        people, created = People.objects.get_or_create(**data)
        cls.peoples[key] = people
        return people

    @staticmethod
    def fix_name(name):
        """修复一些有问题的名字"""
        if name == '侯丕列':
            return '侯丕烈'
        if '文森•布莱克' in name:
            return name.replace('文森•布莱克', '文森·布莱克')
        return name

    @classmethod
    def get_create_peoples(cls, names: list, parents=None, num=None, master_name=None):
        """批量创建数据"""
        names = filter(None, names)
        peoples = []
        for name in names:
            name = cls.fix_name(name.strip())
            get_data, update_data = cls.get_people_data(name, num, master_name)
            people = cls.get_create_people(get_data)
            cls.update_people(people, update_data)
            if parents:
                people.parents.add(*parents)
            peoples.append(people)
        if parents:
            for parent in parents:
                parent.childes.add(*peoples)
        return peoples

    @classmethod
    def update_people(cls, people, data):
        """更新数据，如果有更新则保存"""
        must_save = False
        for k, v in data.items():
            if v and not getattr(people, k):
                setattr(people, k, v)
                must_save = True
        if must_save:
            people.save()

    @classmethod
    def get_people_data(cls, name, num=None, master_name=None):
        """传承人信息解析"""
        # 获取门人条件
        get_data = {
            'name': name
        }
        # 附加信息，更新
        update_data = {
            'master_name': master_name,
        }
        cls.get_birth_death(update_data, name)
        cls.get_nick(update_data, name)
        cls.get_relate(update_data, master_name, name)
        cls.get_address(update_data, name)
        new_name = cls.get_name(name)

        get_data['name'] = new_name if new_name else name
        get_data['name'] = get_data['name'].replace(' ', '').strip()

        if num:
            get_data['grade'] = cls.get_create_grade(num)
        return get_data, update_data

    @classmethod
    def get_name(cls, text):
        """匹配名字"""
        result = cls.name_re.search(text)
        if result:
            name: str = result.group()
            for tag in cls.all_tags:
                name = name.replace(tag[1], '').strip()
            return name

    @classmethod
    def get_nick(cls, target: dict, name):
        # 称号获取，如果有
        result = cls.get_re(cls.nick_tag).search(name)
        if result:
            nicks = result.group().replace(cls.nick_tag[1], '').split(cls.nick_tag[0])
            cls.add_value(target, '称号：' + ','.join(nicks))

    @classmethod
    def get_relate(cls, target: dict, master_name, name):
        # 与师傅关系获取，如果有
        result = cls.get_re(cls.relate_tag).search(name)
        if result:
            cls.add_value(target, '{}之{}'.format(master_name, result.group()))

    @classmethod
    def get_birth_death(cls, target: dict, name):
        # 获得生卒时间，如果有
        result = cls.get_re(cls.birth_death_tag).search(name)
        if result:
            target['birth_death'] = result.group()

    @classmethod
    def get_address(cls, target: dict, name):
        # 地理位置,如果有
        result = cls.get_re(cls.address_tag).search(name)
        if result:
            target['address'] = result.group()

    @staticmethod
    def add_value(target: dict, text, key='desc'):
        if target.get(key):
            target[key] += ';'.join([target[key], text])
        else:
            target[key] = text


if __name__ == '__main__':
    file_path = sys.argv[-1]
    if not os.path.isfile(file_path) or len(sys.argv) < 2:
        file_path = os.path.join(settings.BASE_DIR, 'resources', 'data', 'xym.pdf')
    People.objects.all().delete()
    t = time.time()
    ImportData.import_data(file_path)
    print(time.time() - t)
