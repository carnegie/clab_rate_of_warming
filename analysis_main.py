

import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':

    ##################################
    #### Control area 
    ##################################
    
    fig, axs = plt.subplots(2, 1, figsize = [6, 10], sharex = False, sharey = False, constrained_layout = True) 
    axs = axs.flatten()

    data_path = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Rogelj_et_al_2023/'
    csv_temp_name = '2023_emission_gap_temp_summary_data.csv'
    dfTemp = pd.read_csv(data_path + csv_temp_name)
    csv_emis_name = 'infilled_extended_and_infilled_unep_23.65.csv'
    dfEmis = pd.read_csv(data_path + csv_emis_name)


    from fun1 import roc_time_series
    roc_time_series(dfTemp, axs[0])

    # from fun2 import roc_attribution
    # roc_attribution(dfTemp, dfEmis, axs[1])

    from fun3 import roc_rw_data
    roc_rw_data(axs[1])


    axs[0].set_xlim(1980, 2050)
    axs[0].set_ylim(-0.01, 0.05)

    axs[1].set_xlim(1980, 2050)
    # axs[1].legend(loc = 'upper left', fontsize = 8)
    # plt.show()
    plt.savefig('main.ps')
    plt.clf() 









    # from fun2 import check_filter_scenarios
    # check_filter_scenarios(dfTemp, dfEmis)







