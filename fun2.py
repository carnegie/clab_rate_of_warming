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

import pandas as pd, numpy as np 
from Info_func import temperature_detrend


def raw_temperature(dfTemp, axs): 


    # ----------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------

    def plot_one_case(fit_choice, window_size, color_opts, ls):

        #### Get only current policy with no nz committeement scenairos
        dfTemp_current_policies = dfTemp[dfTemp['model'] == 'Current_policies'] 
        dfTemp_current_policies = dfTemp_current_policies[dfTemp_current_policies['scenario'].str.contains('KyotoFromPrice')]

        flagNz = True; caseNz = 'nz'
        flagEmissions = True; caseEmissions = 'Median'
        flagModels = False ; caseModels = 'MESSAGE'
        flagPrice = False; casePrice = 'incrate2'
        xaxis = np.arange(1850, 2101, 1)

        lw = 1.0

        if fit_choice == 1 and window_size == 33:

            lw = 1.5

            # ----------------------------------------------------------------------------------------------------------------------
            dfTemp_uncertainty0 = dfTemp_current_policies
            if flagNz == True: dfTemp_uncertainty0 = dfTemp_uncertainty0[~dfTemp_uncertainty0['scenario'].str.contains(caseNz)]
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
            peak_rate_warming = []
            for i in range(to_plot_uncertainty0.shape[0]):
                tas = to_plot_uncertainty0[i]
                year, tas_detrended = temperature_detrend(tas, xaxis, window_size)
                roc_2008_2030 = tas_detrended[2008-year[0]:2030-year[0]]
                year_2008_2030 = year[2008-year[0]:2030-year[0]]
                max_2008_2030 = np.argmax(roc_2008_2030)
                peak_rate_warming.append(year_2008_2030[max_2008_2030])
                if i == 0: roc_stack = np.array(tas_detrended)
                if i != 0: roc_stack = np.vstack((roc_stack, np.array(tas_detrended)))
            max_roc, min_roc = np.max(roc_stack, axis=0), np.min(roc_stack, axis=0)
            axs.fill_between(year, max_roc, min_roc, color=color_opts, alpha=0.1)
            print ()
            print ('peak rate of warming')
            print (np.max(peak_rate_warming), np.min(peak_rate_warming))

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
                year, tas_detrended = temperature_detrend(tas, xaxis, window_size)
                if i == 0: roc_stack = np.array(tas_detrended)
                if i != 0: roc_stack = np.vstack((roc_stack, np.array(tas_detrended)))
            max_roc, min_roc = np.max(roc_stack, axis=0), np.min(roc_stack, axis=0)
            axs.fill_between(year, max_roc, min_roc, color=color_opts, alpha=0.3)

        # ----------------------------------------------------------------------------------------------------------------------
        #### Best estimate cases: 
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
            year, tas_detrended = temperature_detrend(tas, xaxis, window_size)
            axs.plot(year, tas_detrended, color=color_opts, linewidth=lw, linestyle=ls)
        
        if fit_choice == 1 and window_size == 33:
            arg_2025, arg_2050 = np.argmin(np.abs(year-2025)), np.argmin(np.abs(year-2050))
            print ()
            print (year[arg_2025], year[arg_2050])
            print (tas_detrended[arg_2025], tas_detrended[arg_2050]) 

    plot_one_case(1, 33, 'red', '-')
    plot_one_case(1, 17, 'blue', '--')