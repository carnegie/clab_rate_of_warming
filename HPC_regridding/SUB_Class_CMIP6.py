import os, numpy as np

class CMIP6_models:
    total_num = 0
    instances = []
    file_path = '/carnegie/nobackup/scratch/lduan/CMIP6/monthly/'
    def __init__(self, Name, Res, Grids, CaseList, VarLab):
        self.__class__.instances.append(self)
        self.Name = Name
        self.Res = Res
        self.Grids = Grids
        self.CaseList = CaseList
        self.VarLab = VarLab
        CMIP6_models.total_num +=1
    def get_nc_name(self, case_name, VarLab):
        self_nc_name = 'tp_' + self.Name + '_' + case_name + '_' + VarLab + '.nc'
        return self_nc_name
    def get_timestamp(self, case_name):
        if not (case_name in self.CaseList):
            print (self.Name, 'does not have', case_name)
            return []
        else:
            data_path = CMIP6_models.file_path + self.Name + '/' + case_name + '/'
            filelist  = os.listdir(data_path)
            timestamp = []
            for file in filelist:
                if file[:3] == 'tas':
                    timestamp.append(file[-16:])
            timestamp_unique = np.unique(timestamp)
            timestamp_unique.sort()
            return timestamp_unique
        
######################################################################################################
def set_class_instance():
    access_cm2      = CMIP6_models( 'ACCESS-CM2',      [144, 192], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    access_esm1_5   = CMIP6_models( 'ACCESS-ESM1-5',   [145, 192], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    awi_cm_1_1_mr   = CMIP6_models( 'AWI-CM-1-1-MR',   [192, 384], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    bcc_csm2_mr     = CMIP6_models( 'BCC-CSM2-MR',     [160, 320], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  )
    cams_csm1_0     = CMIP6_models( 'CAMS-CSM1-0',     [160, 320], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  )
    cesm2           = CMIP6_models( 'CESM2',           [192, 288], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  )
    cesm2_waccm     = CMIP6_models( 'CESM2-WACCM',     [192, 288], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  )
    ciesm           = CMIP6_models( 'CIESM',           [192, 288], 'gr',  ['historical', 'ssp126', 'ssp245',           'ssp585'],  ['r1i1p1f1']  ) # New
    cmcc_cm2_sr5    = CMIP6_models( 'CMCC-CM2-SR5',    [192, 288], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    cnrm_cm6_1      = CMIP6_models( 'CNRM-CM6-1',      [128, 256], 'gr',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f2']  )
    cnrm_esm2_1     = CMIP6_models( 'CNRM-ESM2-1',     [128, 256], 'gr',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f2']  )
    canesm5         = CMIP6_models( 'CanESM5',         [ 64, 128], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  )
    canesm5_canoe   = CMIP6_models( 'CanESM5-CanOE',   [ 64, 128], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p2f1']  ) # New
    ec_earth3       = CMIP6_models( 'EC-Earth3',       [256, 512], 'gr',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  )
    ec_earth3_veg   = CMIP6_models( 'EC-Earth3-Veg',   [256, 512], 'gr',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  )
    fgoals_f3_l     = CMIP6_models( 'FGOALS-f3-L',     [180, 288], 'gr',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    fgoals_g3       = CMIP6_models( 'FGOALS-g3',       [ 80, 180], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  )
    fio_esm_2_0     = CMIP6_models( 'FIO-ESM-2-0',     [192, 288], 'gn',  ['historical', 'ssp126', 'ssp245',           'ssp585'],  ['r1i1p1f1']  ) # New
    gfdl_esm4       = CMIP6_models( 'GFDL-ESM4',       [180, 288], 'gr1', ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  )
    giss_e2_1_g     = CMIP6_models( 'GISS-E2-1-G',     [ 90, 144], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f2']  ) # New
    inm_cm5_0       = CMIP6_models( 'INM-CM5-0',       [120, 180], 'gr1', ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    ipsl_cm6a_lr    = CMIP6_models( 'IPSL-CM6A-LR',    [143, 144], 'gr',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) 
    kace_1_0_g      = CMIP6_models( 'KACE-1-0-G',      [144, 192], 'gr',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    mcm_ua_1_0      = CMIP6_models( 'MCM-UA-1-0',      [80, 96],   'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f2']  ) # New
    miroc_es2l      = CMIP6_models( 'MIROC-ES2L',      [ 64, 128], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f2']  ) 
    miroc6          = CMIP6_models( 'MIROC6',          [128, 256], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) 
    mpi_esm1_2_hr   = CMIP6_models( 'MPI-ESM1-2-HR',   [192, 384], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    mpi_esm1_2_lr   = CMIP6_models( 'MPI-ESM1-2-LR',   [ 96, 192], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    mri_esm2_0      = CMIP6_models( 'MRI-ESM2-0',      [160, 320], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) 
    nesm3           = CMIP6_models( 'NESM3',           [ 96, 192], 'gn',  ['historical', 'ssp126', 'ssp245',           'ssp585'],  ['r1i1p1f1']  ) 
    noresm2_lm      = CMIP6_models( 'NorESM2-LM',      [ 96, 144], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    # noresm2_mm      = CMIP6_models( 'NorESM2-MM',      [ 96, 144], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f1']  ) # New
    ukesm1_0_ll     = CMIP6_models( 'UKESM1-0-LL',     [144, 192], 'gn',  ['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'],  ['r1i1p1f2']  )
    #print (CMIP6_models.total_num, 'CMIP6_models instances has been generated: ', 
    #       access_cm2.Name, access_esm1_5.Name, awi_cm_1_1_mr.Name, bcc_csm2_mr.Name, cams_csm1_0.Name, cesm2.Name, cesm2_waccm.Name,
    #       ciesm.Name, cmcc_cm2_sr5.Name, cnrm_cm6_1.Name, cnrm_esm2_1.Name, canesm5.Name, canesm5_canoe.Name, ec_earth3.Name, ec_earth3_veg.Name,
    #       fgoals_f3_l.Name, fgoals_g3.Name, fio_esm_2_0.Name, gfdl_esm4.Name, giss_e2_1_g.Name, inm_cm5_0.Name, ipsl_cm6a_lr.Name, kace_1_0_g.Name, 
    #       mcm_ua_1_0.Name, miroc_es2l.Name, miroc6.Name, mpi_esm1_2_hr.Name, mpi_esm1_2_lr.Name, mri_esm2_0.Name, nesm3.Name, noresm2_lm.Name, 
    #       noresm2_mm.Name, ukesm1_0_ll.Name)
