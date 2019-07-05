# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:46:18 2017

@author: SunJingyu
"""
from mechanics.python.Data import ExperimentData


def verification(file_path):
    try:
        experiment = ExperimentData(file_path)
        return True
    except:
        return False
