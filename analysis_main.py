



from analysis_global import analysis_global
from analysis_spatial_local import analysis_spatial_local

if __name__ == '__main__':

    ##################################
    #### Control area 
    ##################################
    
    scenario_list = ['ssp126', 'ssp245', 'ssp370', 'ssp585']
    analysis_global(scenario_list)
    stop 

    # scenario_list = ['ssp245']
    # # scenario_list = ['ssp585']
    # analysis_spatial_local(scenario_list)


