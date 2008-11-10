# -*- coding: utf-8 -*-
# 
#  __init__.py
#  kanji_test
#  
#  Created by Lars Yencken on 2008-10-24.
#  Copyright 2008 Lars Yencken. All rights reserved.
# 

"""
All aspects of user proficiency and error modeling.
"""

def build():
    import add_syllabus
    add_syllabus.add_all_syllabi()
