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
            if index != 0 and old_childes:
                tmp_childes = copy.deepcopy(old_childes)
                childes.insert(0, tmp_childes)
                childes = tmp_childes
            childes.append(p)
            self.get_parent(p, childes)

    @staticmethod
    def split_people(peoples: list, p):
        """
        拆分处理
        :param peoples:
        :param p:
        :return:
        """
        results = []
        li_index = []
        for index, people in enumerate(peoples):
            if isinstance(people, list):
                people.insert(0, p)
                results.append(people)
                li_index.append(index)
                continue
            break
        for i in li_index[::-1]:
            del peoples[i]
        results.append(peoples)
        peoples.insert(0, p)
        return results
