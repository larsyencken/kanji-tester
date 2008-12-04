#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_basic_drills.py
#  kanji_test
# 
#  Created by Lars Yencken on 26-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

import unittest

from django.contrib.auth.models import User

from kanji_test.user_model import models
from kanji_test.plugins import basic_drills

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(ReadingQuestionTest),
            unittest.makeSuite(SurfaceQuestionTest),
        ))
    return testSuite

class ReadingQuestionTest(unittest.TestCase):
    def setUp(self):
        User.objects.filter(username='test_user').delete()
        test_user = User(username='test_user')
        test_user.save()
        self.user = test_user

        self.factory = basic_drills.ReadingQuestionFactory()

    def _init_syllabus(self, tag):
        self.syllabus = models.Syllabus.objects.get(tag=tag)
        self.user.userprofile_set.all().delete()
        self.user.errordist_set.all().delete()

        self.user.userprofile_set.create(syllabus=self.syllabus)
        models.ErrorDist.init_from_priors(self.user)

    def test_bug_339(self):
        "Kanji reading questions have only one correct answer."
        self._init_syllabus('jlpt 3')
        partial_kanji = models.PartialKanji.objects.get(kanji__kanji=u'家',
                syllabus=self.syllabus)
        real_readings = set(o.reading for o in \
                partial_kanji.kanji.reading_set.all())
        for i in xrange(100):
            question = self.factory.get_kanji_question(partial_kanji,
                    self.user)
            distractor_values = set(o.value for o in \
                    question.options.all() if not o.is_correct)
            correct_value = question.options.get(is_correct=True).value
            assert correct_value in real_readings
            self.assertEqual(
                    real_readings.intersection(distractor_values), set()
                )
            question.options.all().delete()
            question.delete()

    def tearDown(self):
        pass

class SurfaceQuestionTest(unittest.TestCase):
    def setUp(self):
        User.objects.filter(username='test_user').delete()
        test_user = User(username='test_user')
        test_user.save()
        self.syllabus = models.Syllabus.objects.get(tag='jlpt 4')
        test_user.userprofile_set.create(syllabus=self.syllabus)
        models.ErrorDist.init_from_priors(test_user)
        self.user = test_user

        self.factory = basic_drills.SurfaceQuestionFactory()

    def test_bug_325(self):
        partial_lexeme = models.PartialLexeme.objects.get(
                syllabus=self.syllabus,
                surface_set__surface=u'九つ',
                reading_set__reading=u'ここのつ',
            )
        
        # [325] an infinite loop here
        question = self.factory.get_question(partial_lexeme, self.user)

        # If we get here, it worked.
        question.options.all().delete()
        question.delete()
    
    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:
