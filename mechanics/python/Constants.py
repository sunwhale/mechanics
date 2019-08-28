# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 11:50:47 2017

@author: j.Sun
"""

WorkbenchDirectory = 'F:\\UMAT\\'
UMATDirectory = 'F:\\GitHub\\umat\\'
# UMATDirectory = 'F:\\UMAT\\CurrentVersion\\'
PythonDirectory = 'F:\\GitHub\\python\\'
InputDirectory = WorkbenchDirectory + 'Input\\'
InputTemplate = 'Tension3DTemplate.inp'

# ==============================================================================
# Inconel 718
# ==============================================================================
AbaqusTempDirectory = 'F:\\Temp\\IN7183\\'
ExperimentDirectory = 'F:\\Database\\IN718\\Timed\\'
# ExperimentDirectory = 'F:\\Database\\CMSX4\\Timed\\'
SimulationDirectory = 'F:\\Cloud\\Temp\\IN718_Sim\\'
# SimulationDirectory = 'F:\\Cloud\\Temp\\IN718_Sim_TGMF\\'
ExperimentLogFile = PythonDirectory + 'Inconel718_test_log.csv'
# ExperimentLogFile = PythonDirectory + 'CMSX4_test_log.csv'
# FatigueDirectory = 'F:\\Database\\Fatigue\\'
# FatigueDirectory = 'F:\\Cloud\\GitHub\\fatigue\\model\\'
FatigueDirectory = 'F:\\Cloud\\GitHub\\tgmf\\model\\'
# FatigueDirectory = 'F:\\Cloud\\GitHub\\tgmf\\model\\test\\'
ArticleFigureDirectory = 'F:\\Cloud\\GitHub\\doctor\\Figs\\python\\'
# ArticleFigureDirectory = 'F:\\Cloud\\GitHub\\doctor\\Figs\\test\\'
# ArticleFigureDirectory = 'F:\\Cloud\\GitHub\\tgmf\\Figs\\'

experiment_type_list = []
experiment_type_list.append(['TC-IP', ['7031', '7047', '7030', '7018']])
experiment_type_list.append(['TC-OP', ['7033', '7048', '7032', '7017']])
experiment_type_list.append(['PRO-IP', ['7040', '7029', '7039', '7038']])
experiment_type_list.append(['NPR-IP', ['7036', '7034', '7045', '7046', '7028', '7037']])
experiment_type_list.append(['TC-90', ['7025']])
experiment_type_list.append(['TC-IF', ['7110', '7111', '7112', '7113', '7114', '7115', '7116']])
experiment_type_list.append(['TC-IP-TGMF', ['7201', '7203', '7204', '7205', '7206']])
experiment_type_list.append(['TC-OP-TGMF', ['7207', '7208', '7209', '7210']])
experiment_type_list.append(['TC-IP-TGMF-TBC', ['7301', '7302']])
# experiment_type_list.append(['NPR-IP',['7046']])

experiment_type_dict = {}
experiment_type_dict['TC-IP'] = ['7031', '7047', '7030', '7018']
experiment_type_dict['TC-OP'] = ['7033', '7048', '7032', '7017']
experiment_type_dict['PRO-IP'] = ['7040', '7029', '7039', '7038']
experiment_type_dict['NPR-IP'] = ['7036', '7034', '7045', '7046', '7028', '7037']
experiment_type_dict['TC-90'] = ['7025']
# experiment_type_dict['TC-IF']=['7110','7111','7112','7113','7114','7115','7116']
experiment_type_dict['TC-IF'] = ['7116', '7112', '7110', '7111', '7113', '7115', '7114']
experiment_type_dict['TC-IP-TGMF'] = ['7204', '7203', '7206', '7205']
experiment_type_dict['TC-OP-TGMF'] = ['7210', '7209', '7207', '7208']
experiment_type_dict['TC-IP-TGMF-TBC'] = ['7301', '7302']

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
# plot
# ==============================================================================
marker_list = ['s', 'o', '^', 'D', 'p', '<', '>', 'v', 'h', '8']
color_list = ['red', 'green', 'blue', 'cyan', 'magenta', 'black', 'yellow', 'orange', 'lightgreen']
