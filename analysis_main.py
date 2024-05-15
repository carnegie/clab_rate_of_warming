import pandas as pd
import matplotlib.pyplot as plt
from fun1 import roc_time_series

if __name__ == '__main__':

    axs = plt.subplot(111)

    data_path = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Rogelj_et_al_2023/'
    csv_temp_name = '2023_emission_gap_temp_summary_data.csv'
    dfTemp = pd.read_csv(data_path + csv_temp_name)
    roc_time_series(dfTemp, axs)

    axs.set_xlim(1980, 2050)
    axs.set_ylim(-0.01, 0.05)
    plt.show()
    # plt.savefig('main.ps')
    plt.clf() 