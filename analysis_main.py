from analysis_global import analysis_global
from analysis_spatial import analysis_spatial

if __name__ == '__main__':

    ##################################
    #### Control area 
    ##################################
    
    scenario_list = ['ssp126', 'ssp245', 'ssp370', 'ssp585']
    analysis_global(scenario_list)

    # scenario_list = ['ssp245']
    # analysis_spatial(scenario_list)
