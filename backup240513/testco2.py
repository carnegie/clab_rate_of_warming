import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from Info_func import separate_abs_roc_yty


fname = '/Users/duanlei/Desktop/File/Research/Carnegie_projects/Collabs/Steve_shift_climate/rate_of_change/Data/Keeling_curve/monthly_in_situ_co2_mlo.csv'
data = pd.read_csv(fname)

#### 1958 to 2024
year = np.arange(1958, 2024)
data = np.mean(np.array(data.iloc[:,8]).astype('float').reshape(-1, 12), axis=1)[:-1]
# data_inc = data[1:] - data[:-1]
year, data_inc = separate_abs_roc_yty(data, year, 17)
# plt.plot(year, data)
plt.plot(year, data_inc)
plt.xlim(1980, 2024)
plt.show()


# from Info_func import separate_abs_roc_regression
# from Info_func import separate_abs_roc_fit
# from Info_func import separate_abs_roc_sparse
# year = np.arange(data.shape[0])+1958
# for i in range(3):
#     roc = separate_abs_roc_fit(data[5:, i], 0, '', False) 
#     plt.plot(year[5:], roc)

# plt.show() 