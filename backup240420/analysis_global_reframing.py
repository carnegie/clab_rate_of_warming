from SUB_Class_CMIP6 import CMIP6_models
from SUB_Class_CMIP6 import set_class_instance
from Info_func import info_func
from Info_func import lowpass_filter
from Info_func import separate_abs_roc

import cdms2 as cdms
import cdutil 
import numpy as np 
import pandas as pd
import pickle 

import matplotlib.pyplot as plt 


def analysis_global(source_list):



    #### Shared information 
    info_dict = info_func()
    data_path = info_dict['data_path']
    lowpass_threshold = 0
    window_size = 41




    #### Analysis of the AR6 scenario database
    if 'AR6' in source_list:

        #### Get the whole dataset 
        # csv_file_name = data_path + '/AR6_scenario_database/AR6_Scenarios_Database_World_ALL_CLIMATE_v1.1.csv/AR6_Scenarios_Database_World_ALL_CLIMATE_v1.1.csv'
        csv_file_name = data_path + '/AR6_scenario_database/AR6_Scenarios_Database_World_v1.1.csv/AR6_Scenarios_Database_World_v1.1.csv'
        data_AR6 = pd.read_csv(csv_file_name)
        keys = list(data_AR6.keys()) 
        scenario_list = data_AR6['Scenario'].unique()
        variable_list = data_AR6['Variable'].unique()

        tas_AR6 = data_AR6[data_AR6['Unit'] == 'K'] 
        tas_AR6 = np.array(tas_AR6.iloc[:, 5:])
        whereisnan = np.isnan(tas_AR6) 
        tas_AR6 = np.ma.masked_where(whereisnan, tas_AR6)

        #### Separate into different categories 
        fig, axs = plt.subplots(2, 1, figsize = [5, 8], sharex = True, sharey = False, constrained_layout = True) 
        xaxis = np.arange(106) + 1995
        for i in range(tas_AR6.shape[0]):
            this_entry = tas_AR6[i] 
            peak_awarming = np.max(this_entry)
            if peak_awarming <= 1.5:
            # if peak_awarming > 1.5 and peak_awarming <= 2.0:
            # if peak_awarming <= 2.0:
            # if peak_awarming > 2.0 and peak_awarming <= 3.0:
            # if peak_awarming > 3.0 and peak_awarming <= 4.0:
            # if peak_awarming > 4.0:
            # if peak_awarming <= 100.0: 
                tas, roc_tas = separate_abs_roc(tas_AR6[i], lowpass_threshold, window_size)
                if np.argmax(roc_tas) + 1995 + 21 <= 2030: lc = 'firebrick'
                if np.argmax(roc_tas) + 1995 + 21 > 2030 and np.max(roc_tas) + 1995 + 21 <= 2050: lc = 'royalblue'
                if np.argmax(roc_tas) + 1995 + 21 > 2050 and np.max(roc_tas) + 1995 + 21 <= 2080: lc = 'orange'
                if np.argmax(roc_tas) + 1995 + 21 > 2080: lc = 'darkgreen'
                axs[0].plot(xaxis, tas, color=lc, linewidth=0.05)
                axs[1].plot(xaxis[int((window_size+1)/2):int(-0.5*(window_size-1))], roc_tas, color=lc, linewidth=0.05)
        axs[0].set_ylabel('Global mean temperature anomaly (K)')
        axs[1].set_ylabel('Rate of change (K/year)')
        plt.show() 
        plt.clf()


    if 'CMIP6' in source_list: 

        set_class_instance()

        # fig, axs = plt.subplots(2, 1, figsize = [5, 8], sharex = True, sharey = False, constrained_layout = True) 

        for scenario in ['ssp126', 'ssp245', 'ssp370', 'ssp585']: 

            fig, axs = plt.subplots(2, 1, figsize = [5, 8], sharex = True, sharey = False, constrained_layout = True) 
            count = 0 

            if scenario in ['ssp126', 'ssp245', 'ssp585']:
                tas_abs = np.zeros([32, 250])
                tas_roc = np.zeros([32, 250-window_size])
            if scenario in ['ssp370']:
                tas_abs = np.zeros([29, 250])
                tas_roc = np.zeros([29, 250-window_size])

            if scenario == 'ssp126': lc = 'blue'
            if scenario == 'ssp245': lc = 'green'
            if scenario == 'ssp370': lc = 'orange'
            if scenario == 'ssp585': lc = 'red'

            for instance in CMIP6_models.instances:

                model_Name = instance.Name
                model_CaseList = instance.CaseList
                model_VarLab = instance.VarLab[0]

                if scenario in model_CaseList:

                    # ------------------------------------------------------------------------
                    hist_name = f'/CMIP6_Regrid/tasCanESM5_{model_Name}_historical_{model_VarLab}.nc' 
                    fopen_hist = cdms.open(data_path + hist_name)
                    tas_hist = cdutil.averager(fopen_hist('tas'), axis='yx')

                    ssps_name = f'/CMIP6_Regrid/tasCanESM5_{model_Name}_{scenario}_{model_VarLab}.nc' 
                    fopen_ssps = cdms.open(data_path + ssps_name)
                    tas_ssps = cdutil.averager(fopen_ssps('tas'), axis='yx') 

                    tas = np.array(np.r_[tas_hist, tas_ssps])
                    if np.max(tas) > 200: tas = tas - 273.15
                    tas, roc_tas = separate_abs_roc(tas, lowpass_threshold, window_size)

                    # ------------------------------------------------------------------------    
                    tas_abs[count] = tas
                    tas_roc[count] = roc_tas
                    count += 1 

            # ------------------------------------------------------------------------  
            for i in range(tas_abs.shape[0]):
                initial = np.mean(tas_abs[i, :50])
                if np.argmax(tas_roc[i]) + 1850 + 21 <= 2030: lc = 'firebrick'
                if np.argmax(tas_roc[i]) + 1850 + 21 > 2030 and np.max(tas_roc[i]) + 1850 + 21 <= 2050: lc = 'royalblue'
                if np.argmax(tas_roc[i]) + 1850 + 21 > 2050 and np.max(tas_roc[i]) + 1850 + 21 <= 2080: lc = 'orange'
                if np.argmax(tas_roc[i]) + 1850 + 21 > 2080: lc = 'darkgreen'
                axs[0].plot(np.arange(250) + 1850, tas_abs[i] - initial, color=lc, linewidth=0.5, alpha=1)
                axs[1].plot(np.arange(250-window_size) + 1850 + (window_size+1)/2, tas_roc[i], color=lc, linewidth=0.5, alpha=1) 
            axs[0].set_ylabel('Global mean temperature anomaly (K)')
            axs[1].set_ylabel('Rate of change (K/year)')
            plt.show()
            # plt.savefig('ssps_annual.ps')
            plt.clf() 



    if 'NDCs' in source_list: 

        # ------------------------------------------------------------------------
        #### Meinshausen et al. 2022
        csv_file_name = data_path + '/Data_Meinshausen2022/timeseries_12Nov2021a_CR.csv'
        data_MM = pd.read_csv(csv_file_name)
        tas_MM = data_MM[data_MM['variable'] == 'Surface Temperature (GSAT)|MAGICCv7.5.3']
        keys = list(data_MM.keys())
        tas_MM = np.array(tas_MM.iloc[:, 13:])     # (4254, 106)

        fig, axs = plt.subplots(2, 1, figsize = [5, 8], sharex = True, sharey = False, constrained_layout = True) 
        xaxis = np.arange(106) + 1995
        for i in range(tas_MM.shape[0]):

            this_entry = tas_MM[i]
            peak_awarming = np.max(this_entry)
            # if peak_awarming <= 2.0:
            # if peak_awarming > 2.0 and peak_awarming <= 3.0:
            # if peak_awarming > 3.0 and peak_awarming <= 4.0:
            if peak_awarming > 4.0:
            # if peak_awarming < 100.0:
                tas, roc_tas = separate_abs_roc(this_entry, lowpass_threshold, window_size)
                if np.argmax(roc_tas) + 1995 + 21 <= 2030: lc = 'firebrick'
                if np.argmax(roc_tas) + 1995 + 21 > 2030 and np.max(roc_tas) + 1995 + 21 <= 2050: lc = 'royalblue'
                if np.argmax(roc_tas) + 1995 + 21 > 2050 and np.max(roc_tas) + 1995 + 21 <= 2080: lc = 'orange'
                if np.argmax(roc_tas) + 1995 + 21 > 2080: lc = 'green'
                axs[0].plot(xaxis, tas, color=lc, alpha=1, linewidth=0.1)
                axs[1].plot(xaxis[int((window_size+1)/2):int(-0.5*(window_size-1))], roc_tas, color=lc, alpha=1, linewidth=0.1)

        axs[0].set_ylabel('Global mean temperature anomaly (K)')
        axs[1].set_ylabel('Rate of change (K/year)')

        plt.show() 
        plt.clf() 



























    # # ------------------------------------------------------------------------
    # #### Reanalysis 
    # pickle_file_name = data_path + '/Reanalysis/ERA5_global_avg.pickle'
    # with open(pickle_file_name, 'rb') as f: 
    #     data_ERA5 = pickle.load(f)
    # ERA5_gm_monthly = np.array(data_ERA5['gm']).reshape(-1, 12)
    # ERA5_gm = np.mean(ERA5_gm_monthly, axis=1) - 273.15

    # xaxis = np.arange(45) + 1979
    # axs[0].plot(xaxis, ERA5_gm, 'black', linewidth=0.5)
    # # plt.show()
    # # plt.clf() 
    # # stop 
