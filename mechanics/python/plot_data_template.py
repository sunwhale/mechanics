# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 11:50:47 2017

@author: j.Sun
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter, FormatStrFormatter
from mechanics.python.PlotData import PlotData, xylabels, marker_list, color_list
from mechanics.python.Data import ExperimentData
from mechanics.python.plot_format import plot_format


def create_plot_data(figure_dirname=None, figure_filename=None, datafile_absname=None, x_item='axial_strain', y_item='axial_stress'):
    # ==============================================================================
    # x,y label
    # ==============================================================================
    xlabel = xylabels[x_item]
    ylabel = xylabels[y_item]
    # ==============================================================================
    # plot lines
    # ==============================================================================
    i = 0
    plot_data = PlotData()
    exp = ExperimentData(datafile_absname)
    x = exp.obtain_item(x_item)
    y = exp.obtain_item(y_item)

    plot_data.add_line(x,
                       y,
                       xlabel=xlabel,
                       ylabel=ylabel,
                       linelabel='',
                       linewidth=2,
                       linestyle='-',
                       marker=None,
                       markersize=12,
                       color=color_list[i])
    i += 1

    plot_data.write_to_file(figure_dirname, figure_filename)

    return 0


def plot(figure_dirname=None, figure_filename=None, save_types=[]):
    # ==============================================================================
    # title
    # ==============================================================================
    title = ''
    # ==============================================================================
    # figure format
    # http://matplotlib.org/users/customizing.html?highlight=rcparams
    # ==============================================================================
    plot_format()
    # ==============================================================================
    # grid set up
    # ==============================================================================
    # plt.grid(True, which='major',linestyle='-')
    # plt.grid(True, which='minor',linestyle='-')
    # plt.grid(True, which='major')
    # plt.grid(True, which='minor')
    # ==============================================================================
    # print title
    # ==============================================================================
    plt.title(title, fontsize=16)
    # ==============================================================================
    # x,y limite
    # ==============================================================================
    # plt.xlim(400, 1000)
    # plt.ylim(0, 300)
    # ==============================================================================
    # xy log scale
    # ==============================================================================
    # plt.xscale('log')
    # plt.yscale('log')
    # ==============================================================================
    # xy axial equal
    # ==============================================================================
    ax = plt.gca()
    # ax.set_aspect('equal')
    ax.set_aspect('auto')
    # ==============================================================================
    # plot lines
    # ==============================================================================
    plot_data = PlotData()
    plot_data.read_from_file(figure_dirname, figure_filename)
    plot_data.plot()
    # ==============================================================================
    # http://stackoverflow.com/questions/21920233/matplotlib-log-scale-tick-label-number-formatting
    # ==============================================================================
    #    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    #    ax.xaxis.set_minor_locator(MultipleLocator(0.1))
    #    ax.xaxis.set_major_formatter(ScalarFormatter())
    #    ax.yaxis.set_major_locator(MultipleLocator(50))
    #    ax.yaxis.set_minor_locator(MultipleLocator(10))
    #    ax.yaxis.set_major_formatter(ScalarFormatter())
    # ==============================================================================
    # show legend
    # ==============================================================================
    lg = plt.legend(title='', loc=2)
    title = lg.get_title()
    title.set_fontsize(16)
    # ==============================================================================
    # save figures
    # # ==============================================================================
    if figure_dirname is not None and figure_filename is not None:
        for save_type in save_types:
            figure_basename = figure_filename + save_type
            figure_absname = os.path.join(figure_dirname, figure_basename)
            plt.savefig(figure_absname, dpi=100, transparent=True)
            print 'save as', figure_absname
    # plt.show()
    plt.close()

    return 0