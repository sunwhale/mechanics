# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:46:18 2017

@author: SunJingyu
"""
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os


# ==============================================================================
# PlotData
# ==============================================================================
class PlotData:
    """
    Define a data structure for plot.
    
    lines = [{line1},{line2},...]
    
    Example:
    
    life_NASA = [33,35,200,515,830,1072,1785,1850,2868,4323,8903,13332,13762]
    strain_amplitude_NASA = [1.75,1.75,0.85,0.85,0.575,0.5,0.507,0.575,0.398,0.402,0.329,0.323,0.328] # %
    stess_amplitude_NASA = [873.5,873.5,726.6,726.6,636.8,601,605,636.8,538,541,480,474,479] # MPa
    
    life_BHU = [100000,48745,50900,35940,12980,6300,2220,678,515]
    strain_amplitude_BHU = [0.4,0.42,0.43,0.45,0.47,0.5,0.6,0.8,1.0] # %
    stess_amplitude_BHU = [621,638,607,606,653,646,749,756,779] # MPa
    
    plot_data = PlotData()
    plot_data.add_line(life_NASA,strain_amplitude_NASA)
    plot_data.add_line(life_BHU,strain_amplitude_BHU)
    """

    def __init__(self, figure_path=None, figure_name=None, save_types=[]):
        self.lines = []
        self.number_of_header_lines = 15
        self.figure_path = figure_path
        self.figure_name = figure_name
        self.save_types = save_types

    def set_figure_file(self, figure_path=None, figure_name=None, save_types=[]):
        if figure_path is not None:
            self.figure_path = figure_path
        if figure_name is not None:
            self.figure_name = figure_name
        if save_types is not None:
            self.save_types = save_types

    def add_line(self,
                 x,
                 y,
                 xlabel='xlabel',
                 ylabel='ylabel',
                 linelabel='',
                 linestyle='',
                 linewidth=2,
                 marker=None,
                 markersize=12,
                 color='auto',
                 skip=1,
                 log_skip=1,
                 markerfacecolor='auto',
                 markeredgecolor='auto',
                 markeredgewidth=''):

        self.lines.append({'x': x,
                           'y': y,
                           'xlabel': xlabel,
                           'ylabel': ylabel,
                           'linelabel': linelabel,
                           'linestyle': linestyle,
                           'linewidth': linewidth,
                           'marker': marker,
                           'markersize': markersize,
                           'color': color,
                           'skip': skip,
                           'log_skip': log_skip,
                           'markerfacecolor': markerfacecolor,
                           'markeredgecolor': markeredgecolor,
                           'markeredgewidth': markeredgewidth})

    def plot_line(self, line):
        skip = int(line['skip'])
        log_skip = int(line['log_skip'])
        x = []
        y = []
        if log_skip == 1:
            x = line['x'][::skip]
            y = line['y'][::skip]
        else:
            x.append(line['x'][0])
            y.append(line['y'][0])
            for i in range(1, len(line['x']) - 1):
                if int(math.log(i, log_skip)) == math.log(i, log_skip):
                    x.append(line['x'][i])
                    y.append(line['y'][i])
        #            x.append(line['x'][-1])
        #            y.append(line['y'][-1])
        if line['color'] == 'auto':
            plt.plot(x,
                     y,
                     label=line['linelabel'],
                     linestyle=line['linestyle'],
                     linewidth=line['linewidth'],
                     marker=line['marker'],
                     markersize=line['markersize'],
                     markerfacecolor=line['markerfacecolor'],
                     markeredgecolor=line['markeredgecolor'],
                     markeredgewidth=line['markeredgewidth'])
        else:
            plt.plot(x,
                     y,
                     label=line['linelabel'],
                     linestyle=line['linestyle'],
                     linewidth=line['linewidth'],
                     marker=line['marker'],
                     markersize=line['markersize'],
                     color=line['color'],
                     markerfacecolor=line['markerfacecolor'],
                     markeredgecolor=line['markeredgecolor'],
                     markeredgewidth=line['markeredgewidth'])

    def plot(self, line_index=[]):
        if line_index == []:
            for line in self.lines:
                plt.xlabel(line['xlabel'])
                plt.ylabel(line['ylabel'])
                self.plot_line(line)
        else:
            for i in line_index:
                line = self.lines[i]
                plt.xlabel(line['xlabel'])
                plt.ylabel(line['ylabel'])
                self.plot_line(line)

    def write_to_file(self, dirname=None, filename=None):
        if dirname is None and filename is None:
            dirname = self.figure_path
            filename = self.figure_name
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
            print('Create new dirname:', dirname)
        basename = filename + '.csv'
        absname = os.path.join(dirname, basename)
        resultfile = open(absname, 'w')  # write to csv
        data_list = []
        for line in self.lines:
            xarray = []
            xarray.append('x')
            xarray.append(line['xlabel'])
            xarray.append(line['linelabel'])
            xarray.append(line['linestyle'])
            xarray.append(line['linewidth'])
            xarray.append(line['marker'])
            xarray.append(line['markersize'])
            xarray.append(line['color'])
            xarray.append(line['skip'])
            xarray.append(line['log_skip'])
            xarray.append(line['markerfacecolor'])
            xarray.append(line['markeredgecolor'])
            xarray.append(line['markeredgewidth'])
            for i in range(len(xarray), self.number_of_header_lines):
                xarray.append('')
            for x in line['x']:
                xarray.append(x)
            data_list.append(xarray)

            yarray = []
            yarray.append('y')
            yarray.append(line['ylabel'])
            yarray.append(line['linelabel'])
            yarray.append(line['linestyle'])
            yarray.append(line['linewidth'])
            yarray.append(line['marker'])
            yarray.append(line['markersize'])
            yarray.append(line['color'])
            yarray.append(line['skip'])
            yarray.append(line['log_skip'])
            yarray.append(line['markerfacecolor'])
            yarray.append(line['markeredgecolor'])
            yarray.append(line['markeredgewidth'])
            for i in range(len(yarray), self.number_of_header_lines):
                yarray.append('')
            for y in line['y']:
                yarray.append(y)
            data_list.append(yarray)

        data_length_list = []
        for data in data_list:
            data_length_list.append(len(data))
        data_length_max = max(data_length_list)
        data_height = len(data_list)

        for i in range(data_length_max):
            l = ''
            for j in range(data_height):
                if i < data_length_list[j]:
                    l += '%s,' % str(data_list[j][i])
                else:
                    l += '%s,' % ''
            print >> resultfile, l[:-1]

        resultfile.close()
        print('save as', dirname + filename + '.csv')

    def read_from_file(self, dirname=None, filename=None):
        if dirname is None and filename is None:
            dirname = self.figure_path
            filename = self.figure_name
        self.lines = []
        basename = filename + '.csv'
        absname = os.path.join(dirname, basename)
        data = np.genfromtxt(absname, delimiter=',', skip_header=0, dtype=str)  # read from csv
        data = data.transpose()
        data_item_list = []
        for d in data:
            data_item_list.append(d[0])
        data_item = np.array(data_item_list)
        data_item_index = np.where(data_item == 'x')[0]
        for i in data_item_index:
            x_index = i
            y_index = i + 1
            x_data = data[x_index]
            y_data = data[y_index]
            x = [float(x) for x in x_data[self.number_of_header_lines:] if x != '']
            y = [float(y) for y in y_data[self.number_of_header_lines:] if y != '']
            xlabel = x_data[1]
            ylabel = y_data[1]
            linelabel = x_data[2]
            linestyle = x_data[3]
            linewidth = float(x_data[4])
            marker = x_data[5]
            markersize = int(x_data[6])
            color = x_data[7]

            if x_data[8] != '':
                skip = x_data[8]
            else:
                skip = 1

            if x_data[9] != '':
                log_skip = x_data[9]
            else:
                log_skip = 1

            if x_data[10] != '':
                markerfacecolor = x_data[10]
            else:
                markerfacecolor = 'auto'

            if x_data[11] != '':
                markeredgecolor = x_data[11]
            else:
                markeredgecolor = 'auto'

            if x_data[12] != '':
                markeredgewidth = x_data[12]
            else:
                markeredgewidth = 1

            self.lines.append({'x': x,
                               'y': y,
                               'xlabel': xlabel,
                               'ylabel': ylabel,
                               'linelabel': linelabel,
                               'linestyle': linestyle,
                               'linewidth': linewidth,
                               'marker': marker,
                               'markersize': markersize,
                               'color': color,
                               'skip': skip,
                               'log_skip': log_skip,
                               'markerfacecolor': markerfacecolor,
                               'markeredgecolor': markeredgecolor,
                               'markeredgewidth': markeredgewidth})

    def save_figure(self, figure_path=None, figure_name=None, save_type=[]):
        if figure_path is None:
            figure_path = self.figure_path
        if figure_name is None:
            figure_name = self.figure_name
        if save_type is []:
            save_types = self.save_types
        if figure_path is not None and figure_name is not None:
            for save_type in save_types:
                plt.savefig(figure_path + figure_name + save_type, dpi=150, transparent=True)
                print('save as', figure_path + figure_name + save_type)


# ==============================================================================
# dictionary
# ==============================================================================
xylabels = {'axial_count': 'N [cycle]',
            'runing_time': 'Running Time [s]',
            'temperature':'Temperature [$^{\circ}$C]',
            # 'temperature': 'Temperature [K]',
            'axial_disp': 'Axial Displacement [mm]',
            'axial_force': 'Axial Force [N]',
            'axial_strain': 'Axial Strain $\\varepsilon$ [%]',
            'axial_stress': 'Axial Stress $\sigma$ [MPa]',
            'rotation': 'Rotation [$^{\circ}$]',
            'torque': 'Torque [N$\cdot$m]',
            'shear_strain': 'Engineering Shear Strain $\gamma$ [%]',
            'shear_stress': 'Shear Stress $\\tau$ [MPa]',
            'eqpl_strain': 'Equvialent Plastic Strain $p$]',
            'thermal_strain': 'Thermal Strain [%]',
            'total_strain': 'Total Strain [%]',
            'shear_stress_eq': 'Equvialent Shear Stress $\sqrt{3}\\tau$ [MPa]',
            'shear_strain_eq': 'Equvialent Shear Strain $\\gamma/\sqrt{3}$ [%]',
            'axial_log_strain': 'Axial Logarithmic Strain $\\varepsilon$ [%]',
            'axial_true_stress': 'Axial True Stress $\sigma$ [MPa]',
            'axial_stress_amplitude': 'Axial Stress Amplitude $\Delta\sigma/2$ [MPa]',
            'axial_strain_amplitude': 'Axial Strain Amplitude $\Delta\\varepsilon/2$ [%]',
            'equivalent_strain_amplitude': 'Equivalent Strain Amplitude $\Delta\\varepsilon_{\\rm{ep}}/2$ [%]',
            'experimental_life': 'Experimental Fatigue Lifetime $N_{\\rm{f}}$',
            'predicted_life': 'Predicted Fatigue Lifetime $N_{\\rm{p}}$',
            'mean_stress': 'Mean Stress $\sigma_{\\rm m}$ [MPa]',
            }


# ==============================================================================
# predefined
# ==============================================================================
marker_list = ['s', 'o', '^', 'D', 'p', '<', '>', 'v', 'h', '8']
color_list = ['red', 'green', 'blue', 'cyan', 'magenta', 'black', 'yellow', 'orange', 'lightgreen']