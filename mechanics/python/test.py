# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:46:18 2017

@author: SunJingyu
"""
import os
import datetime
from mechanics.python.plot_data_template import plot, create_plot_data
from flask import current_app


figure_path = '/home/sunwhale/mechanics/uploads/data/'
figure_name = '7036_3_plot'

starttime = datetime.datetime.now()

create_plot_data(figure_path,figure_name)
plot(figure_path,figure_name,save_types=['.pdf','.png'])


endtime = datetime.datetime.now()
print (endtime - starttime).microseconds