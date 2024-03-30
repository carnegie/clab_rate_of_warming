


from SUB_Class_CMIP6 import CMIP6_models
from SUB_Class_CMIP6 import set_class_instance
from Info_func import info_func

import pickle 
import numpy as np 




def analysis_spatial_local(scenario_list):

    info_dict = info_func()
    data_path = info_dict['data_path']
    lowpass_threshold = 10

    set_class_instance()

    for scenario in scenario_list: 

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




                print ()
                print ()
                print (pickle_file_name)
                print (tas_ij.shape)
                print (roc_tas_ij.shape) 
                print () 

                stop 


