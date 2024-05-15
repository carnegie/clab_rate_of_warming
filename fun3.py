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
from Info_func import separate_abs_roc_regression
from Info_func import separate_abs_roc_yty_detrend
from Info_func import get_rw_data

def roc_rw_data(axs): 

    fit_choice = 1
    window_size = 17

    obs_data_path = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Others/'
    BE, GISS, HadCRUT5, NOAA, ERA5 = get_rw_data(obs_data_path)
    color_list = ['green', 'brown', 'orange', 'purple', 'pink', 'gray', 'cyan']

    i = 1
    year_obs = np.arange(1980, 2024) 
    for obs_i in [BE, GISS, HadCRUT5, NOAA, ERA5]: 
        tas = obs_i
        if fit_choice == 0:
            year, roc = separate_abs_roc_regression(tas, year_obs, window_size) 
        if fit_choice == 1:
            year, roc = separate_abs_roc_yty_detrend(tas, year_obs, window_size) 
        axs.plot(year, roc, color=color_list[i], linewidth=1) 
        i+=1
