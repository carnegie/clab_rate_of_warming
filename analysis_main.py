


# from analysis_global import analysis_global
# from analysis_global_reframing import analysis_global
from analysis_global_EG import analysis_global_EG
from backup240420.analysis_spatial_local import analysis_spatial_local

if __name__ == '__main__':

    ##################################
    #### Control area 
    ##################################

    
    analysis_global_EG() 

    # source_list = ['AR6']
    # source_list = ['CMIP6']
    # source_list = ['NDCs']
    # analysis_global(source_list)
    # stop 

    # scenario_list = ['ssp126', 'ssp245', 'ssp370', 'ssp585']
    # analysis_global(scenario_list)

    # scenario_list = ['ssp245']
    # # scenario_list = ['ssp585']
    # analysis_spatial_local(scenario_list)


