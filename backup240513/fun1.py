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
from Info_func import separate_abs_roc_yty
from Info_func import interpolate_emissions


def comb_filter_scenarios(dfTemp, dfEmis): 

    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    #### Get only current policy with no nz committeement scenairos
    dfTemp_current_policies = dfTemp[dfTemp['model'] == 'Current_policies'] 
    dfTemp_current_policies = dfTemp_current_policies[dfTemp_current_policies['scenario'].str.contains('KyotoFromPrice')]
    dfTemp_current_policies = dfTemp_current_policies[~dfTemp_current_policies['scenario'].str.contains('nz')]

    dfEmis_current_policies = dfEmis[dfEmis['Model'] == 'Current policies']
    dfEmis_current_policies = dfEmis_current_policies[dfEmis_current_policies['Scenario'].str.contains('KyotoFromPrice')]
    dfEmis_current_policies = dfEmis_current_policies[~dfEmis_current_policies['Scenario'].str.contains('nz')]
    dfEmis_scenario_names_unique = list(dfEmis_current_policies['Scenario'].unique())
    dfEmis_scenario_names_unique = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in dfEmis_scenario_names_unique]

    # print (len(dfEmis_scenario_names_unique))
    # diff_list = []
    # for i in dfTemp_scenario_names_unique:
    #     if i not in dfEmis_scenario_names_unique: diff_list.append(i)
    # if len(diff_list) == 0:
    #     print ('same sceniarios between emissions and temperature change')
    # else:
    #     print ('different scenarios: ', len(diff_list), ' will stop now')
    #     stop 


    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    flagEmissions = True
    caseEmissions = 'Median'

    flagModels = False 
    caseModels = 'MESSAGE'

    flagPrice = False
    casePrice = 'incrate2'

    lowpass_threshold = 0
    window_size = 17
    fit_choice = 1

    xaxis = np.arange(2100-1850+1) + 1850 ### Starting from 1850 and end at 2100 

    fig, axs = plt.subplots(2, 2, figsize = [10, 10], sharex = True, sharey = False, constrained_layout = True) 
    axs = axs.flatten()



    # """
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    dfTemp_uncertainty0 = dfTemp_current_policies
    if flagEmissions == True: dfTemp_uncertainty0 = dfTemp_uncertainty0[dfTemp_uncertainty0['scenario'].str.contains(caseEmissions)]
    if flagModels == True: dfTemp_uncertainty0 = dfTemp_uncertainty0[dfTemp_uncertainty0['scenario'].str.contains(caseModels)]
    if flagPrice == True: dfTemp_uncertainty0 = dfTemp_uncertainty0[dfTemp_uncertainty0['scenario'].str.contains(casePrice)]
    scenario_names = list(dfTemp_uncertainty0['scenario'])
    scenario_names = [s.replace('.csv', '').replace('-', '_') for s in scenario_names]
    scenario_names_unique = list(dfTemp_uncertainty0['scenario'].unique())
    scenario_names_unique = [s.replace('.csv', '').replace('-', '_') for s in scenario_names_unique]
    print ()
    print (len(scenario_names), len(scenario_names_unique)) 
    to_plot_uncertainty0 = np.array(dfTemp_uncertainty0.iloc[:, 3:])
    # peak_roc_year = [] 
    for i in range(to_plot_uncertainty0.shape[0]):
        tas = to_plot_uncertainty0[i]
        if fit_choice == 0:
            year, roc = separate_abs_roc_regression(tas, xaxis, window_size)

        if fit_choice == 1:
            year, roc = separate_abs_roc_yty(tas, xaxis, window_size)



        # index_1980_roc = 1980 - (1850 + window_size - 1)
        # index_2050_roc = 2050 - (1850 + window_size - 1) + 1
        # peak_roc_year.append(np.argmax(roc[index_1980_roc:index_2050_roc]))
        if i == 0: tas_stack, roc_stack = np.array(tas), np.array(roc)
        if i != 0: tas_stack, roc_stack = np.vstack((tas_stack, np.array(tas))), np.vstack((roc_stack, np.array(roc)))
    max_tas = np.max(tas_stack, axis=0)
    min_tas = np.min(tas_stack, axis=0)
    max_roc = np.max(roc_stack, axis=0)
    min_roc = np.min(roc_stack, axis=0)
    axs[1].fill_between(xaxis, max_tas, min_tas, color='blue', alpha=0.1)
    axs[3].fill_between(year, max_roc, min_roc, color='blue', alpha=0.1)
    # #### Find where the peak warming is
    # peak_roc_year = np.array(peak_roc_year)
    # min_boundary, max_boundary = np.min(peak_roc_year) + 1980, np.max(peak_roc_year) + 1980
    # axs[3].fill_betweenx([0, 0.035], [min_boundary, min_boundary], [max_boundary, max_boundary], color='firebrick', alpha=0.2)

    # ----------------------------------------------------------------------------------------------------------------------
    dfTemp_uncertainty1 = dfTemp_uncertainty0[dfTemp_uncertainty0['quantile'] == 0.5]
    scenario_names = list(dfTemp_uncertainty1['scenario'])
    scenario_names = [s.replace('.csv', '').replace('-', '_') for s in scenario_names]
    scenario_names_unique = list(dfTemp_uncertainty1['scenario'].unique())
    scenario_names_unique = [s.replace('.csv', '').replace('-', '_') for s in scenario_names_unique]
    print ()
    print (len(scenario_names), len(scenario_names_unique)) 
    to_plot_uncertainty1 = np.array(dfTemp_uncertainty1.iloc[:, 3:])
    for i in range(to_plot_uncertainty1.shape[0]):
        tas = to_plot_uncertainty1[i]
        if fit_choice == 0:
            year, roc = separate_abs_roc_regression(tas, xaxis, window_size)
        if fit_choice == 1:
            year, roc = separate_abs_roc_yty(tas, xaxis, window_size)
        if i == 0: tas_stack, roc_stack = np.array(tas), np.array(roc)
        if i != 0: tas_stack, roc_stack = np.vstack((tas_stack, np.array(tas))), np.vstack((roc_stack, np.array(roc)))
    max_tas = np.max(tas_stack, axis=0)
    min_tas = np.min(tas_stack, axis=0)
    max_roc = np.max(roc_stack, axis=0)
    min_roc = np.min(roc_stack, axis=0)
    axs[1].fill_between(xaxis, max_tas, min_tas, color='blue', alpha=0.3)
    axs[3].fill_between(year, max_roc, min_roc, color='blue', alpha=0.3)

    # ----------------------------------------------------------------------------------------------------------------------
    #### Best estimate cases: 
    ####    1.1. Current policy no net zero targets 
    ####    1.2. Median emissions 
    ####    1.3. MESSAGE model for emission projections 
    ####    1.4. 2% increasing rate
    ####    1.5. 0.5 percentiles
    dfTemp_best_estimate = dfTemp[dfTemp['model'] == 'Current_policies'] 
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('KyotoFromPrice')]
    dfTemp_best_estimate = dfTemp_best_estimate[~dfTemp_best_estimate['scenario'].str.contains('nz')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('Median')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('MESSAGE')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('incrate2')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['quantile'] == 0.5]
    scenario_names = list(dfTemp_best_estimate['scenario'])
    scenario_names = [s.replace('.csv', '').replace('-', '_') for s in scenario_names]
    scenario_names_unique = list(dfTemp_best_estimate['scenario'].unique())
    scenario_names_unique = [s.replace('.csv', '').replace('-', '_') for s in scenario_names_unique]
    print ()
    print (len(scenario_names), len(scenario_names_unique)) 
    to_plot_best_estimate = np.array(dfTemp_best_estimate.iloc[:, 3:])
    for i in range(to_plot_best_estimate.shape[0]): 
        tas = to_plot_best_estimate[i]
        if fit_choice == 0:
            year, roc = separate_abs_roc_regression(tas, xaxis, window_size)
        if fit_choice == 1:
            year, roc = separate_abs_roc_yty(tas, xaxis, window_size)
        axs[1].plot(xaxis, tas, color='black', linewidth=1.5)
        axs[3].plot(year, roc, color='black', linewidth=1.5)
    # """



    # """
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    dfEmis_uncertainty0 = dfEmis_current_policies
    if flagEmissions == True: dfEmis_uncertainty0 = dfEmis_uncertainty0[dfEmis_uncertainty0['Scenario'].str.contains(caseEmissions)]
    if flagModels == True: dfEmis_uncertainty0 = dfEmis_uncertainty0[dfEmis_uncertainty0['Scenario'].str.contains(caseModels)]
    if flagPrice == True: dfEmis_uncertainty0 = dfEmis_uncertainty0[dfEmis_uncertainty0['Scenario'].str.contains(casePrice)]
    scenario_names = list(dfEmis_uncertainty0['Scenario'])
    scenario_names = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in scenario_names]
    scenario_names_unique = list(dfEmis_uncertainty0['Scenario'].unique())
    scenario_names_unique = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in scenario_names_unique]
    print ()
    print (len(scenario_names), len(scenario_names_unique)) 
    dfEmis_uncertainty0_CO2 = dfEmis_uncertainty0[dfEmis_uncertainty0['Variable'] == 'Emissions|CO2']
    dfEmis_uncertainty0_CO2eq = dfEmis_uncertainty0[dfEmis_uncertainty0['Variable'] == 'Emissions|Kyoto Gases (AR6-GWP100)']
    to_plot_uncertainty1_CO2 = np.array(dfEmis_uncertainty0_CO2.iloc[:, 5:])
    to_plot_uncertainty1_CO2eq = np.array(dfEmis_uncertainty0_CO2eq.iloc[:, 5:])
    for i in range(to_plot_uncertainty1_CO2.shape[0]):
        x_fine, y_fine_CO2 = interpolate_emissions(to_plot_uncertainty1_CO2[i])
        x_fine, y_fine_CO2eq = interpolate_emissions(to_plot_uncertainty1_CO2eq[i])
        if i == 0: co2_stack, co2eq_stack = np.array(y_fine_CO2), np.array(y_fine_CO2eq)
        if i != 0: co2_stack, co2eq_stack = np.vstack((co2_stack, np.array(y_fine_CO2))), np.vstack((co2eq_stack, np.array(y_fine_CO2eq)))
        cumulative_y_fine_CO2 = np.cumsum(y_fine_CO2)
        cumulative_y_fine_CO2eq = np.cumsum(y_fine_CO2eq)
        if i == 0: cumulative_co2_stack, cumulative_co2eq_stack = np.array(cumulative_y_fine_CO2), np.array(cumulative_y_fine_CO2eq)
        if i != 0: cumulative_co2_stack, cumulative_co2eq_stack = np.vstack((cumulative_co2_stack, np.array(cumulative_y_fine_CO2))), np.vstack((cumulative_co2eq_stack, np.array(cumulative_y_fine_CO2eq)))
    max_co2 = np.max(co2_stack, axis=0)
    min_co2 = np.min(co2_stack, axis=0)
    max_co2eq = np.max(co2eq_stack, axis=0)
    min_co2eq = np.min(co2eq_stack, axis=0)
    axs[2].fill_between(x_fine, max_co2, min_co2, color='r', alpha=0.5)
    axs[2].fill_between(x_fine, max_co2eq, min_co2eq, color='b', alpha=0.5)
    max_cumulative_co2 = np.max(cumulative_co2_stack, axis=0)
    min_cumulative_co2 = np.min(cumulative_co2_stack, axis=0)
    max_cumulative_co2eq = np.max(cumulative_co2eq_stack, axis=0)
    min_cumulative_co2eq = np.min(cumulative_co2eq_stack, axis=0)
    axs[0].fill_between(x_fine, max_cumulative_co2, min_cumulative_co2, color='r', alpha=0.5)
    axs[0].fill_between(x_fine, max_cumulative_co2eq, min_cumulative_co2eq, color='b', alpha=0.5)

    # ----------------------------------------------------------------------------------------------------------------------
    dfEmis_best_estimate = dfEmis[dfEmis['Model'] == 'Current policies']
    dfEmis_best_estimate = dfEmis_best_estimate[dfEmis_best_estimate['Scenario'].str.contains('KyotoFromPrice')]
    dfEmis_best_estimate = dfEmis_best_estimate[~dfEmis_best_estimate['Scenario'].str.contains('nz')]
    dfEmis_best_estimate = dfEmis_best_estimate[dfEmis_best_estimate['Scenario'].str.contains('Median')]
    dfEmis_best_estimate = dfEmis_best_estimate[dfEmis_best_estimate['Scenario'].str.contains('MESSAGE')]
    dfEmis_best_estimate = dfEmis_best_estimate[dfEmis_best_estimate['Scenario'].str.contains('incrate2')]
    scenario_names = list(dfEmis_best_estimate['Scenario'])
    scenario_names = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in scenario_names]
    scenario_names_unique = list(dfEmis_best_estimate['Scenario'].unique())
    scenario_names_unique = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in scenario_names_unique]
    print ()
    print (len(scenario_names), len(scenario_names_unique)) 
    dfEmis_best_estimate_CO2 = dfEmis_best_estimate[dfEmis_best_estimate['Variable'] == 'Emissions|CO2']
    dfEmis_best_estimate_CO2eq = dfEmis_best_estimate[dfEmis_best_estimate['Variable'] == 'Emissions|Kyoto Gases (AR6-GWP100)']
    to_plot_best_estimate_CO2 = np.array(dfEmis_best_estimate_CO2.iloc[:, 5:])
    to_plot_best_estimate_CO2eq = np.array(dfEmis_best_estimate_CO2eq.iloc[:, 5:])
    for i in range(to_plot_best_estimate_CO2.shape[0]): 
        x_fine, y_fine_CO2 = interpolate_emissions(to_plot_best_estimate_CO2[i])
        x_fine, y_fine_CO2eq = interpolate_emissions(to_plot_best_estimate_CO2eq[i])
        axs[2].plot(x_fine, y_fine_CO2, color='r', linewidth=1.5)
        axs[2].plot(x_fine, y_fine_CO2eq, color='b', linewidth=1.5)
        cumulative_y_fine_CO2 = np.cumsum(y_fine_CO2)
        cumulative_y_fine_CO2eq = np.cumsum(y_fine_CO2eq)
        axs[0].plot(x_fine, cumulative_y_fine_CO2, color='r', linewidth=1.5)
        axs[0].plot(x_fine, cumulative_y_fine_CO2eq, color='b', linewidth=1.5)
    # """



    # """
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    from Info_func import get_rw_data
    obs_data_path = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Others/'
    BE, GISS, HadCRUT5, NOAA, ERA5 = get_rw_data(obs_data_path)
    color_list = ['red', 'blue', 'green', 'brown', 'orange', 'purple', 'pink', 'gray', 'cyan']
    i = 0 
    year_obs = np.arange(1980, 2024) 
    for obs_i in [BE, GISS, HadCRUT5, NOAA, ERA5]: 
        tas = obs_i
        if fit_choice == 0:
            year, roc = separate_abs_roc_regression(tas, year_obs, window_size) 
        if fit_choice == 1:
            year, roc = separate_abs_roc_yty(tas, year_obs, window_size) 
        axs[1].plot(year_obs, tas, color=color_list[i], linewidth=1) 
        axs[3].plot(year, roc, color=color_list[i], linewidth=1) 
        i+=1
    # """


    # """
    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------
    fname = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Keeling_curve/monthly_in_situ_co2_mlo.csv'
    data = pd.read_csv(fname)
    #### 1958 to 2024
    year = np.arange(1958, 2024)
    data = np.mean(np.array(data.iloc[:,8]).astype('float').reshape(-1, 12), axis=1)[:-1]
    year, data_inc = separate_abs_roc_yty(data, year, 5)
    axs[2].plot(year, data_inc * 16800)



    # ----------------------------------------------------------------------------------------------------------------------
    axs[0].set_xlim(1980, 2050)
    # axs[0].set_xlim(2010, 2050)
    plt.show()
    plt.clf() 