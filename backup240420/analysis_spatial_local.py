


from SUB_Class_CMIP6 import CMIP6_models
from SUB_Class_CMIP6 import set_class_instance
from Info_func import info_func

import cdms2 as cdms 
import pickle 
import numpy as np 
import cdutil
import genutil

import matplotlib
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as colors
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap


def analysis_spatial_local(scenario_list):

    info_dict = info_func()
    data_path = info_dict['data_path']
    lowpass_threshold = 10

    set_class_instance()

    for scenario in scenario_list: 

        if scenario in ['ssp126', 'ssp245', 'ssp585']:
            tas_abs = np.zeros([32, 250, 64, 128])
            tas_roc = np.zeros([32, 250-31, 64, 128])
        if scenario in ['ssp370']:
            tas_abs = np.zeros([29, 250, 64, 128])
            tas_roc = np.zeros([29, 250-31, 64, 128])

        count = 0

        for instance in CMIP6_models.instances:

            model_Name = instance.Name
            model_CaseList = instance.CaseList
            model_VarLab = instance.VarLab[0]

            if scenario in model_CaseList:

                pickle_file_name = data_path + '/CMIP6_spatial_results/' + model_Name + '_' + scenario + '.pickle' 
                with open(pickle_file_name, 'rb') as f:
                    tas_ij, roc_tas_ij = pickle.load(f)


                """
                There are two ways to calculate the ensemble mean metric:
                    1. First calculate each model and then average the results
                    2. First average the data from each model and then calculate the metric
                
                For the maximum rate of change and timing, the second approach might be better?
                """
                tas_abs[count] = tas_ij
                tas_roc[count] = roc_tas_ij
                count += 1

        #### Now do ensemble mean
        tas_abs_mean = np.mean(tas_abs, axis=0)
        max_tas_abs = np.max(tas_abs_mean, axis=0)
        argmax_tas_abs = np.argmax(tas_abs_mean, axis=0)

        tas_roc_mean = np.mean(tas_roc, axis=0)
        #### Now do a X year moving average
        for i in range(15, 250-31):
            tas_roc_mean[i] = np.mean(tas_roc_mean[i-15:i+15], axis=0)

        max_tas_roc = np.max(tas_roc_mean[15:-15], axis=0)
        argmax_tas_roc = np.argmax(tas_roc_mean[15:-15], axis=0) + 1850 + 16 + 15

        map_max_global_h = tas_roc_mean[107]
        map_max_global_c = tas_roc_mean[157]
        map_max_global_f = tas_roc_mean[217]


        # #### Calculate spatial standard deviation 
        # # std_h = genutil.statistics.std(tas_roc_mean[107])
        # # std_c = genutil.statistics.std(tas_roc_mean[157])
        # # std_f = genutil.statistics.std(tas_roc_mean[217])
        # std_h = np.std(map_max_global_h)
        # std_c = np.std(map_max_global_c)
        # std_f = np.std(map_max_global_f)
        # print ()
        # print (std_h) 
        # print (std_c)
        # print (std_f)
        # print () 
        # stop 

        


        canesm5_open = cdms.open('./HPC_regridding/tas_Amon_CanESM5_historical_r1i1p1f1_gn_185001-201412.nc')
        tas_canesm5 = canesm5_open('tas', squeeze=1)[0]
        canesm5_open.close()
        lat = np.array(tas_canesm5.getAxis(0)[:])
        lon = np.array(tas_canesm5.getAxis(1)[:])

        #### Plot results 
        def plotP(var, col, name):

            #### Normalize 
            # var = var / np.mean(var)

            ax1 = plt.subplot(111, projection=ccrs.PlateCarree())
            ax1.add_feature(cfeature.COASTLINE)
            ax1.add_feature(cfeature.BORDERS)
            ax1.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
            # mp = ax1.pcolor(lon, lat, var, cmap=col, norm=colors.Normalize(vmin=0, vmax=2), transform=ccrs.PlateCarree())
            mp = ax1.pcolor(lon, lat, var, cmap=col, transform=ccrs.PlateCarree())
            # ax1.contourf(lon, lat, mask_array_new, colors='none', hatches=['.'*5], transform=ccrs.PlateCarree())
            #### Plot contour of 1 
            ax1.contour(lon, lat, var, levels=[1], colors='purple', transform=ccrs.PlateCarree())
            plt.colorbar(mp, ax=ax1, extend='both', shrink=0.5, orientation='vertical')
            plt.show()
            # plt.savefig(name + '.ps', bbox_inches='tight') 
            plt.clf()

        plotP(max_tas_roc, 'Reds', 'max_roc')
        plotP(argmax_tas_roc, 'Reds', 'year_max_roc')

        # plotP(map_max_global_h, 'Reds', 'map_h')
        # plotP(map_max_global_c, 'Reds', 'map_c')
        # plotP(map_max_global_f, 'Reds', 'map_f')

