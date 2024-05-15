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
import statsmodels.api as sm
from Info_func import separate_abs_roc_sparse
from fun1 import get_roc

def roc_attribution(dfTemp, dfEmis, axs):


    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    print ()
    print ()
    flagNz = False; caseNz = 'nz'
    flagModels = False ; caseModels = 'MESSAGE'
    flagPrice = False; casePrice = 'incrate2'
    dfTemp_current_policies = dfTemp[dfTemp['model'] == 'Current_policies'] 
    dfTemp_current_policies = dfTemp_current_policies[dfTemp_current_policies['scenario'].str.contains('KyotoFromPrice')]
    dfTemp_current_policies = dfTemp_current_policies[dfTemp_current_policies['scenario'].str.contains('Median')]
    if flagNz == True: dfTemp_current_policies = dfTemp_current_policies[~dfTemp_current_policies['scenario'].str.contains(caseNz)]
    if flagModels == True: dfTemp_current_policies = dfTemp_current_policies[dfTemp_current_policies['scenario'].str.contains(caseModels)]
    if flagPrice == True: dfTemp_current_policies = dfTemp_current_policies[dfTemp_current_policies['scenario'].str.contains(casePrice)]
    dfTemp_current_policies = dfTemp_current_policies[dfTemp_current_policies['quantile'] == 0.5]
    dfTemp_scenario_names_unique = list(dfTemp_current_policies['scenario'].unique())
    dfTemp_scenario_names_unique_unify = [s.replace('.csv', '').replace('-', '_') for s in dfTemp_scenario_names_unique]
    dict_dfTemp = {}
    for i in range(len(dfTemp_scenario_names_unique)):
        dict_dfTemp[dfTemp_scenario_names_unique[i]] = dfTemp_scenario_names_unique_unify[i]
    print (len(dfTemp_current_policies), len(dfTemp_scenario_names_unique_unify)) 
    dfEmis_current_policies = dfEmis[dfEmis['Model'] == 'Current policies']
    dfEmis_current_policies = dfEmis_current_policies[dfEmis_current_policies['Scenario'].str.contains('KyotoFromPrice')]
    dfEmis_current_policies = dfEmis_current_policies[dfEmis_current_policies['Scenario'].str.contains('Median')]
    if flagNz == True: dfEmis_current_policies = dfEmis_current_policies[~dfEmis_current_policies['Scenario'].str.contains(caseNz)]
    if flagModels == True: dfEmis_current_policies = dfEmis_current_policies[dfEmis_current_policies['Scenario'].str.contains(caseModels)] 
    if flagPrice == True: dfEmis_current_policies = dfEmis_current_policies[dfEmis_current_policies['Scenario'].str.contains(casePrice)]
    dfEmis_scenario_names_unique = list(dfEmis_current_policies['Scenario'].unique())
    dfEmis_scenario_names_unique_unify = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in dfEmis_scenario_names_unique]
    dict_dfEmis = {}
    for i in range(len(dfEmis_scenario_names_unique_unify)):
        dict_dfEmis[dfEmis_scenario_names_unique_unify[i]] = dfEmis_scenario_names_unique[i]
    print (len(dfEmis_current_policies), len(dfEmis_scenario_names_unique_unify))  #### 28 species each case


    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    print ()
    print ()
    roc_list = [] 
    co2eq_list,    co2_list,        other_list,      co2_roc_list,      co2eq_roc_list,      other_roc_list      = [], [], [], [], [], []
    co2_list_lag1, co2eq_list_lag1, other_list_lag1, co2_roc_list_lag1, co2eq_roc_list_lag1, other_roc_list_lag1 = [], [], [], [], [], []
    time_dfEmis = np.array([2010,2015,2020,2030,2040,2045,2050,2053,2060,2070,2080,2090,2100])
    color_list = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    list_work = [] 
    list_not_work = [] 
    for i in range(len(dfTemp_current_policies)): 
        
        this_entry_dfTemp = dfTemp_current_policies.iloc[i] 
        entry_scenario_dfTemp = dict_dfTemp[this_entry_dfTemp['scenario']]

        if entry_scenario_dfTemp in dict_dfEmis.keys():

            entry_data_dfTemp = np.array(this_entry_dfTemp[3:]).astype('float')
            # tas = entry_data_dfTemp[time_dfEmis-1850]
            # roc_tas = separate_abs_roc_sparse(tas)
            tas = entry_data_dfTemp
            year, roc = get_roc(tas, np.arange(1850, 2101, 1), 1, 17)
            roc_tas = roc[time_dfEmis[3:-3]-year[0]]
            roc_list += list(roc_tas)
            
            entry_scenario_dfEmis = dict_dfEmis[entry_scenario_dfTemp]
            this_entry_dfEmis = dfEmis_current_policies[dfEmis_current_policies['Scenario'] == entry_scenario_dfEmis]
            
            co2eq = np.array(this_entry_dfEmis[this_entry_dfEmis['Variable'] == 'Emissions|Kyoto Gases (AR6-GWP100)'].iloc[0, 5:]).astype('float')
            co2 = np.array(this_entry_dfEmis[this_entry_dfEmis['Variable'] == 'Emissions|CO2'].iloc[0, 5:]).astype('float')
            other = co2eq - co2 

            # roc_co2 = separate_abs_roc_sparse(co2)
            # roc_co2eq = separate_abs_roc_sparse(co2eq) 
            # roc_other = separate_abs_roc_sparse(other) 
            # start, end = 3, -3
            # co2_list += list(co2[start:end])
            # co2eq_list += list(co2eq[start:end])
            # other_list += list(other[start:end])
            # co2_roc_list += list(roc_co2[start:end])
            # co2eq_roc_list += list(roc_co2eq[start:end])
            # other_roc_list += list(roc_other[start:end])
            # co2_list_lag1 += list(co2[start-1:end-1])
            # co2eq_list_lag1 += list(co2eq[start-1:end-1])
            # other_list_lag1 += list(other[start-1:end-1])
            # co2_roc_list_lag1 += list(roc_co2[start-1:end-1])
            # co2eq_roc_list_lag1 += list(roc_co2eq[start-1:end-1]) 
            # other_roc_list_lag1 += list(roc_other[start-1:end-1])
            # list_work.append(entry_scenario_dfTemp)

            to_plot_x = co2eq[3:-3]
            to_plot_y = roc_tas
            if entry_scenario_dfTemp == 'Median_Harmonized_KyotoFromPrice_incrate2_MESSAGE_GLOBIOM_1_0_SSP2':
                for i in range(len(to_plot_x)): axs.scatter(to_plot_x[i]/1e6, to_plot_y[i], c=color_list[i], s=10)
            else:
                for i in range(len(to_plot_x)): axs.scatter(to_plot_x[i]/1e6, to_plot_y[i], c=color_list[i], s=10, alpha=0.8)
            

    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # print ()
    # print ()
    dfTemp_best_estimate = dfTemp[dfTemp['model'] == 'Current_policies'] 
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('KyotoFromPrice')]
    dfTemp_best_estimate = dfTemp_best_estimate[~dfTemp_best_estimate['scenario'].str.contains('nz')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('Median')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('MESSAGE')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('incrate2')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['quantile'] == 0.5]
    # stop 



    #### 0.981
    # X = np.column_stack((np.ones(len(roc_list)), 
    #                      np.array(co2_list)/1e6, np.array(other_list)/1e6, 
    #                      np.array(co2_roc_list)/1e6, np.array(other_roc_list)/1e6,
    #                      np.array(co2_list_lag1)/1e6, np.array(other_list_lag1)/1e6,
    #                      np.array(co2_roc_list_lag1)/1e6, np.array(other_roc_list_lag1)/1e6))

    # #### 0.940 
    # X = np.column_stack((np.ones(len(roc_list)), 
    #                      np.array(co2_list)/1e6, np.array(other_list)/1e6, 
    #                      np.array(co2_roc_list)/1e6, np.array(other_roc_list)/1e6))
    
    # # #### 0.919 
    # X = np.column_stack((np.ones(len(roc_list)), 
    #                      np.array(co2_list)/1e6, np.array(other_list)/1e6))
    
    # #### 0.724
    # X = np.column_stack((np.ones(len(roc_list)), 
    #                      np.array(co2_roc_list)/1e6, np.array(other_roc_list)/1e6))

    # #### 0.919 
    # X = np.column_stack((np.ones(len(roc_list)), 
    #                      np.array(co2_list)/1e6, np.array(other_list)/1e6))


    # # #### 0.919 
    # X = np.column_stack((np.ones(len(roc_list)), np.array(co2eq_list)/1e6))
    # Y = np.array(roc_list)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print () 
    # print (results.summary())

    # X = np.column_stack((np.ones(len(roc_list)), np.array(co2_list)/1e6))
    # Y = np.array(roc_list)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print () 
    # print (results.summary()) 

    # roc_list = np.array(roc_list).reshape(-1, 7)
    # co2eq_list = np.array(co2eq_list).reshape(-1, 7)

    # color_list = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    # label_list = [2030,2040,2045,2050,2053,2060,2070]
    # for i in range(7):
    #     axs.scatter(np.array(co2eq_list[:, i])/1e6, roc_list[:, i], c=color_list[i], s=10, label=label_list[i])
    # axs.scatter(np.array(co2_list)/1e6, Y, c='blue', s=10)