#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
import copy
from django.db.models.manager import Manager


class PeopleManager(Manager):
    def query_people(self, name):
        """
        模糊匹配门人
        :param name:
        :return:
        """
        peoples = self.filter(name__icontains=name).select_related('grade')
        results = []
        for people in peoples:
            li = []
            self.get_parent(people, li)
            results.extend(self.split_people(li, people))
        return results

    def get_parent(self, people, childes: list):
        """
        获取父节点，递归至顶级
        :param people:
        :param childes:
        :return:
        """
        parents = people.parents.all()
        old_childes = None
        for index, p in enumerate(parents):
            if parents.count() > 1 and index == 0:
                old_childes = copy.deepcopy(childes)
            if index != 0 and old_childes is not None:
                tmp_childes = copy.deepcopy(old_childes)
                childes.insert(0, tmp_childes)
                childes = tmp_childes
            childes.append(p)
            self.get_parent(p, childes)

    @classmethod
    def split_people(cls, peoples: list, p):
        """
        拆分处理
        :param peoples:
        :param p:
        :return:
        """
        results = cls.check_list(peoples)
        for li in results:
            li.insert(0, p)
        return results

    @classmethod
    def check_list(cls, peoples, results=None):
        if results is None:
            results = []
        li = []
        for p in peoples:
            if isinstance(p, list):
                cls.check_list(p, results)
                continue
            li.append(p)
        results.append(li)
        return results


class GradeManager(Manager):
    def get_create_grade(self, num):
        """辈份"""
        title = '第 {} 代门人'.format(num)
        grade, _ = self.get_or_create(code=int(num), title=title)
        return grade
