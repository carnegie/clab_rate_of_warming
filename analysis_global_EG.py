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

def analysis_global_EG(): 
    
    csv_file_name = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Rogelj_et_al_2023/2023_emission_gap_temp_summary_data.csv'
    df = pd.read_csv(csv_file_name)

    lowpass_threshold = 0
    window_size = 40

    # ----------------------------------------------------------------------------------------------------------------------
    #### Case 1: current policy case 

    ### Central case only:
    ### 1. no nz;
    ### 2. Median emissions;
    ### 3. 2% growth rate 
    ### 4. 0.5 percentile 
    # df_current_policies = df[df['model'] == 'Current_policies'] 
    # df_current_policies_l1 = df_current_policies[~df_current_policies['scenario'].str.contains('nz')]
    # df_current_policies_l2 = df_current_policies_l1[df_current_policies_l1['scenario'].str.contains('Median')]
    # df_current_policies_l3 = df_current_policies_l2[df_current_policies_l2['scenario'].str.contains('incrate2')]
    # df_current_policies_l4 = df_current_policies_l3[df_current_policies_l3['quantile'] == 0.5]
    # to_plot = np.array(df_current_policies_l4.iloc[:, 3:])
    # scenario_names = list(df_current_policies_l4['scenario'])
    # scenario_names_unique = df_current_policies_l4['scenario'].unique() 

    ### Remvoing nz limitation:
    # df_current_policies = df[df['model'] == 'Current_policies'] 
    # df_current_policies_l2 = df_current_policies[df_current_policies['scenario'].str.contains('Median')]
    # df_current_policies_l3 = df_current_policies_l2[df_current_policies_l2['scenario'].str.contains('incrate2')]
    # df_current_policies_l4 = df_current_policies_l3[df_current_policies_l3['quantile'] == 0.5]
    # to_plot = np.array(df_current_policies_l4.iloc[:, 3:])
    # scenario_names = list(df_current_policies_l4['scenario'])
    # scenario_names_unique = df_current_policies_l4['scenario'].unique() 

    ### Remvoing Median emission limit 
    # df_current_policies = df[df['model'] == 'Current_policies'] 
    # df_current_policies_l3 = df_current_policies[df_current_policies['scenario'].str.contains('incrate2')]
    # df_current_policies_l4 = df_current_policies_l3[df_current_policies_l3['quantile'] == 0.5]
    # to_plot = np.array(df_current_policies_l4.iloc[:, 3:])
    # scenario_names = list(df_current_policies_l4['scenario'])
    # scenario_names_unique = df_current_policies_l4['scenario'].unique() 

    ## Remvoing growth rate limit 
    # df_current_policies = df[df['model'] == 'Current_policies'] 
    # df_current_policies_l4 = df_current_policies[df_current_policies['quantile'] == 0.5]
    # to_plot = np.array(df_current_policies_l4.iloc[:, 3:])
    # scenario_names = list(df_current_policies_l4['scenario'])
    # scenario_names_unique = df_current_policies_l4['scenario'].unique() 

    # ### Remvoing the quantile limit 
    df_current_policies = df[df['model'] == 'Current_policies'] 
    df_current_policies_l3 = df_current_policies[df_current_policies['scenario'].str.contains('incrate1')]
    df_current_policies_l4 = df_current_policies_l3[df_current_policies_l3['quantile'] == 0.9]
    to_plot = np.array(df_current_policies_l4.iloc[:, 3:])
    scenario_names = list(df_current_policies_l4['scenario'])
    scenario_names_unique = df_current_policies_l4['scenario'].unique() 


    #### So max/median/min has some impact
    #### increase rate little impact 
    # print ()
    print ()
    print (scenario_names) 
    # stop 


    ### Remove all limitations
    # df_current_policies = df[df['model'] == 'Current_policies'] 
    # to_plot = np.array(df_current_policies.iloc[:, 3:])
    # scenario_names = list(df_current_policies['scenario'])
    # scenario_names_unique = df_current_policies['scenario'].unique() 


    fig, axs = plt.subplots(2, 1, figsize = [5, 8], sharex = True, sharey = False, constrained_layout = True) 
    xaxis = np.arange(2100-1850+1) + 1850
    for i in range(to_plot.shape[0]):
        this_entry = to_plot[i]
        tas, roc_tas = separate_abs_roc(this_entry, lowpass_threshold, window_size)
        axs[0].plot(xaxis, tas, linewidth=0.5)
        axs[1].plot(xaxis[window_size-1:], roc_tas, linewidth=0.5)
    # axs[0].set_xlim([1980, 2050])
    # axs[1].set_xlim([1980, 2050])
    plt.show()
    plt.clf() 





"""
Current policy: 
'Max_Harmonized_KyotoFromPrice_incrate0_GCAM_4-2_SSP2.csv', 
'Max_Harmonized_KyotoFromPrice_incrate0_REMIND-MAgPIE_1-5__SSP2.csv', 
'Max_Harmonized_KyotoFromPrice_incrate0_WITCH-GLOBIOM_3-1_SSP2.csv', 
'Max_Harmonized_KyotoFromPrice_incrate1_GCAM_4-2_SSP2.csv', 
'Max_Harmonized_KyotoFromPrice_incrate2_GCAM_4-2_SSP2.csv', 
'Max_Harmonized_KyotoFromPrice_prescribed_GCAM_4-2_SSP2.csv', 
'Median_Harmonized_KyotoFromPrice_incrate0_GCAM_4-2_SSP2.csv', 
'Median_Harmonized_KyotoFromPrice_incrate0_WITCH-GLOBIOM_3-1_SSP2.csv', 
'Median_Harmonized_KyotoFromPrice_incrate1_GCAM_4-2_SSP2.csv']
"""
