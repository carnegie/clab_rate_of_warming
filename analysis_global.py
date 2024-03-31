from SUB_Class_CMIP6 import CMIP6_models
from SUB_Class_CMIP6 import set_class_instance
from Info_func import info_func
from Info_func import lowpass_filter
from Info_func import separate_abs_roc

import cdms2 as cdms
import cdutil 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 


def analysis_global(scenario_list):


    fig, axs = plt.subplots(2, 1, figsize = [5, 8], 
                            sharex = True, sharey = False, constrained_layout = True)
    axs = axs.ravel()

    info_dict = info_func()
    data_path = info_dict['data_path']
    lowpass_threshold = 10


    # ------------------------------------------------------------------------
    #### Meinshausen et al. 2022

    csv_file_name = data_path + '/Data_Meinshausen2022/timeseries_12Nov2021a_CR.csv'
    data_MM = pd.read_csv(csv_file_name)
    tas_MM = data_MM[data_MM['variable'] == 'Surface Temperature (GSAT)|MAGICCv7.5.3']
    keys = list(data_MM.keys())
    tas_MM = np.array(tas_MM.iloc[:, 13:])     # (4254, 106)

    xaxis = np.arange(106) + 1995
    for i in range(tas_MM.shape[0]):
        tas, roc_tas = separate_abs_roc(tas_MM[i], lowpass_threshold)
        # axs[0].plot(xaxis, tas, 'grey', alpha=0.1, linewidth=0.1)
        axs[1].plot(xaxis[16:-15], roc_tas, 'grey', alpha=0.1, linewidth=0.1)

    # plt.show() 
    # plt.clf() 
    # stop 


    # ------------------------------------------------------------------------
    #### CMIP6 models  
        
    set_class_instance()
    

    for scenario in scenario_list: 

        count = 0 
        if scenario in ['ssp126', 'ssp245', 'ssp585']:
            tas_abs = np.zeros([32, 250])
            tas_roc = np.zeros([32, 250-31])
        if scenario in ['ssp370']:
            tas_abs = np.zeros([29, 250])
            tas_roc = np.zeros([29, 250-31])

        if scenario == 'ssp126': lc = 'blue'
        if scenario == 'ssp245': lc = 'green'
        if scenario == 'ssp370': lc = 'orange'
        if scenario == 'ssp585': lc = 'red'

        for instance in CMIP6_models.instances:

            model_Name = instance.Name
            model_CaseList = instance.CaseList
            model_VarLab = instance.VarLab[0]

            # if model_Name in ["ACCESS-CM2"]:
            if scenario in model_CaseList:

                # ------------------------------------------------------------------------
                ########################
                #### Get data  
                ########################

                hist_name = f'/CMIP6_Regrid/tasCanESM5_{model_Name}_historical_{model_VarLab}.nc' 
                fopen_hist = cdms.open(data_path + hist_name)
                tas_hist = cdutil.averager(fopen_hist('tas'), axis='yx')

                ssps_name = f'/CMIP6_Regrid/tasCanESM5_{model_Name}_{scenario}_{model_VarLab}.nc' 
                fopen_ssps = cdms.open(data_path + ssps_name)
                tas_ssps = cdutil.averager(fopen_ssps('tas'), axis='yx') 

                tas = np.array(np.r_[tas_hist, tas_ssps])
                if np.max(tas) > 200: tas = tas - 273.15
                tas, roc_tas = separate_abs_roc(tas, lowpass_threshold)

                # ------------------------------------------------------------------------    
                tas_abs[count] = tas
                tas_roc[count] = roc_tas
                count += 1

        print ()
        print (count)
        # ------------------------------------------------------------------------  
        ensemble_mean_tas_roc = np.mean(tas_roc, axis=0)
        print (np.max(ensemble_mean_tas_roc))
        print (np.argmax(ensemble_mean_tas_roc))
        print ()
        axs[0].plot(np.arange(250) + 1850, np.mean(tas_abs, axis=0), color=lc, linestyle='-')
        axs[1].plot(np.arange(250-31) + 1850 + 16, np.mean(tas_roc, axis=0), color=lc, linestyle='--') 
    
    # plt.show()
    plt.savefig('ssps_annual.ps')
    plt.clf() 
