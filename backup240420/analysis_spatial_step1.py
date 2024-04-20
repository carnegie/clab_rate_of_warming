
"""

A few variables to calculate:

1. Maximum absolute temperature
2. Year of maximum absolute temperature
3. Maximum rate of change of temperature
4. Year of maximum rate of change of temperature


Maybe for each model, create 1 file to store all four variables:

    tas = (250, 64, 128)
    roc_tas = (250-31, 64, 128)

"""


from SUB_Class_CMIP6 import CMIP6_models
from SUB_Class_CMIP6 import set_class_instance
from Info_func import info_func
from Info_func import lowpass_filter
from Info_func import separate_abs_roc

import cdms2 as cdms
import cdutil 
import numpy as np 
import pickle
import pandas as pd
import csv

def analysis_spatial(scenario_list):

    set_class_instance()
    info_dict = info_func()
    data_path = info_dict['data_path']
    get_latlon = False
    lowpass_threshold = 10

    for instance in CMIP6_models.instances:

        model_Name = instance.Name
        model_CaseList = instance.CaseList
        model_VarLab = instance.VarLab[0]

        for scenario in scenario_list: 

            if scenario in model_CaseList:

                tas_ij = np.zeros([250, 64, 128])
                roc_tas_ij = np.zeros([250-31, 64, 128])

                hist_name = f'/CMIP6_Regrid/tasCanESM5_{model_Name}_historical_{model_VarLab}.nc' 
                fopen_hist = cdms.open(data_path + hist_name)
                tas_hist = fopen_hist('tas')

                if get_latlon == False:
                    lat = np.array(tas_hist.getAxis(1)[:])
                    lon = np.array(tas_hist.getAxis(2)[:])
                    get_latlon = True 

                ssps_name = f'/CMIP6_Regrid/tasCanESM5_{model_Name}_{scenario}_{model_VarLab}.nc' 
                fopen_ssps = cdms.open(data_path + ssps_name)
                tas_ssps = fopen_ssps('tas')

                tas = np.array(np.r_[tas_hist, tas_ssps])
                if np.max(tas) > 200:
                    tas = tas - 273.15 

                for i in range(64):
                    for j in range(128):
                        tas_ij[:, i, j], roc_tas_ij[:, i, j] = separate_abs_roc(tas[:, i, j], lowpass_threshold)


                output_file_name = f'/CMIP6_spatial_results/{model_Name}_{scenario}.pickle'                
                with open(data_path + output_file_name, 'wb') as file:
                    pickle.dump([tas_ij, roc_tas_ij], file) 
                    



        # #### Plot here
        # def plotP(var, col):
        #     ax1 = plt.subplot(111, projection=ccrs.PlateCarree())
        #     ax1.add_feature(cfeature.COASTLINE)
        #     ax1.add_feature(cfeature.BORDERS)
        #     ax1.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
        #     # mp = ax1.pcolor(lon, lat, var, cmap=col, norm=colors.Normalize(vmin=-2, vmax=2), transform=ccrs.PlateCarree())
        #     mp = ax1.pcolor(lon, lat, var, cmap=col, transform=ccrs.PlateCarree())
        #     # ax1.contourf(lon, lat, mask_array_new, colors='none', hatches=['.'*5], transform=ccrs.PlateCarree())
        #     plt.colorbar(mp, ax=ax1, extend='both', shrink=0.5, orientation='vertical')
        #     plt.show()
        #     plt.clf()
        # max_roc = np.mean(tas_roc[:, 0], axis=0)
        # argmax_roc = np.mean(tas_roc[:, 1], axis=0)
        # plotP(max_roc, 'bwr')
        # plotP(argmax_roc, 'bwr')


if __name__ == '__main__':
    

    scenario_list = ['ssp126']
    analysis_spatial(scenario_list)