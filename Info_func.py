
import scipy.signal as signal
import numpy as np 
import statsmodels.api as sm
import platform

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



def separate_abs_roc(var, threshold, window_length):

    #### Let's do some lowpass filtering first 
    if threshold > 0: var = lowpass_filter(var, 'butter', threshold)

    #### Now calculate the rate of change using a linear regression approach
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

    return var, roc_var