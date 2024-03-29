from SUB_Class_CMIP6 import CMIP6_models
from SUB_Class_CMIP6 import set_class_instance
from Info_func import info_func
from Info_func import lowpass_filter
from Info_func import separate_abs_roc

import cdms2 as cdms
import cdutil 
import numpy as np 
import statsmodels.api as sm
import pickle
import pandas as pd
import csv

import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as colors
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap





















def analysis_spatial(scenario_list):




    #### Models

    set_class_instance()
    
    info_dict = info_func()
    data_path = info_dict['data_path']

    get_latlon = False

    for scenario in scenario_list: 

        count = 0 
        if scenario in ['ssp126', 'ssp245', 'ssp585']:
            tas_abs = np.zeros([32, 2, 64, 128])
            tas_roc = np.zeros([32, 2, 64, 128])
        if scenario in ['ssp370']:
            tas_abs = np.zeros([29, 2, 64, 128])
            tas_roc = np.zeros([29, 2, 64, 128])

        for instance in CMIP6_models.instances:

            model_Name = instance.Name
            model_CaseList = instance.CaseList
            model_VarLab = instance.VarLab[0]

            # if model_Name in ["ACCESS-CM2"]:
            if scenario in model_CaseList:

                # ------------------------------------------------------------------------
                ########################
                #### Get data  
                ########################

                hist_name = f'/tasCanESM5_{model_Name}_historical_{model_VarLab}.nc' 
                fopen_hist = cdms.open(data_path + hist_name)
                tas_hist = fopen_hist('tas')

                if get_latlon == False:
                    lat = np.array(tas_hist.getAxis(1)[:])
                    lon = np.array(tas_hist.getAxis(2)[:])
                    get_latlon = True 

                ssps_name = f'/tasCanESM5_{model_Name}_{scenario}_{model_VarLab}.nc' 
                fopen_ssps = cdms.open(data_path + ssps_name)
                tas_ssps = fopen_ssps('tas')

                tas = np.array(np.r_[tas_hist, tas_ssps])
                if np.max(tas) > 200:
                    tas = tas - 273.15

                for i in range(64):
                    for j in range(128):
                        
                        tas_ij = lowpass_filter(tas[:, i, j], 'butter', 30)
                        tas_abs[count, 0, i, j] = np.max(tas_ij)
                        tas_abs[count, 1, i, j] = np.argmax(tas_ij) + 1850

                        total_length = len(tas_ij)
                        window_length = 31
                        roc_tas = np.zeros(total_length - window_length)
                        for k in range(total_length - window_length):
                            # Do linear regression 
                            x = np.arange(window_length)
                            x_const = sm.add_constant(x)
                            y = tas_ij[k:k+window_length]
                            model = sm.OLS(y, x_const).fit()
                            roc_tas[i] = model.params[1]
                        tas_roc[count, 0, i, j] = np.max(roc_tas) 
                        tas_roc[count, 1, i, j] = np.argmax(roc_tas) + 1850 + 16

                count += 1

        #### Save data to pickle 
        with open(scenario + '.pkl', 'wb') as f:
            pickle.dump([tas_abs, tas_roc], f)

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