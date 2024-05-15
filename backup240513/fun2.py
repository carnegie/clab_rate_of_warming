"""
1. Three models:

- 'Current_policies' 
- 'NDC_case_-_conditional' 
- 'NDC_case_-_unconditional'

2. Scenario example:

- Max/Median/Min emission estimates 
- 0/1/2/3/4/5/Prescribed carbon price growth rate
- AIM/GCAM/MESSAGE/REMIND/WITCH model for price-emission relationship 
- 0.1/.../0.5/.../0.9 percentile of warming 

"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from Info_func import separate_abs_roc_regression
from Info_func import separate_abs_roc_fit
from Info_func import separate_abs_roc_sparse
from Info_func import interpolate_emissions
from Info_func import lowpass_filter
import statsmodels.api as sm
from fun3 import get_data















def check_filter_scenarios(dfTemp, dfEmis): 

    lowpass_threshold = 10
    xaxis = np.arange(2100-1850+1) + 1850 ### Starting from 1850 and end at 2100 

    flagEmissions = True; caseEmissions = 'Median'
    flagModels = True; caseModels = 'MESSAGE'
    flagPrice = True; casePrice = 'incrate2'

    color_list = ['red', 'blue', 'green', 'brown', 'orange', 'purple', 'pink', 'gray', 'cyan']


    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    obs_data_path = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Others/'
    BE, GISS, HadCRUT5, NOAA, ERA5 = get_data(obs_data_path)


    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    #### Get temperature data 
    dfTemp_current_policies = dfTemp[dfTemp['model'] == 'Current_policies'] 
    dfTemp_current_policies = dfTemp_current_policies[dfTemp_current_policies['scenario'].str.contains('KyotoFromPrice')]
    dfTemp_current_policies = dfTemp_current_policies[~dfTemp_current_policies['scenario'].str.contains('nz')]
    dfTemp_uncertainty0 = dfTemp_current_policies
    if flagEmissions == True: dfTemp_uncertainty0 = dfTemp_uncertainty0[dfTemp_uncertainty0['scenario'].str.contains(caseEmissions)]
    if flagModels == True: dfTemp_uncertainty0 = dfTemp_uncertainty0[dfTemp_uncertainty0['scenario'].str.contains(caseModels)]
    if flagPrice == True: dfTemp_uncertainty0 = dfTemp_uncertainty0[dfTemp_uncertainty0['scenario'].str.contains(casePrice)]
    dfTemp_uncertainty1 = dfTemp_uncertainty0
    dfTemp_uncertainty1 = dfTemp_uncertainty0[dfTemp_uncertainty0['quantile'] == 0.5]
    scenario_names = list(dfTemp_uncertainty1['scenario'])
    scenario_names_unify = [s.replace('.csv', '').replace('-', '_') for s in scenario_names]
    scenario_names_unique = list(dfTemp_uncertainty1['scenario'].unique())
    scenario_names_unique_unify = [s.replace('.csv', '').replace('-', '_') for s in scenario_names_unique]
    dict_dfTemp = {}
    for i in range(len(scenario_names_unique_unify)):
        dict_dfTemp[scenario_names_unique_unify[i]] = scenario_names_unique[i]
    print ()
    print ()
    print (len(scenario_names), len(scenario_names_unique)) 

    #### Get emissions data 
    dfEmis_current_policies = dfEmis[dfEmis['Model'] == 'Current policies']
    dfEmis_current_policies = dfEmis_current_policies[dfEmis_current_policies['Scenario'].str.contains('KyotoFromPrice')]
    dfEmis_current_policies = dfEmis_current_policies[~dfEmis_current_policies['Scenario'].str.contains('nz')]
    dfEmis_scenario_names_unique = list(dfEmis_current_policies['Scenario'].unique())
    dfEmis_scenario_names_unique = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in dfEmis_scenario_names_unique]
    dfEmis_uncertainty0 = dfEmis_current_policies
    if flagEmissions == True: dfEmis_uncertainty0 = dfEmis_uncertainty0[dfEmis_uncertainty0['Scenario'].str.contains(caseEmissions)]
    if flagModels == True: dfEmis_uncertainty0 = dfEmis_uncertainty0[dfEmis_uncertainty0['Scenario'].str.contains(caseModels)]
    if flagPrice == True: dfEmis_uncertainty0 = dfEmis_uncertainty0[dfEmis_uncertainty0['Scenario'].str.contains(casePrice)]
    scenario_names = list(dfEmis_uncertainty0['Scenario'])
    scenario_names_unify = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in scenario_names]
    scenario_names_unique = list(dfEmis_uncertainty0['Scenario'].unique())
    scenario_names_unique_unify = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in scenario_names_unique]
    dict_dfEmis = {}
    for i in range(len(scenario_names_unique_unify)):
        dict_dfEmis[scenario_names_unique_unify[i]] = scenario_names_unique[i]
    print (len(scenario_names), len(scenario_names_unique)) 

    print ()
    print ()
    print (len(dfTemp_uncertainty1))
    print (len(dfEmis_uncertainty0)) #### 28 emission variables each scenario 

    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------



    # """
    #### Case 1: plot the relationship 
    # fig, axs = plt.subplots(2, 1, figsize = [5, 10], sharex = True, sharey = False, constrained_layout = True) 
    # axs = axs.flatten()

    for i in range(len(dfTemp_uncertainty1)): 

        fig, axs = plt.subplots(3, 1, figsize = [5, 10], sharex = True, sharey = False, constrained_layout = True) 
        axs = axs.flatten()

        this_entry_dfTemp = dfTemp_uncertainty1.iloc[i] 
        entry_scenario_dfTemp = this_entry_dfTemp['scenario'].replace('.csv', '').replace('-', '_') 
        tas = np.array(this_entry_dfTemp[3:]).astype('float')
        ref_1981_2020 = np.mean(tas[1981-1850:2021-1850])
        tas = tas - ref_1981_2020
        roc = tas[1:] - tas[:-1]

        width = 13
        halfWidth = int((width - 1) / 2)

        axs[0].plot(xaxis, tas, color = 'black', linestyle='--', linewidth=1)
        axs[1].plot(xaxis[1:], roc, color = 'black', linestyle='--', linewidth=1)

        # roc_detrended = lowpass_filter(roc, 'hann', width)
        # axs[2].plot(xaxis[1+halfWidth:-halfWidth], roc_detrended[halfWidth:-halfWidth], color = 'black', linestyle='--', linewidth=1)
 
        roc_detrended = separate_abs_roc_regression(tas, width) 
        axs[2].plot(xaxis[halfWidth:-halfWidth], roc_detrended, color = 'black', linestyle='--', linewidth=1)


        # width = 33
        # tas_detrended = lowpass_filter(tas, 'hann', width)
        # # axs[0].plot(xaxis, tas, color = 'black', linestyle='--', linewidth=1)
        # axs[0].plot(xaxis[5:-5], tas_detrended[5:-5], color = 'red', linestyle='--', linewidth=1)
        # roc = tas[1:] - tas[:-1]
        # roc_detrended = tas_detrended[1:] - tas_detrended[:-1]
        # # axs[1].plot(xaxis[1:], roc, color = 'black', linestyle='--', linewidth=1)
        # axs[1].plot(xaxis[6:-5], roc_detrended[5:-5], color = 'red', linestyle='--', linewidth=1)




        color_list = ['red', 'blue', 'green', 'brown', 'orange', 'purple', 'pink', 'gray', 'cyan']
        i = 0 
        year_obs = np.arange(1980, 2024)
        for obs_i in [BE, GISS, HadCRUT5, NOAA, ERA5]:
            roc_i = obs_i[1:] - obs_i[:-1]
            axs[0].plot(year_obs, obs_i, color=color_list[i], linewidth=1)
            axs[1].plot(year_obs[1:], roc_i, color=color_list[i], linewidth=1)

            roc_detrended = separate_abs_roc_regression(obs_i, width) 
            axs[2].plot(year_obs[halfWidth:-halfWidth], roc_detrended, color=color_list[i], linestyle='--', linewidth=1)

            # roc_i_detrended = lowpass_filter(roc_i, 'hann', width)
            # axs[2].plot(year_obs[1+halfWidth:-halfWidth], roc_i_detrended[halfWidth:-halfWidth], color=color_list[i], linewidth=1)
            i+=1



        # axs[0].set_xlim(2020, 2050)
        axs[0].set_xlim(1980, 2050) 
        # axs[0].set_ylim(0, 2.5)
        # axs[1].set_ylim(-0.1, 0.08)
        # axs[1].set_ylim(-0.0, 0.03)
        plt.show()









        # stop 

        # #### Linear regression approach 
        # window_size_list = [5, 21, 41, 61]   #### If removing both start and end, use odd number
        # for window_size in window_size_list: 
        #     start = int((window_size - 1) / 2)
        #     end = -int(start)
        #     roc = separate_abs_roc_regression(entry_data_dfTemp, lowpass_threshold, window_size) 
        #     axs[1].plot(xaxis[start:end], roc, color = color_list[window_size_list.index(window_size)], linewidth=1, label = str(window_size))
        
        # #### Fitting approach 
        # roc = separate_abs_roc_fit(entry_data_dfTemp, lowpass_threshold, '', False) 
        # axs[2].plot(xaxis, roc, color = 'black', linestyle='--', linewidth=1) 

        # #### Fitting approach with parabola 
        # window_size_list = [5, 21, 41, 61] 
        # for window_size in window_size_list: 
        #     start = int((window_size - 1) / 2)
        #     end = -int(start)
        #     roc = separate_abs_roc_fit(entry_data_dfTemp, lowpass_threshold, window_size, True)
        #     axs[3].plot(xaxis[start:end], roc, color = color_list[window_size_list.index(window_size)], linewidth=1)

        # # entry_scenario_dfEmis = dict_dfEmis[entry_scenario_dfTemp]
        # # this_entry_dfEmis = dfEmis_uncertainty0[dfEmis_uncertainty0['Scenario'] == entry_scenario_dfEmis]
        # # time, entry_CO2_dfEmis = interpolate_emissions(np.array(this_entry_dfEmis[this_entry_dfEmis['Variable'] == 'Emissions|CO2'].iloc[0, 5:]).astype('float'))
        # # time, entry_CO2eq_dfEmis = interpolate_emissions(np.array(this_entry_dfEmis[this_entry_dfEmis['Variable'] == 'Emissions|Kyoto Gases (AR6-GWP100)'].iloc[0, 5:]).astype('float'))
        # # axs[3].plot(time, entry_CO2_dfEmis, color = 'r', linewidth=1)
        # # axs[3].plot(time, entry_CO2eq_dfEmis, color = 'b', linewidth=1)
        # # axs[3].plot(time, entry_CO2eq_dfEmis-entry_CO2_dfEmis, color = 'green', linewidth=1)

        # # axs[0].set_xlim(1980, 2050)
        # axs[0].set_xlim(2000, 2030)

        # axs[1].set_ylim(0, 0.06)
        # axs[2].set_ylim(0, 0.06)
        # axs[3].set_ylim(0, 0.06)

        # # axs[1].legend()
        # plt.show()
    # """








    """
    #### Case 2: try regression for rate of change
    print ()
    print () 


    roc_list = []
    co2_list = []
    co2eq_list = []
    other_list = []
    co2_roc_list = []
    co2eq_roc_list = []
    other_roc_list = []
    co2_list_lag1 = []
    co2eq_list_lag1 = []
    other_list_lag1 = []
    co2_roc_list_lag1 = []
    co2eq_roc_list_lag1 = []
    other_roc_list_lag1 = []


    for i in range(len(dfTemp_uncertainty1)): 

        time_dfTemp = np.arange(1850, 2101, 1)
        time_dfEmis = np.array([2010,2015,2020,2030,2040,2045,2050,2053,2060,2070,2080,2090,2100])

        this_entry_dfTemp = dfTemp_uncertainty1.iloc[i] 
        entry_scenario_dfTemp = this_entry_dfTemp['scenario'].replace('.csv', '').replace('-', '_') 
        entry_data_dfTemp = np.array(this_entry_dfTemp[3:]).astype('float')
        tas = entry_data_dfTemp[time_dfEmis-1850]

        entry_scenario_dfEmis = dict_dfEmis[entry_scenario_dfTemp]
        this_entry_dfEmis = dfEmis_uncertainty0[dfEmis_uncertainty0['Scenario'] == entry_scenario_dfEmis]
        co2 = np.array(this_entry_dfEmis[this_entry_dfEmis['Variable'] == 'Emissions|CO2'].iloc[0, 5:]).astype('float')
        co2eq = np.array(this_entry_dfEmis[this_entry_dfEmis['Variable'] == 'Emissions|Kyoto Gases (AR6-GWP100)'].iloc[0, 5:]).astype('float')
        other = co2eq - co2

        roc_tas = separate_abs_roc_sparse(tas, lowpass_threshold, '', False) 
        roc_co2 = separate_abs_roc_sparse(co2, lowpass_threshold, '', False)
        roc_co2eq = separate_abs_roc_sparse(co2eq, lowpass_threshold, '', False)
        roc_other = separate_abs_roc_sparse(other, lowpass_threshold, '', False)

        start = 3
        end = -3
        roc_list += list(roc_tas[start:end])
        co2_list += list(co2[start:end])
        co2eq_list += list(co2eq[start:end])
        other_list += list(other[start:end])
        co2_roc_list += list(roc_co2[start:end])
        co2eq_roc_list += list(roc_co2eq[start:end])
        other_roc_list += list(roc_other[start:end])
        co2_list_lag1 += list(co2[start-1:end-1])
        co2eq_list_lag1 += list(co2eq[start-1:end-1])
        other_list_lag1 += list(other[start-1:end-1])
        co2_roc_list_lag1 += list(roc_co2[start-1:end-1])
        co2eq_roc_list_lag1 += list(roc_co2eq[start-1:end-1])
        other_roc_list_lag1 += list(roc_other[start-1:end-1])



        # fig, axs = plt.subplots(4, 2, figsize = [5, 10], sharex = True, sharey = False, constrained_layout = True) 
        # axs = axs.flatten()
        # axs[0].plot(time_dfEmis[start:end], tas[start:end], color = 'black', linestyle='--', linewidth=1)
        # axs[1].plot(time_dfEmis[start:end], roc_tas[start:end], color = 'black', linestyle='--', linewidth=1)
        # axs[2].plot(time_dfEmis[start:end], co2[start:end], color = 'r', linestyle='--', linewidth=1)
        # axs[3].plot(time_dfEmis[start:end], roc_co2[start:end], color = 'r', linestyle='--', linewidth=1)
        # axs[4].plot(time_dfEmis[start:end], co2eq[start:end], color = 'b', linestyle='--', linewidth=1)
        # axs[5].plot(time_dfEmis[start:end], roc_co2eq[start:end], color = 'b', linestyle='--', linewidth=1)
        # axs[6].plot(time_dfEmis[start:end], other[start:end], color = 'green', linestyle='--', linewidth=1)
        # axs[7].plot(time_dfEmis[start:end], roc_other[start:end], color = 'green', linestyle='--', linewidth=1)
        # plt.show()

    # print ( len(roc_list) )
    #### Do linear regression with co2_list, co2eq_list, other_list as independent variables

    # X = np.column_stack((np.ones(len(roc_list)), 
    #                      np.array(co2_list)/1e6, 
    #                      np.array(co2eq_list)/1e6, 
    #                      np.array(other_list)/1e6, 
    #                      np.array(co2_roc_list)/1e6, 
    #                      np.array(co2eq_roc_list)/1e6, 
    #                      np.array(other_roc_list)/1e6)) 

    # X = np.column_stack((np.ones(len(roc_list)), 
    #                      np.array(co2_list)/1e6, 
    #                      np.array(co2eq_list)/1e6, 
    #                      np.array(other_list)/1e6, 
    #                      np.array(co2_roc_list)/1e6, 
    #                      np.array(co2eq_roc_list)/1e6, 
    #                      np.array(other_roc_list)/1e6,
    #                      np.array(co2_list_lag1)/1e6,
    #                      np.array(co2eq_list_lag1)/1e6,
    #                      np.array(other_list_lag1)/1e6,
    #                      np.array(co2_roc_list_lag1)/1e6,
    #                      np.array(co2eq_roc_list_lag1)/1e6,
    #                      np.array(other_roc_list_lag1)/1e6))
     

    # X = np.column_stack((np.ones(len(roc_list)), 
    #                      np.array(co2_list)/1e6, 
    #                      np.array(other_list)/1e6, 
    #                      np.array(co2_roc_list)/1e6, 
    #                      np.array(other_roc_list)/1e6)) 
    
    # X = np.column_stack((np.ones(len(roc_list)), 
    #                      np.array(co2_list)/1e6)) 
    
    X = np.column_stack((np.ones(len(roc_list)), 
                         np.array(co2_list)/1e6,
                         np.array(other_list)/1e6,
                         np.array(other_roc_list)/1e6 )) 
    
    Y = np.array(roc_list)

    model = sm.OLS(Y, X)
    results = model.fit()
    print (results.summary())
    # """
