

import pickle, platform, numpy as np, pandas as pd
import statsmodels.api as sm
import scipy.signal as signal
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit


def info_func():
    info_dict = {}
    # If on linux system:
    if platform.system() == 'Linux':
        info_dict['data_path'] = '/carnegie/nobackup/scratch/lduan/project_data_store/clab_rate_of_warming'
    # If on macOS:
    if platform.system() == 'Darwin':
        info_dict['data_path'] = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data'
    return info_dict


def highpass_filter(var, approach, highpass):
    fs = 1
    if approach == 'butter':
        npt = 10
        cutoff_period = highpass
        cutoff_freque = (1/cutoff_period) / (fs/2)
        z, p, k = signal.butter(npt, cutoff_freque, 'highpass', output="zpk")
        smoothed0 = signal.zpk2sos(z, p, k)
        output_highpass = signal.sosfiltfilt(smoothed0, var)
    if approach == 'fft':
        length = len(var)
        cutoff_period = highpass
        cutoff_freque = (1/cutoff_period)
        input_fft = np.fft.fft(var)
        input_fre = np.fft.fftfreq(length)
        input_fft[np.abs(input_fre)<=cutoff_freque] = 0.
        output_highpass = np.fft.ifft(input_fft).real      
    return output_highpass


def lowpass_filter(var, approach, lowpass):
    fs = 1
    if approach == 'hann':
        window = signal.windows.hann(lowpass)
        output_lowpass = signal.convolve(var, window/window.sum(), mode='same')
    if approach == 'butter':
        npt = 10
        cutoff_period = lowpass
        cutoff_freque = (1/cutoff_period) / (fs/2)
        z, p, k = signal.butter(npt, cutoff_freque, 'lowpass', output="zpk")
        smoothed0 = signal.zpk2sos(z, p, k)
        output_lowpass = signal.sosfiltfilt(smoothed0, var)
    if approach == 'fft':
        length = len(var)
        cutoff_period = lowpass
        cutoff_freque = (1/cutoff_period)
        input_fft = np.fft.fft(var)
        input_fre = np.fft.fftfreq(length)
        input_fft[np.abs(input_fre)>=cutoff_freque] = 0.
        output_lowpass = np.fft.ifft(input_fft).real      
    if approach == 'convolve':
        n = 10
        b = np.ones(n)/n
        output_lowpass = np.convolve(var, b, mode='same')
    return output_lowpass


def hann_window_new(x_list, y_list, t_width):
    x = np.array(x_list)
    y = np.array(y_list) 
    half_width = t_width / 2.0
    weighted_mean_list = [] 
    for t0 in x:        
        indices = np.where((x >= t0 - half_width) & (x <= t0 + half_width))[0]
        x_window = x[indices]
        y_window = y[indices]
        relative_positions = (x_window - (t0 - half_width)) / t_width
        hann_weights = 0.5 * (1 - np.cos(2 * np.pi * relative_positions))
        weighted_mean = np.sum(hann_weights * y_window) / np.sum(hann_weights)
        weighted_mean_list.append(weighted_mean)
    return weighted_mean_list



def separate_abs_roc_regression(var, year, window_length):
    total_length = len(var)
    num_of_intervals = total_length - window_length + 1
    roc_var = np.zeros(num_of_intervals)
    for i in range(num_of_intervals):
        x = np.arange(window_length)
        x_const = sm.add_constant(x)
        y = var[i:i+window_length]
        model = sm.OLS(y, x_const).fit() 
        roc_var[i] = model.params[1] 
    whereisnan1 = np.isnan(var) 
    var = np.ma.masked_where(whereisnan1, var) 
    whereisnan2 = np.isnan(roc_var) 
    roc_var = np.ma.masked_where(whereisnan2, roc_var) 
    hafwidth = int((window_length-1)/2)
    return year[hafwidth:-hafwidth], roc_var 

def separate_abs_roc_wls(var, year, window_length):
    total_length = len(var)
    window = signal.windows.hann(window_length)
    num_of_intervals = total_length - window_length + 1
    roc_var = np.zeros(num_of_intervals)
    for i in range(num_of_intervals):
        x = np.arange(window_length)
        x_const = sm.add_constant(x)
        y = var[i:i+window_length]
        # model = sm.OLS(y, x_const).fit() 
        model = sm.WLS(y, x_const, weights=window).fit() 
        roc_var[i] = model.params[1] 
    whereisnan1 = np.isnan(var) 
    var = np.ma.masked_where(whereisnan1, var) 
    whereisnan2 = np.isnan(roc_var) 
    roc_var = np.ma.masked_where(whereisnan2, roc_var) 
    hafwidth = int((window_length-1)/2)
    return year[hafwidth:-hafwidth], roc_var 


def separate_abs_roc_spline(var, year, window_length):
    def parabolic_fit(x, a, b, c):
        return a * x**2 + b * x + c
    cubic_spline = CubicSpline(year, var)
    spline_derivatives = cubic_spline.derivative()
    roc_var = spline_derivatives(year)    
    if window_length == 0: 
        return year, roc_var
    else:
        start = (window_length-1)/2
        end = -int(start)
        mid_values = []
        total_seg = len(roc_var) - window_length + 1 
        for i in range(total_seg):
            x = year[i:i+window_length]
            y = roc_var[i:i+window_length]
            popt, pcov = curve_fit(lambda x, a, b, c: a*x**2 + b*x + c, x, y)       
            mid_values.append(parabolic_fit(x[int(window_length/2)], *popt))                                                                                                                                       
        return year[int(start):int(end)], mid_values 
    

def separate_abs_roc_yty_detrend(var, year, threshold):
    roc = (var[1:] - var[:-1]) / (year[1:] - year[:-1])
    if threshold > 0: 
        # roc_detrended = lowpass_filter(roc, 'hann', threshold) 
        roc_detrended = hann_window_new(year[1:], roc, threshold)
        halfWidth = int((threshold - 1) / 2)
    else:
        roc_detrended = roc
        halfWidth = 0
    return year[halfWidth+1:-halfWidth], roc_detrended[halfWidth:-halfWidth]





def separate_abs_roc_sparse(var):
    year = np.array([2010,2015,2020,2030,2040,2045,2050,2053,2060,2070,2080,2090,2100])
    cubic_spline = CubicSpline(year, var)
    spline_derivatives = cubic_spline.derivative()
    roc_var = spline_derivatives(year)     
    return roc_var
    

def interpolate_emissions(var):
    year_info = np.array([2010,2015,2020,2030,2040,2045,2050,2053,2060,2070,2080,2090,2100])
    cs = CubicSpline(year_info, var) 
    x_fine = np.arange(2010, 2051, 1)
    y_fine = cs(x_fine)
    return x_fine, y_fine






def get_rw_data(obs_data_path):

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