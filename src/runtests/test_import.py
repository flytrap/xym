#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created by flytrap
import sys, os, logging
from django.conf import settings
from django.test import TestCase
from grade.models import Grade, People

logger = logging.getLogger('test')


class ImportDataTestCase(TestCase):
    def setUp(self):
        if not People.objects.exists():
            logger.debug('import data')
            sys.path.insert(0, settings.BASE_DIR)
            from resources.script.import_data import ImportData
            ImportData.import_data(os.path.join(settings.BASE_DIR, 'resources', 'data', 'xym.pdf'))
            # self.peoples = People.objects.all()
            # self._next = 1
        self.first = People.objects.first()

    def test_first(self):
        p = People.objects.first()
        self.assertTrue(p.childes.exists())

    def test_peoples(self):
        for people in People.objects.all():
            self.check_people(people)
            # setattr(self, 'test_{}'.format(people.id), functools.partial(self.check_people(people)))

    def check_people(self, people: People):
        msg = '{}->{}'.format(people.id, people.name)
        self.assertTrue(bool(people.name), msg)
        if people.name != self.first.name:
            self.assertTrue(bool(people.master_name), msg)
        self.assertIsNotNone(people.grade, msg)
        self.assertTrue(People.objects.filter(name=people.master_name).exists(), msg)
        # if people.childes.exists():
        #     for child in people.childes.all():
        #         self.assertEqual(child.master_name, people.name, '{}:child:{}'.format(msg, child.name))
