import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from Info_func import separate_abs_roc

def analysis_figure2(): 
    
    csv_file_name = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Rogelj_et_al_2023/2023_emission_gap_temp_summary_data.csv'
    df = pd.read_csv(csv_file_name)

    lowpass_threshold = 0
    window_size = 40
    start_year = 1980 
    end_year = 2050

    # ----------------------------------------------------------------------------------------------------------------------
    #### Figure 2
    #### Get the time of peak warming
    #### Get the rate of warming changing rate
    #### Are there any relationships with peak warming level? 

    fig, axs = plt.subplots(2, 3, figsize = [12, 5], sharex = True, constrained_layout = True) 
    axs = axs.ravel()
    axs[1].get_shared_y_axes().join(axs[0], axs[1], axs[2])
    axs[4].get_shared_y_axes().join(axs[3], axs[4], axs[5])
    xaxis = np.arange(2100-1850+1) + 1850

    #### Only cases with the string "KyotoFromPrice" in names 
    df_current_policies = df[df['model'] == 'Current_policies'] 
    df_current_policies_l0 = df_current_policies[df_current_policies['scenario'].str.contains('KyotoFromPrice')]
    uncertainty0 = df_current_policies_l0[df_current_policies_l0['scenario'].str.contains('MESSAGE')]
    uncertainty0 = np.array(uncertainty0.iloc[:, 3:])

    #### Let's sub-select based on the peak warming level 
    less2C = uncertainty0[np.max(uncertainty0, axis=1)<=2, :] 
    less3C = uncertainty0[(np.max(uncertainty0, axis=1)<=3)&(np.max(uncertainty0, axis=1)>2), :] 
    more3C = uncertainty0[np.max(uncertainty0, axis=1)>3, :] 
    for i in range(less2C.shape[0]):
        this_entry = less2C[i]
        tas, roc = separate_abs_roc(this_entry, lowpass_threshold, window_size)
        axs[0].plot(xaxis, tas, color='green', linewidth=0.5, alpha=0.5)
        axs[3].plot(xaxis[window_size-1:], roc, color='green', linewidth=0.5, alpha=0.5)
    for i in range(less3C.shape[0]):
        this_entry = less3C[i]
        tas, roc = separate_abs_roc(this_entry, lowpass_threshold, window_size)
        axs[1].plot(xaxis, tas, color='orange', linewidth=0.5, alpha=0.5)
        axs[4].plot(xaxis[window_size-1:], roc, color='orange', linewidth=0.5, alpha=0.5)
    for i in range(more3C.shape[0]):
        this_entry = more3C[i]
        tas, roc = separate_abs_roc(this_entry, lowpass_threshold, window_size)
        axs[2].plot(xaxis, tas, color='red', linewidth=0.5, alpha=0.5)
        axs[5].plot(xaxis[window_size-1:], roc, color='red', linewidth=0.5, alpha=0.5)

    axs[0].set_xlim(1980, 2100)
    # axs[0].set_ylim(0, 2.5)
    # axs[0].set_ylim(0, 0.035)
    plt.show()
    plt.clf() 