
import os
import pandas as pd
import numpy as np 
import pickle 
import matplotlib.pyplot as plt 


def get_data(obs_data_path):

    #### Let's adjust them so all start from 1980 to 2023 and refer to 1980-2010 as reference

    '''
    Berkely Earth data: 1850 to 2023, 1951-1980 as reference 
    '''
    BE = pd.read_csv(obs_data_path + 'Berkeley_Eartch.csv')
    BE = BE.iloc[1:,:]
    BE_sat = []
    for i in range(BE.shape[0]):
        BE_sat.append(BE.iloc[i,0].split()[1])
    BE_sat = np.array(BE_sat).astype('float')
    ref_1951_1980 = 14.101
    BE_sat_abs = BE_sat + ref_1951_1980
    ref_1981_2010 = np.mean(BE_sat_abs[1981-1850:2011-1850])
    BE_sat_adj = (BE_sat_abs - ref_1981_2010)[1980-1850:]


    '''
    GISS data: 1880 to 2023, 1951-1980 as reference 
    '''
    GISS = pd.read_csv(obs_data_path + 'GISS_surface_temperature_analysis_version_4.csv')
    
    #### GEt each line, and then calculate the average of the first 12 column
    GISS_sat = []
    for i in range(GISS.shape[0]-1):
        tmp = np.mean(np.array(GISS.iloc[i,1:13].values).astype('float'))
        GISS_sat.append(tmp)
    GISS_sat = np.array(GISS_sat).astype('float')
    ref_1951_1980 = np.mean(GISS_sat[1951-1880:1981-1880])
    ref_1981_2010 = np.mean(GISS_sat[1981-1880:2011-1880])
    GISS_sat_adj = (GISS_sat - (ref_1981_2010-ref_1951_1980))[1980-1880:]


    '''
    HadCRUT5 data: 1850 to 2023, 1961-1990 as reference 
    '''   
    HadCRUT5 = pd.read_csv(obs_data_path + 'HadCRUT.5.0.2.0.analysis.summary_series.global.annual.csv')
    HadCRUT5_sat = np.array(HadCRUT5.iloc[:,1].values.astype('float'))
    ref_1961_1990 = np.mean(HadCRUT5_sat[1961-1850:1991-1850])
    ref_1981_2010 = np.mean(HadCRUT5_sat[1981-1850:2011-1850])
    HadCRUT5_sat_adj = (HadCRUT5_sat - (ref_1981_2010-ref_1961_1990))[1980-1850:]


    '''
    NOAA data: 1850 to 2023, 1901-2000 as reference 
    '''   
    NOAA = pd.read_csv(obs_data_path + 'NOAA_GlobalTemp.csv')
    NOAA_sat = np.array(NOAA.iloc[:,1].values.astype('float'))
    ref_1901_2000 = np.mean(NOAA_sat[1901-1850:2001-1850])
    ref_1981_2010 = np.mean(NOAA_sat[1981-1850:2011-1850])
    NOAA_sat_adj = (NOAA_sat - (ref_1981_2010-ref_1901_2000))[1980-1850:]


    '''
    ERA5, 1979 to 2023
    '''
    with open(obs_data_path + 'ERA5_global_avg.pickle', 'rb') as f:
        ERA5 = pickle.load(f)
    ERA5_sat = np.mean(np.array(ERA5['gm']).reshape(-1, 12), axis=1)
    ref_1981_2010 = np.mean(ERA5_sat[1981-1979:2011-1979])
    ERA5_sat_adj = (ERA5_sat - ref_1981_2010)[1980-1979:]


    return BE_sat_adj, GISS_sat_adj, HadCRUT5_sat_adj, NOAA_sat_adj, ERA5_sat_adj



def check_obs_data(obs_data_path):

    BE, GISS, HadCRUT5, NOAA, ERA5 = get_data(obs_data_path)

    year = np.arange(1980, 2024)
    color_list = ['red', 'green', 'blue', 'orange', 'purple']

    for data_i in [BE, GISS, HadCRUT5, NOAA, ERA5]:
        plt.plot(year, data_i, color=color_list.pop(0))
    plt.show() 