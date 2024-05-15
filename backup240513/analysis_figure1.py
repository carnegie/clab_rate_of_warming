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
from Info_func import separate_abs_roc
from Info_func import interpolate_emissions




















def temp_filter_scenarios(dfIn):

    lowpass_threshold = 0
    window_size = 40
    start_year = 1980 
    end_year = 2050

    # ----------------------------------------------------------------------------------------------------------------------
    #### Figure 1
    #### p1: Emissions of Kyoto gases; 
    #### p2: Absolute temperature change;
    #### p3: Rate of wraming 

    fig, axs = plt.subplots(2, 1, figsize = [5, 8], sharex = True, sharey = False, constrained_layout = True) 
    xaxis = np.arange(2100-1850+1) + 1850

    df_current_policies = dfIn[dfIn['model'] == 'Current_policies'] 
    df_current_policies_l0 = df_current_policies[df_current_policies['scenario'].str.contains('KyotoFromPrice')]
    df_current_policies_l1 = df_current_policies_l0[~df_current_policies_l0['scenario'].str.contains('nz')]
    # df_current_policies_l1 = df_current_policies_l0[df_current_policies_l0['scenario'].str.contains('nz')]
    
    # #### (0) Full uncertainty range for the model MESSAGE:
    # uncertainty0 = df_current_policies_l1[df_current_policies_l1['scenario'].str.contains('MESSAGE')]
    # uncertainty0 = np.array(uncertainty0.iloc[:, 3:])
    # peak_roc_year = [] 
    # for i in range(uncertainty0.shape[0]):
    #     this_entry = uncertainty0[i]
    #     tas, roc = separate_abs_roc(this_entry, lowpass_threshold, window_size)
    #     #### Now roc start from 1889 to 2100 
    #     peak_roc_year.append(np.argmax(roc[start_year-1889:end_year-1889+1]))
    #     if i == 0: tas_stack, roc_stack = np.array(tas), np.array(roc)
    #     if i != 0: tas_stack, roc_stack = np.vstack((tas_stack, np.array(tas))), np.vstack((roc_stack, np.array(roc)))
    # max_tas = np.max(tas_stack, axis=0)
    # min_tas = np.min(tas_stack, axis=0)
    # max_roc = np.max(roc_stack, axis=0)
    # min_roc = np.min(roc_stack, axis=0)
    # axs[0].fill_between(xaxis, max_tas, min_tas, color='royalblue', alpha=0.1)
    # axs[1].fill_between(xaxis[window_size-1:], max_roc, min_roc, color='royalblue', alpha=0.1)
    # #### Find where the peak warming is
    # peak_roc_year = np.array(peak_roc_year)
    # min_boundary, max_boundary = np.min(peak_roc_year) + 1980, np.max(peak_roc_year) + 1980
    # axs[1].fill_betweenx([0, 0.035], [min_boundary, min_boundary], [max_boundary, max_boundary], color='firebrick', alpha=0.2)

    # #### (1) Constant emission uncertainty 
    # uncertainty1 = df_current_policies_l1[df_current_policies_l1['scenario'].str.contains('MESSAGE')]
    # uncertainty1 = uncertainty1[uncertainty1['quantile'] == 0.5]
    # uncertainty1 = np.array(uncertainty1.iloc[:, 3:])
    # for i in range(uncertainty1.shape[0]):
    #     this_entry = uncertainty1[i]
    #     tas, roc = separate_abs_roc(this_entry, lowpass_threshold, window_size)
    #     if i == 0: tas_stack, roc_stack = np.array(tas), np.array(roc)
    #     if i != 0: tas_stack, roc_stack = np.vstack((tas_stack, np.array(tas))), np.vstack((roc_stack, np.array(roc)))
    # max_tas = np.max(tas_stack, axis=0)
    # min_tas = np.min(tas_stack, axis=0)
    # max_roc = np.max(roc_stack, axis=0)
    # min_roc = np.min(roc_stack, axis=0)
    # axs[0].fill_between(xaxis, max_tas, min_tas, color='royalblue', alpha=0.5)
    # axs[1].fill_between(xaxis[window_size-1:], max_roc, min_roc, color='royalblue', alpha=0.5)

    #### (2) Best estimate cases: 
    ####    1.1. Current policy no net zero targets 
    ####    1.2. Median emissions 
    ####    1.3. 2% increasing rate
    ####    1.4. MESSAGE model for emission projections 
    ####    1.5. 0.5 percentiles
    best_estimate = df_current_policies_l1[df_current_policies_l1['scenario'].str.contains('Median')]
    best_estimate = best_estimate[best_estimate['scenario'].str.contains('incrate2')]
    # best_estimate = best_estimate[best_estimate['scenario'].str.contains('MESSAGE')] 
    # best_estimate = best_estimate[best_estimate['scenario'].str.contains('MESSAGE')] 
    best_estimate = best_estimate[best_estimate['scenario'].str.contains('AIM')] 
    best_estimate = best_estimate[best_estimate['quantile'] == 0.5]
    best_estimate = np.array(best_estimate.iloc[:, 3:])
    for i in range(best_estimate.shape[0]): 
        this_entry = best_estimate[i]
        tas, roc_tas = separate_abs_roc(this_entry, lowpass_threshold, window_size)
        # axs[0].plot(xaxis, tas, color='black', linewidth=1.5)
        # axs[1].plot(xaxis[window_size-1:], roc_tas, color='black', linewidth=1.5)
        print () 
        print (xaxis[160:]) 
        print (tas[160:]) 

    # scenario_names = list(data_to_plot['scenario'])
    # scenario_names_unique = data_to_plot['scenario'].unique() 
    # print (scenario_names_unique)
    # stop 

    # axs[0].set_xlim(2010, 2050)
    # # axs[0].set_xlim(1980, 2050)
    # # axs[0].set_xlim(1850, 2050)
    # axs[0].set_ylim(0, 2.5)
    # axs[1].set_ylim(0, 0.035)
    # plt.show()
    # plt.clf() 













def comb_filter_scenarios(dfTemp, dfEmis): 


    lowpass_threshold = 0
    window_size = 40
    start_year = 1980 
    end_year = 2050

    fig, axs = plt.subplots(2, 2, figsize = [10, 10], sharex = True, sharey = False, constrained_layout = True) 
    axs = axs.flatten()
    xaxis = np.arange(2100-1850+1) + 1850

    # ----------------------------------------------------------------------------------------------------------------------
    #### Get only current policy with no nz committeement scenairos
    dfTemp_current_policies = dfTemp[dfTemp['model'] == 'Current_policies'] 
    dfTemp_current_policies_l0 = dfTemp_current_policies[dfTemp_current_policies['scenario'].str.contains('KyotoFromPrice')]
    dfTemp_current_policies_l1 = dfTemp_current_policies_l0[~dfTemp_current_policies_l0['scenario'].str.contains('nz')]
    dfTemp_scenario_names_unique = list(dfTemp_current_policies_l1['scenario'].unique())
    dfTemp_scenario_names_unique = [s.replace('.csv', '').replace('-', '_') for s in dfTemp_scenario_names_unique]

    dfEmis_current_policies = dfEmis[dfEmis['Model'] == 'Current policies']
    dfEmis_current_policies_l0 = dfEmis_current_policies[dfEmis_current_policies['Scenario'].str.contains('KyotoFromPrice')]
    dfEmis_current_policies_l1 = dfEmis_current_policies_l0[~dfEmis_current_policies_l0['Scenario'].str.contains('nz')]
    dfEmis_scenario_names_unique = list(dfEmis_current_policies_l1['Scenario'].unique())
    dfEmis_scenario_names_unique = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in dfEmis_scenario_names_unique]

    #### Let's first make sure scenarios are consistent 
    print ()
    print ()
    print (len(dfTemp_scenario_names_unique))
    print (len(dfEmis_scenario_names_unique))
    diff_list = []
    for i in dfTemp_scenario_names_unique:
        if i not in dfEmis_scenario_names_unique: diff_list.append(i)
    if len(diff_list) == 0:
        print ('same sceniarios between emissions and temperature change')
    else:
        print ('different scenarios: ', len(diff_list), ' will stop now')
        stop 


    # ----------------------------------------------------------------------------------------------------------------------
    #### (0) Full uncertainty range for the model MESSAGE:
    dfTemp_uncertainty0 = dfTemp_current_policies_l1[dfTemp_current_policies_l1['scenario'].str.contains('MESSAGE')]
    dfTemp_uncertainty0 = dfTemp_uncertainty0[dfTemp_uncertainty0['scenario'].str.contains('MESSAGE')]
    dfTemp_uncertainty0 = np.array(dfTemp_uncertainty0.iloc[:, 3:])
    peak_roc_year = [] 
    for i in range(dfTemp_uncertainty0.shape[0]):
        this_entry = dfTemp_uncertainty0[i]
        tas, roc = separate_abs_roc(this_entry, lowpass_threshold, window_size)
        tas = tas - tas[160]
        #### Now roc start from 1889 to 2100 
        peak_roc_year.append(np.argmax(roc[start_year-1889:end_year-1889+1]))
        if i == 0: tas_stack, roc_stack = np.array(tas), np.array(roc)
        if i != 0: tas_stack, roc_stack = np.vstack((tas_stack, np.array(tas))), np.vstack((roc_stack, np.array(roc)))
    max_tas = np.max(tas_stack, axis=0)
    min_tas = np.min(tas_stack, axis=0)
    max_roc = np.max(roc_stack, axis=0)
    min_roc = np.min(roc_stack, axis=0)
    axs[1].fill_between(xaxis, max_tas, min_tas, color='royalblue', alpha=0.1)
    axs[3].fill_between(xaxis[window_size-1:], max_roc, min_roc, color='royalblue', alpha=0.1)
    # #### Find where the peak warming is
    # peak_roc_year = np.array(peak_roc_year)
    # min_boundary, max_boundary = np.min(peak_roc_year) + 1980, np.max(peak_roc_year) + 1980
    # axs[3].fill_betweenx([0, 0.035], [min_boundary, min_boundary], [max_boundary, max_boundary], color='firebrick', alpha=0.2)

    # ----------------------------------------------------------------------------------------------------------------------
    #### (1) Constant emission uncertainty 
    dfTemp_uncertainty1 = dfTemp_current_policies_l1[dfTemp_current_policies_l1['scenario'].str.contains('MESSAGE')]
    dfTemp_uncertainty1 = dfTemp_uncertainty1[dfTemp_uncertainty1['quantile'] == 0.5]
    dfTemp_uncertainty1 = np.array(dfTemp_uncertainty1.iloc[:, 3:])
    for i in range(dfTemp_uncertainty1.shape[0]):
        this_entry = dfTemp_uncertainty1[i]
        tas, roc = separate_abs_roc(this_entry, lowpass_threshold, window_size)
        tas = tas - tas[160]
        if i == 0: tas_stack, roc_stack = np.array(tas), np.array(roc)
        if i != 0: tas_stack, roc_stack = np.vstack((tas_stack, np.array(tas))), np.vstack((roc_stack, np.array(roc)))
    max_tas = np.max(tas_stack, axis=0)
    min_tas = np.min(tas_stack, axis=0)
    max_roc = np.max(roc_stack, axis=0)
    min_roc = np.min(roc_stack, axis=0)
    axs[1].fill_between(xaxis, max_tas, min_tas, color='royalblue', alpha=0.5)
    axs[3].fill_between(xaxis[window_size-1:], max_roc, min_roc, color='royalblue', alpha=0.5)

    dfEmis_uncertainty1 = dfEmis_current_policies_l1[dfEmis_current_policies_l1['Scenario'].str.contains('MESSAGE')]
    dfEmis_uncertainty1_CO2 = dfEmis_uncertainty1[dfEmis_uncertainty1['Variable'] == 'Emissions|CO2']
    dfEmis_uncertainty1_CO2 = np.array(dfEmis_uncertainty1_CO2.iloc[:, 5:])
    dfEmis_uncertainty1_CO2eq = dfEmis_uncertainty1[dfEmis_uncertainty1['Variable'] == 'Emissions|Kyoto Gases (AR6-GWP100)']
    dfEmis_uncertainty1_CO2eq = np.array(dfEmis_uncertainty1_CO2eq.iloc[:, 5:])
    for i in range(dfEmis_uncertainty1_CO2.shape[0]):
        x_fine, y_fine_CO2 = interpolate_emissions(dfEmis_uncertainty1_CO2[i])
        x_fine, y_fine_CO2eq = interpolate_emissions(dfEmis_uncertainty1_CO2eq[i])
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
    #### (2) Best estimate cases: 
    ####    1.1. Current policy no net zero targets 
    ####    1.2. Median emissions 
    ####    1.3. 2% increasing rate
    ####    1.4. MESSAGE model for emission projections 
    ####    1.5. 0.5 percentiles
    dfTemp_best_estimate = dfTemp_current_policies_l1[dfTemp_current_policies_l1['scenario'].str.contains('Median')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('incrate2')]
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['scenario'].str.contains('MESSAGE')] 
    dfTemp_best_estimate = dfTemp_best_estimate[dfTemp_best_estimate['quantile'] == 0.5]
    dfTemp_best_estimate = np.array(dfTemp_best_estimate.iloc[:, 3:])
    for i in range(dfTemp_best_estimate.shape[0]): 
        this_entry = dfTemp_best_estimate[i]
        tas, roc_tas = separate_abs_roc(this_entry, lowpass_threshold, window_size)
        tas = tas - tas[160]
        axs[1].plot(xaxis, tas, color='black', linewidth=1.5)
        axs[3].plot(xaxis[window_size-1:], roc_tas, color='black', linewidth=1.5)
        
    dfEmis_best_estimate = dfEmis_current_policies_l1[dfEmis_current_policies_l1['Scenario'].str.contains('Median')]
    dfEmis_best_estimate = dfEmis_best_estimate[dfEmis_best_estimate['Scenario'].str.contains('incrate2')]
    dfEmis_best_estimate = dfEmis_best_estimate[dfEmis_best_estimate['Scenario'].str.contains('MESSAGE')]
    dfEmis_best_estimate_CO2 = dfEmis_best_estimate[dfEmis_best_estimate['Variable'] == 'Emissions|CO2']
    dfEmis_best_estimate_CO2 = np.array(dfEmis_best_estimate_CO2.iloc[:, 5:])
    dfEmis_best_estimate_CO2eq = dfEmis_best_estimate[dfEmis_best_estimate['Variable'] == 'Emissions|Kyoto Gases (AR6-GWP100)']
    dfEmis_best_estimate_CO2eq = np.array(dfEmis_best_estimate_CO2eq.iloc[:, 5:])
    for i in range(dfEmis_best_estimate_CO2.shape[0]): 
        x_fine, y_fine_CO2 = interpolate_emissions(dfEmis_best_estimate_CO2[i])
        x_fine, y_fine_CO2eq = interpolate_emissions(dfEmis_best_estimate_CO2eq[i])
        axs[2].plot(x_fine, y_fine_CO2, color='r', linewidth=1.5)
        axs[2].plot(x_fine, y_fine_CO2eq, color='b', linewidth=1.5)
        cumulative_y_fine_CO2 = np.cumsum(y_fine_CO2)
        cumulative_y_fine_CO2eq = np.cumsum(y_fine_CO2eq)
        axs[0].plot(x_fine, cumulative_y_fine_CO2, color='r', linewidth=1.5)
        axs[0].plot(x_fine, cumulative_y_fine_CO2eq, color='b', linewidth=1.5)

    # ----------------------------------------------------------------------------------------------------------------------
    axs[0].set_xlim(2010, 2050)
    plt.show()
    plt.clf() 





def timing_filter_scenarios(dfTemp, dfEmis): 

    lowpass_threshold = 0
    # window_size = 40
    window_size = 30
    start_year = 1980 
    end_year = 2050

    
    xaxis = np.arange(2100-1850+1) + 1850

    # ----------------------------------------------------------------------------------------------------------------------
    #### Get only current policy with no nz committeement scenairos
    dfTemp_current_policies = dfTemp[dfTemp['model'] == 'Current_policies'] 
    dfTemp_current_policies_l0 = dfTemp_current_policies[dfTemp_current_policies['scenario'].str.contains('KyotoFromPrice')]
    dfTemp_current_policies_l1 = dfTemp_current_policies_l0[~dfTemp_current_policies_l0['scenario'].str.contains('nz')]

    dfEmis_current_policies = dfEmis[dfEmis['Model'] == 'Current policies']
    dfEmis_current_policies_l0 = dfEmis_current_policies[dfEmis_current_policies['Scenario'].str.contains('KyotoFromPrice')]
    dfEmis_current_policies_l1 = dfEmis_current_policies_l0[~dfEmis_current_policies_l0['Scenario'].str.contains('nz')]

    # ----------------------------------------------------------------------------------------------------------------------
    #### (1) Constant emission uncertainty 
    # dfTemp_uncertainty1 = dfTemp_current_policies_l1[dfTemp_current_policies_l1['scenario'].str.contains('MESSAGE')]
    dfTemp_uncertainty1 = dfTemp_current_policies_l1[dfTemp_current_policies_l1['scenario'].str.contains('Median')]
    dfTemp_uncertainty1 = dfTemp_uncertainty1[dfTemp_uncertainty1['quantile'] == 0.5]
    dfTemp_scenario_names_unique = list(dfTemp_uncertainty1['scenario'].unique())
    dfTemp_scenario_names_unique = [s.replace('.csv', '').replace('-', '_') for s in dfTemp_scenario_names_unique]
    dfTemp_uncertainty1 = np.array(dfTemp_uncertainty1.iloc[:, 3:])

    # dfEmis_uncertainty1 = dfEmis_current_policies_l1[dfEmis_current_policies_l1['Scenario'].str.contains('MESSAGE')]
    dfEmis_uncertainty1 = dfEmis_current_policies_l1[dfEmis_current_policies_l1['Scenario'].str.contains('Median')]
    dfEmis_scenario_names_unique = list(dfEmis_uncertainty1['Scenario'].unique())
    dfEmis_scenario_names_unique = [s.replace('|', '_').replace('/', '_').replace(' ', '_').replace('.', '_').replace('*', '_').replace('-', '_') for s in dfEmis_scenario_names_unique]
    dfEmis_uncertainty1_CO2 = dfEmis_uncertainty1[dfEmis_uncertainty1['Variable'] == 'Emissions|CO2']
    dfEmis_uncertainty1_CO2 = np.array(dfEmis_uncertainty1_CO2.iloc[:, 5:])
    dfEmis_uncertainty1_CO2eq = dfEmis_uncertainty1[dfEmis_uncertainty1['Variable'] == 'Emissions|Kyoto Gases (AR6-GWP100)']
    dfEmis_uncertainty1_CO2eq = np.array(dfEmis_uncertainty1_CO2eq.iloc[:, 5:])
    

    # fig, axs = plt.subplots(2, 1, figsize = [5, 10], sharex = True, sharey = False, constrained_layout = True) 
    # axs = axs.flatten()
    for i in range(dfTemp_uncertainty1.shape[0]):
        this_entry = dfTemp_uncertainty1[i]
        tas, roc = separate_abs_roc(this_entry, lowpass_threshold, window_size)
        xaxis_roc = xaxis[window_size-1:]
        args_max_roc = np.argmax(roc[:-50])
        year_max_roc = xaxis_roc[args_max_roc]

        x_fine, y_fine_CO2 = interpolate_emissions(dfEmis_uncertainty1_CO2[i])
        x_fine, y_fine_CO2eq = interpolate_emissions(dfEmis_uncertainty1_CO2eq[i])
        args_max_CO2 = np.argmax(y_fine_CO2)
        year_max_CO2 = x_fine[args_max_CO2]
        args_max_CO2eq = np.argmax(y_fine_CO2eq)
        year_max_CO2eq = x_fine[args_max_CO2eq]

        print ()
        print (dfTemp_scenario_names_unique[i])
        print (dfEmis_scenario_names_unique[i])
        print (year_max_roc, year_max_CO2, year_max_CO2eq) 

        fig, axs = plt.subplots(2, 1, figsize = [5, 10], sharex = True, sharey = False, constrained_layout = True) 
        axs = axs.flatten()
        axs[0].plot(xaxis, tas, color='black', linewidth=1.5)
        # axs[0].plot(xaxis[window_size-1:], roc, color='black', linewidth=1.5) 
        axs[1].plot(x_fine, y_fine_CO2, color='r', linewidth=1.5)
        axs[1].plot(x_fine, y_fine_CO2eq, color='b', linewidth=1.5)
        axs[1].plot(x_fine, y_fine_CO2eq-y_fine_CO2, color='green', linewidth=1.5)
        axs[0].set_xlim(2010, 2050)
        # axs[0].set_ylim(1.0, 2.0)
        axs[1].set_xlim(2010, 2050)
        axs[1].set_yscale('log')
        plt.show()
        plt.clf() 

    
    
    
    
    
    
    
    
    # for i in range(dfEmis_uncertainty1_CO2.shape[0]):
    #     x_fine, y_fine_CO2 = interpolate_emissions(dfEmis_uncertainty1_CO2[i])
    #     x_fine, y_fine_CO2eq = interpolate_emissions(dfEmis_uncertainty1_CO2eq[i])
    #     if i == 0: co2_stack, co2eq_stack = np.array(y_fine_CO2), np.array(y_fine_CO2eq)
    #     if i != 0: co2_stack, co2eq_stack = np.vstack((co2_stack, np.array(y_fine_CO2))), np.vstack((co2eq_stack, np.array(y_fine_CO2eq)))
    #     cumulative_y_fine_CO2 = np.cumsum(y_fine_CO2)
    #     cumulative_y_fine_CO2eq = np.cumsum(y_fine_CO2eq)
    #     if i == 0: cumulative_co2_stack, cumulative_co2eq_stack = np.array(cumulative_y_fine_CO2), np.array(cumulative_y_fine_CO2eq)
    #     if i != 0: cumulative_co2_stack, cumulative_co2eq_stack = np.vstack((cumulative_co2_stack, np.array(cumulative_y_fine_CO2))), np.vstack((cumulative_co2eq_stack, np.array(cumulative_y_fine_CO2eq)))
    # max_co2 = np.max(co2_stack, axis=0)
    # min_co2 = np.min(co2_stack, axis=0)
    # max_co2eq = np.max(co2eq_stack, axis=0)
    # min_co2eq = np.min(co2eq_stack, axis=0)
    # axs[2].fill_between(x_fine, max_co2, min_co2, color='r', alpha=0.5)
    # axs[2].fill_between(x_fine, max_co2eq, min_co2eq, color='b', alpha=0.5)
    # max_cumulative_co2 = np.max(cumulative_co2_stack, axis=0)
    # min_cumulative_co2 = np.min(cumulative_co2_stack, axis=0)
    # max_cumulative_co2eq = np.max(cumulative_co2eq_stack, axis=0)
    # min_cumulative_co2eq = np.min(cumulative_co2eq_stack, axis=0)
    # axs[0].fill_between(x_fine, max_cumulative_co2, min_cumulative_co2, color='r', alpha=0.5)
    # axs[0].fill_between(x_fine, max_cumulative_co2eq, min_cumulative_co2eq, color='b', alpha=0.5)

    # # ----------------------------------------------------------------------------------------------------------------------
    # axs[0].set_xlim(2010, 2050)
    # plt.show()
    # plt.clf() 








def analysis_figure1(): 

    data_path = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Rogelj_et_al_2023/'

    csv_temp_name = '2023_emission_gap_temp_summary_data.csv'
    dfTemp = pd.read_csv(data_path + csv_temp_name)
    # temp_filter_scenarios(dfTemp)
    # stop 
    csv_emis_name = 'infilled_extended_and_infilled_unep_23.65.csv'
    dfEmis = pd.read_csv(data_path + csv_emis_name)
    # comb_filter_scenarios(dfTemp, dfEmis)
    timing_filter_scenarios(dfTemp, dfEmis)