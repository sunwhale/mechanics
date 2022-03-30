# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:46:18 2017

@author: SunJingyu
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import re
import os
import pandas as pd


# ==============================================================================
# ExperimentData
# ==============================================================================
class ExperimentData:
    """
    Read and analyze experiment data.
    """

    def __init__(self, filename):
        """
        读取csv文件，表头和单位如下：
        
        ['Axial Segment Count' 'Running Time' 'Temperature' 'Axial Displacement'
         'Axial Force' 'Axial Strain' 'Axial Stress' 'Rotation' 'Torque'
         'Angle Strain' 'Shear Stress' 'Equivalent Plastic Strain' 'Thermal Strain'
         'Axial Total Strain']
         
        ['cycle' 'sec' 'C' 'mm' 'N' 'mm/mm' 'MPa' 'deg' 'N*m' '-' 'MPa' '-'
         'mm/mm' 'mm/mm']
        """

        df = pd.read_csv(filename, header=[0, 1])

        self.filename = filename
        self.node_label = [36]  # 试验对应的有限元模型节点为36号
        self.header = [column[0] for column in df]
        self.unit = [column[1] for column in df]

        self.axial_count = np.array(df.iloc[:, 0])
        self.running_time = np.array(df.iloc[:, 1])
        self.temperature = np.array(df.iloc[:, 2])
        self.axial_disp = np.array(df.iloc[:, 3])
        self.axial_force = np.array(df.iloc[:, 4])
        self.axial_strain = np.array(df.iloc[:, 5])
        self.axial_stress = np.array(df.iloc[:, 6])
        self.rotation = np.array(df.iloc[:, 7])
        self.torque = np.array(df.iloc[:, 8])
        self.shear_strain = np.array(df.iloc[:, 9])
        self.shear_stress = np.array(df.iloc[:, 10])
        self.eqpl_strain = np.array(df.iloc[:, 11])
        self.thermal_strain = np.array(df.iloc[:, 12])
        self.total_strain = np.array(df.iloc[:, 13])
        del df

        self.shear_stress_eq = self.shear_stress * np.sqrt(3.0)
        self.shear_strain_eq = self.shear_strain / np.sqrt(3.0)
        self.axial_log_strain = np.log(1.0 + self.axial_strain)
        self.axial_true_stress = self.axial_stress * (1.0 + self.axial_strain)

        self.item_list = [
            'nodelabel',
            'axial_count',
            'running_time',
            'temperature',
            'axial_disp',
            'axial_force',
            'axial_strain',
            'axial_stress',
            'rotation',
            'torque',
            'shear_strain',
            'shear_stress',
            'eqpl_strain',
            'thermal_strain',
            'total_strain',
            'shear_stress_eq',
            'shear_strain_eq',
            'axial_log_strain',
            'axial_true_stress',
        ]

        # 数组长度
        self.length = len(self.axial_count)
        # 总试验时间
        self.total_running_time = self.running_time[-1]
        # 总循环数
        self.total_axial_count = int(self.axial_count[-1])
        # 初始半疲劳寿命
        self.half_life_cycle = 0
        # 初始温度
        self.initial_temperature = self.temperature[0]

        self.axial_count_index_list = []
        self.axial_count_begin_index = {}
        self.axial_count_end_index = {}

        self.obtain_count_index()

    def obtain_count_index(self):
        """
        建立每个循环开始位置的索引表：axial_count_begin_index。
        建立每个循环结束位置的索引表：axial_count_end_index。
        计算半疲劳寿命：half_life_cycle。
        """
        self.axial_count_begin_index = {}
        self.axial_count_end_index = {}
        self.axial_count_begin_index[0] = 0
        self.axial_count_begin_index[int(self.axial_count[0])] = 0
        for i in range(self.length - 1):
            if int(self.axial_count[i]) != int(self.axial_count[i + 1]):  # 如果当前行计数与下一行计数不同
                self.axial_count_end_index[int(self.axial_count[i])] = i  # 当前循环结尾为i-1,这里用i,因为[a:b]中截取a到b-1
                self.axial_count_begin_index[int(self.axial_count[i + 1])] = i  # 下一循环的开头为i
        self.axial_count_index_list = list(self.axial_count_begin_index.keys())  # 所有存在的循环列表
        self.axial_count_index_list.sort()
        for c in self.axial_count_index_list:
            if abs(c - int(self.total_axial_count / 2.0)) <= abs(
                    self.half_life_cycle - int(self.total_axial_count / 2.0)):
                self.half_life_cycle = c

    def obtain_nth_cycle(self, item, begin_cycle, end_cycle=None):
        """
        截取指定数组的第begin_cycle到end_cycle循环中的数据。
        """
        if item in self.item_list:
            if end_cycle is None:
                end_cycle = begin_cycle
            if self.total_axial_count == []:
                print('self.total_axial_count is empty.')
                return []
            if self.axial_count_begin_index.has_key(begin_cycle) and self.axial_count_end_index.has_key(end_cycle):
                return eval('self.' + item)[
                       self.axial_count_begin_index[begin_cycle]:self.axial_count_end_index[end_cycle]]
            else:
                return []
        else:
            return []

    def obtain_item(self, item):
        """
        截取指定数组的第begin_cycle到end_cycle循环中的数据。
        """
        if item in self.item_list:
            return eval('self.' + item)
        else:
            return []

    def obtain_peak_valley(self, item):
        """
        返回指定数组的峰谷值。
        """
        cycle = []
        peak = []
        valley = []
        for n in self.axial_count_index_list:
            data_nth_cycle = self.obtain_nth_cycle(item, n)
            if data_nth_cycle != []:
                maxitem = max(data_nth_cycle)
                minitem = min(data_nth_cycle)
                cycle.append(n)
                peak.append(maxitem)
                valley.append(minitem)
        return cycle, peak, valley

    def update_strain(self, period, strain_pv_list):
        strain_mean = (strain_pv_list[0] + strain_pv_list[1]) / 2.0
        strain_min = min(strain_pv_list)
        strain_max = max(strain_pv_list)
        time_list = [0, period / 4.0, period / 2.0, period / 4.0 * 3.0, period]
        strain_list = [strain_mean, strain_max, strain_mean, strain_min, strain_mean]

        outfile = open(self.filename, 'w')
        print('writing: ' + self.filename)
        print()
        outfile.writelines(
            'Axial Segment Count,Running Time,Temperature,Axial Displacement,Axial Force,Axial Strain,Axial Stress,Rotation,Torque,Angle Strain,Shear Stress,Equivalent Plastic Strain,Thermal Strain,Axial Total Strain\n')
        outfile.writelines('cycle,sec,C,mm,N,mm/mm,MPa,deg,N*m,-,MPa,-,mm/mm,mm/mm\n')

        for i, time in enumerate(self.running_time[:]):
            local_time = (time - self.running_time[self.axial_count_begin_index[self.axial_count[i]]]) % period
            time_list_tmp = time_list + [local_time]
            time_list_tmp.sort()
            point_front = time_list_tmp.index(local_time) - 1
            point_after = point_front + 1
            x = [time_list[point_front], time_list[point_after]]
            y = [strain_list[point_front], strain_list[point_after]]
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            self.axial_strain[i] = p(local_time)

            line = ''
            line += '%s,' % (self.axial_count[i])
            line += '%s,' % (self.running_time[i])
            line += '%s,' % (self.temperature[i])
            line += '%s,' % (self.axial_disp[i])
            line += '%s,' % (self.axial_force[i])
            line += '%s,' % (self.axial_strain[i])
            line += '%s,' % (self.axial_stress[i])
            line += '%s,' % (self.rotation[i])
            line += '%s,' % (self.torque[i])
            line += '%s,' % (self.shear_strain[i])
            line += '%s,' % (self.shear_stress[i])
            line += '%s,' % (self.eqpl_strain[i])
            line += '%s,' % (self.thermal_strain[i])
            line += '%s,' % (self.total_strain[i])

            print >> outfile, line[:-1]

        outfile.close()

    def update_stress(self):
        outfile = open(self.filename, 'w')
        print('writing: ' + self.filename)
        print()
        outfile.writelines(
            'Axial Segment Count,Running Time,Temperature,Axial Displacement,Axial Force,Axial Strain,Axial Stress,Rotation,Torque,Angle Strain,Shear Stress,Equivalent Plastic Strain,Thermal Strain,Axial Total Strain\n')
        outfile.writelines('cycle,sec,C,mm,N,mm/mm,MPa,deg,N*m,-,MPa,-,mm/mm,mm/mm\n')

        for i, time in enumerate(self.running_time[:]):
            add_stress = (self.axial_count[i]) ** 0.55 * 2.9
            print(add_stress)
            self.axial_stress[i] += add_stress - 20

            line = ''
            line += '%s,' % (self.axial_count[i])
            line += '%s,' % (self.running_time[i])
            line += '%s,' % (self.temperature[i])
            line += '%s,' % (self.axial_disp[i])
            line += '%s,' % (self.axial_force[i])
            line += '%s,' % (self.axial_strain[i])
            line += '%s,' % (self.axial_stress[i])
            line += '%s,' % (self.rotation[i])
            line += '%s,' % (self.torque[i])
            line += '%s,' % (self.shear_strain[i])
            line += '%s,' % (self.shear_stress[i])
            line += '%s,' % (self.eqpl_strain[i])
            line += '%s,' % (self.thermal_strain[i])
            line += '%s,' % (self.total_strain[i])

            print >> outfile, line[:-1]

        outfile.close()


# ==============================================================================
# SimulationData
# ==============================================================================
class SimulationData:
    """
    Read and analyze simulation data.
    """

    def __init__(self, filename, period):
        data = np.genfromtxt(filename, delimiter=',', skip_header=0, dtype=None)
        self.header = [i for i in data[0]]
        del data

        data = np.genfromtxt(filename, delimiter=',', skip_header=1, dtype=float)
        self.filename = filename
        self.axial_count = []
        self.frame = []
        self.running_time = []
        self.node_label = []
        self.temperature = []
        self.axial_strain = []
        self.axial_stress = []
        self.shear_strain = []
        self.shear_stress = []
        self.mises_stress = []
        self.heat_flux_1 = []
        self.heat_flux_2 = []
        self.heat_flux_3 = []
        self.axial_count_index = {}
        self.axial_count_index_list = []
        self.total_axial_count = []
        self.item_list = ['axial_count',
                          'frame',
                          'running_time',
                          'node_label',
                          'temperature',
                          'axial_strain',
                          'axial_stress',
                          'shear_strain',
                          'shear_stress',
                          'mises_stress',
                          'heat_flux_1',
                          'heat_flux_2',
                          'heat_flux_3']

        for h in self.header:
            if h in ['Frame']:
                self.frame = data[:, self.header.index(h)]
            if h in ['Time']:
                self.running_time = data[:, self.header.index(h)]
            if h in ['NodeLabel']:
                self.node_label = data[:, self.header.index(h)]
            if h in ['Temperature']:
                self.temperature = data[:, self.header.index(h)]
            if h in ['LE22', 'E22', 'E33']:
                self.axial_strain = data[:, self.header.index(h)]
            if h in ['S22', 'S33']:
                self.axial_stress = data[:, self.header.index(h)]
            if h in ['LE23', 'E23']:
                self.shear_strain = data[:, self.header.index(h)]
            if h in ['S23']:
                self.shear_stress = data[:, self.header.index(h)]
            if h in ['Mises']:
                self.mises_stress = data[:, self.header.index(h)]
            if h in ['HFL1']:
                self.heat_flux_1 = data[:, self.header.index(h)]
            if h in ['HFL2']:
                self.heat_flux_2 = data[:, self.header.index(h)]
            if h in ['HFL3']:
                self.heat_flux_3 = data[:, self.header.index(h)]
        del data

        self.length = len(self.running_time)
        self.axial_count = np.zeros(self.length)

        self.obtain_count_index(period)

    def obtain_count_index(self, period):
        """
        建立每个循环开始位置的索引表：axial_count_index。
        """
        self.total_axial_count = int(self.running_time[-1] / period)
        self.axial_count_index = {}
        self.axial_count_index[0] = 0
        self.axial_count_index[1] = 0
        count = 1
        for i in range(self.length):
            if self.running_time[i] <= count * period and self.running_time[i] >= (count - 1) * period:
                self.axial_count[i] = count
            if self.running_time[i] > count * period:
                count = int(self.running_time[i] / period) + 1
                self.axial_count_index[count] = i
        self.axial_count_index_list = list(self.axial_count_index.keys())
        self.half_life_cycle = self.axial_count_index_list[-2]

    def obtain_nth_cycle(self, item, begin_cycle, end_cycle=None):
        """
        截取指定数组的第begin_cycle到end_cycle循环中的数据。
        """
        if item in self.item_list:
            if end_cycle is None:
                end_cycle = begin_cycle
            if self.total_axial_count == []:
                print('self.total_axial_count is empty.')
            if self.axial_count_index.has_key(begin_cycle) and self.axial_count_index.has_key(end_cycle + 1):
                return eval('self.' + item)[self.axial_count_index[begin_cycle]:self.axial_count_index[end_cycle + 1]]
        else:
            return []

    def obtain_peak_valley(self, item):
        """
        返回指定数组的峰谷值。
        """
        cycle = []
        peak = []
        valley = []
        for n in range(1, self.total_axial_count):
            data_nth_cycle = self.obtain_nth_cycle(item, n)
            if data_nth_cycle != []:
                maxitem = max(data_nth_cycle)
                minitem = min(data_nth_cycle)
                cycle.append(n)
                peak.append(maxitem)
                valley.append(minitem)
        return cycle, peak, valley


# ==============================================================================
# SimulationData 3D
# ==============================================================================
class SimulationData3D:
    """
    Read and analyze simulation data.
    """

    def __init__(self, filename, period):
        data = np.genfromtxt(filename, delimiter=',', skip_header=0, dtype=None)
        self.header = [i for i in data[0]]
        del data

        data = np.genfromtxt(filename, delimiter=',', skip_header=1, dtype=float)
        self.filename = filename
        self.axial_count = []
        self.frame = []
        self.running_time = []
        self.node_label = []
        self.temperature = []
        self.s11 = []
        self.s22 = []
        self.s33 = []
        self.s12 = []
        self.s13 = []
        self.s23 = []
        self.e11 = []
        self.e22 = []
        self.e33 = []
        self.e12 = []
        self.e13 = []
        self.e23 = []
        self.mises_stress = []
        self.heat_flux_1 = []
        self.heat_flux_2 = []
        self.heat_flux_3 = []
        self.axial_count_index = {}
        self.axial_count_index_list = []
        self.total_axial_count = []
        self.item_list = ['axial_count',
                          'frame',
                          'running_time',
                          'node_label',
                          'temperature',
                          's11',
                          's22',
                          's33',
                          's12',
                          's13',
                          's23',
                          'e11',
                          'e22',
                          'e33',
                          'e12',
                          'e13',
                          'e23',
                          'mises_stress',
                          'heat_flux_1',
                          'heat_flux_2',
                          'heat_flux_3']

        for h in self.header:
            if h in ['Frame']:
                self.frame = data[:, self.header.index(h)]
            if h in ['Time']:
                self.running_time = data[:, self.header.index(h)]
            if h in ['NodeLabel']:
                self.node_label = data[:, self.header.index(h)]
            if h in ['Temperature']:
                self.temperature = data[:, self.header.index(h)]
            if h in ['LE11', 'E11']:
                self.e11 = data[:, self.header.index(h)]
            if h in ['LE22', 'E22']:
                self.e22 = data[:, self.header.index(h)]
            if h in ['LE33', 'E33']:
                self.e33 = data[:, self.header.index(h)]
            if h in ['LE12', 'E12']:
                self.e12 = data[:, self.header.index(h)]
            if h in ['LE13', 'E13']:
                self.e13 = data[:, self.header.index(h)]
            if h in ['LE23', 'E23']:
                self.e23 = data[:, self.header.index(h)]
            if h in ['S11']:
                self.s11 = data[:, self.header.index(h)]
            if h in ['S22']:
                self.s22 = data[:, self.header.index(h)]
            if h in ['S33']:
                self.s33 = data[:, self.header.index(h)]
            if h in ['S12']:
                self.s12 = data[:, self.header.index(h)]
            if h in ['S13']:
                self.s13 = data[:, self.header.index(h)]
            if h in ['S23']:
                self.s23 = data[:, self.header.index(h)]
            if h in ['Mises']:
                self.mises_stress = data[:, self.header.index(h)]
            if h in ['HFL1']:
                self.heat_flux_1 = data[:, self.header.index(h)]
            if h in ['HFL2']:
                self.heat_flux_2 = data[:, self.header.index(h)]
            if h in ['HFL3']:
                self.heat_flux_3 = data[:, self.header.index(h)]
        del data

        self.length = len(self.running_time)
        self.axial_count = np.zeros(self.length)

        self.obtain_count_index(period)

    def obtain_count_index(self, period):
        """
        建立每个循环开始位置的索引表：axial_count_index。
        """
        self.total_axial_count = int(self.running_time[-1] / period)
        self.axial_count_index = {}
        self.axial_count_index[0] = 0
        self.axial_count_index[1] = 0
        count = 1
        for i in range(self.length):
            if self.running_time[i] <= count * period and self.running_time[i] >= (count - 1) * period:
                self.axial_count[i] = count
            if self.running_time[i] > count * period:
                count = int(self.running_time[i] / period) + 1
                self.axial_count_index[count] = i
        self.axial_count_index_list = list(self.axial_count_index.keys())
        self.half_life_cycle = self.axial_count_index_list[-2]

    def obtain_nth_cycle(self, item, begin_cycle, end_cycle=None):
        """
        截取指定数组的第begin_cycle到end_cycle循环中的数据。
        """
        if item in self.item_list:
            if end_cycle is None:
                end_cycle = begin_cycle
            if self.total_axial_count == []:
                print('self.total_axial_count is empty.')
            if self.axial_count_index.has_key(begin_cycle) and self.axial_count_index.has_key(end_cycle + 1):
                return eval('self.' + item)[self.axial_count_index[begin_cycle]:self.axial_count_index[end_cycle + 1]]
        else:
            return []

    def obtain_peak_valley(self, item):
        """
        返回指定数组的峰谷值。
        """
        cycle = []
        peak = []
        valley = []
        for n in range(1, self.total_axial_count):
            data_nth_cycle = self.obtain_nth_cycle(item, n)
            if data_nth_cycle != []:
                maxitem = max(data_nth_cycle)
                minitem = min(data_nth_cycle)
                cycle.append(n)
                peak.append(maxitem)
                valley.append(minitem)
        return cycle, peak, valley


# ==============================================================================
# ExperimentLog
# ==============================================================================
class ExperimentLog:
    """
    Read experiment log.
    """

    def __init__(self, filename):
        data = np.genfromtxt(filename, delimiter=',', skip_header=0, dtype=None)
        self.header = [i for i in data[0]]
        del data

        data = np.genfromtxt(filename, delimiter=',', skip_header=1, dtype=str)
        """
        ['number', 'din mm', 'dout mm', 'gauge length mm', 'load type', 'axial control mode', 
        'rotational control mode', 'temperature mode', 'axial displacement', 'axial strain %', 
        'axial force', 'rotation', 'angel strain deg', 'torque', 'equivalent strain %', 
        'axial rotational phase deg', 'axial temperature phase deg', 'Period', 
        'load rate or frequence', 'test date', 'comments', 'calculate']
        """

        self.number = data[:, 0]
        self.d_in = data[:, 1]
        self.d_out = data[:, 2]
        self.gauge_length = data[:, 3]
        self.load_type = data[:, 4]
        self.axial_control_mode = data[:, 5]
        self.rotational_control_mode = data[:, 6]
        self.temperature_mode = data[:, 7]
        self.axial_displacement = data[:, 8]
        self.axial_strain = data[:, 9]
        self.axial_force = data[:, 10]
        self.rotation = data[:, 11]
        self.angel_strain = data[:, 12]
        self.torque = data[:, 13]
        self.equivalent_strain = data[:, 14]
        self.axial_rotational_phase = data[:, 15]
        self.axial_temperature_phase = data[:, 16]
        self.period = data[:, 17]
        self.load_rate = data[:, 18]
        self.test_date = data[:, 19]
        self.comments = data[:, 20]
        self.calculate = data[:, 21]
        self.data = data
        self.length = len(self.number)

    def output(self, name):
        number = self.find(name)
        print('=========================Experiment=========================')
        for i in range(len(self.header)):
            print('%-40s%-20s' % (self.header[i], self.data[number][i]))

    def find(self, name):
        number = int(np.where(self.number == name)[0][0])
        return number

    def keyFilter(self, key):
        numbers = np.where(eval(key))[0]
        for number in numbers:
            self.find(self.number[number])
        number_list = []
        for number in numbers:
            number_list.append(self.number[number])
        return number_list

    def obtainItem(self, name, item, regular):
        """
        总结
        ^ 匹配字符串的开始。
        $ 匹配字符串的结尾。
        \b 匹配一个单词的边界。
        \d 匹配任意数字。
        \D 匹配任意非数字字符。
        x? 匹配一个可选的 x 字符 (换言之，它匹配 1 次或者 0 次 x 字符)。
        x* 匹配0次或者多次 x 字符。
        x+ 匹配1次或者多次 x 字符。
        x{n,m} 匹配 x 字符，至少 n 次，至多 m 次。
        (a|b|c) 要么匹配 a，要么匹配 b，要么匹配 c。
        (x) 一般情况下表示一个记忆组 (remembered group)。你可以利用 re.search 函数返回对象的 groups() 函数获取它的值。
        正则表达式中的点号通常意味着 “匹配任意单字符”
        """
        number = self.find(name)
        string = eval('self.%s[number]' % item)
        result_list = re.findall(regular, string)
        if len(result_list) == 0:
            return [0.0]
        elif len(result_list) >= 1:
            return result_list


# ==============================================================================
# FatigueData
# ==============================================================================
class FatigueData:
    """
    Read and analyze fatigue data.
    """

    def __init__(self, filename):
        """
        ['Number of Cycles to Failure N\\-(f)',
        'Mises Equivalent Strain Amplitude \\i(\\g(De))\\-(eq)/2',
        'Stress Amplitude e \\i(\\g(Ds))/2',
        'Specimen',
        'Critical Plane',
        'sigma_n_max',
        'delta_sigma', 
        'delta_epsilon',
        'tau_n_max',
        'delta_tau',
        'delta_gamma',
        'Predicted Fatigue Lifetime N\\-(p)', 
        'Fatigue Coefficient',
        'Temperature',
        'Load Type']
        """
        data = np.genfromtxt(filename, delimiter=',', skip_header=0, dtype=None)
        self.header = [i for i in data[0]]
        self.unit = [i for i in data[1]]
        del data

        data = np.genfromtxt(filename, delimiter=',', skip_header=2, dtype=float)
        self.experimental_life = data[:, 0]
        self.equivalent_strain_amplitude = data[:, 1]
        self.stress_amplitude = data[:, 2]
        self.specimen = data[:, 3]
        self.critical_plane = data[:, 4]
        self.sigma_n_max = data[:, 5]
        self.delta_sigma = data[:, 6]
        self.delta_epsilon = data[:, 7]
        self.tau_n_max = data[:, 8]
        self.delta_tau = data[:, 9]
        self.delta_gamma = data[:, 10]
        self.predicted_life = data[:, 11]
        self.fatigue_coefficient = data[:, 12]
        self.temperature = data[:, 13]
        del data

        data = np.genfromtxt(filename, delimiter=',', skip_header=2, dtype=str)
        for h in self.header:
            if h in ['Load Type']:
                self.load_type = data[:, self.header.index(h)]

        #        self.load_type = data[:,14]
        del data

    def loadTypeFilter(self, load_type, item):
        numbers = np.where(self.load_type == load_type)[0]
        result = []
        for number in numbers:
            result.append(eval('self.%s[number]' % item))
        return result

    def quantitativeTN(self):
        """
        \[\bar E = \frac{1}{n}\sum\limits_{i = 1}^n {\log \left( {\frac{{{N_{f,i}}}}{{{N_{p,i}}}}} \right)} \]
        """
        Nf = self.experimental_life
        Np = self.predicted_life
        n = len(Nf)
        E_bar = 0
        for i in range(n):
            E_bar += np.log(Nf[i] / Np[i])
        E_bar = E_bar / n

        TN = 10 ** E_bar
        return TN

    def quantitativeTRMS(self):
        """
        \[\bar E = \frac{1}{n}\sum\limits_{i = 1}^n {\log \left( {\frac{{{N_{f,i}}}}{{{N_{p,i}}}}} \right)} \]
        """
        Nf = self.experimental_life
        Np = self.predicted_life
        n = len(Nf)
        E_RMS = 0
        for i in range(n):
            E_RMS += np.log(Nf[i] / Np[i]) ** 2
        E_RMS = E_RMS / n

        TRMS = 10 ** E_RMS
        return TRMS