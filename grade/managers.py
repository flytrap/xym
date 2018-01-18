#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
from django.db.models.manager import Manager


class PeopleManager(Manager):
    def query_people(self, name):
        peoples = self.filter(name__icontains=name).select_related('grade')
        results = []
        # return [[people].extend(self.calc_parent_people(people)) for people in peoples]
        for people in peoples:
            li = self.calc_parent_people(people)
            # self.check_list(results, people, li)
            if li and isinstance(li[-1], list):
                results.append([people] + li[-1])
                del li[-1]
            if li and isinstance(li[-2], list):
                results.append([people] + li[-2])
                del li[-2]
            results.append([people] + li)
        return results

    def check_list(self, results, people, back_peoples: list):
        # results.extend([people] + back_peoples)
        for i, pp in enumerate(back_peoples[::-1]):
            if not pp:
                del back_peoples[back_peoples.index(pp)]
                continue
            if isinstance(pp, list):
                results.append(pp)
                del back_peoples[back_peoples.index(pp)]
                continue
            break
        return results

    def calc_parent_people(self, people):
        results = []
        if not people.master_name:
            return []
        # peoples = people.people_set.all().select_related('grade')
        peoples = self.filter(name=people.master_name).select_related('grade')
        for index, p in enumerate(peoples):
            back_peoples = self.calc_parent_people(p)
            if len(peoples) > 1 and index != 0:
                results.append([p] + back_peoples)
            else:
                results.extend([p] + back_peoples)
                self.check_list(results, p, back_peoples)
                # for i, pp in enumerate(back_peoples[::-1]):
                #     if isinstance(pp, list):
                #         results.append(back_peoples[len(back_peoples) - i - 1].insert(0, p))
                #         del back_peoples[i]
                #         continue
                #     break
        return results
