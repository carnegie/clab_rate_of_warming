import cdms2 as cdms
from SUB_Class_CMIP6 import CMIP6_models
from SUB_Class_CMIP6 import set_class_instance
from SUB_GetNcData   import get_nc_data

if __name__ == '__main__':
    set_class_instance()
    get_case_name = 'ssp585'
    for instance in CMIP6_models.instances:
        if get_case_name in instance.CaseList:
            print ('----------', instance.Name, '----------')
            
            varlab_used = instance.VarLab[0]
            get_nc_data(instance, get_case_name, 'tas', varlab_used)
