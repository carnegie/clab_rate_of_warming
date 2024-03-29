import numpy as np, cdms2 as cdms, MV2 as MV, cdutil

def create_EAG(num_lat):
    lat    = cdms.createEqualAreaAxis(num_lat)
    Gau    = cdms.createGaussianGrid(num_lat)
    lon    = Gau.getAxis(1)
    gEq    = cdms.createRectGrid(lat, lon)
    return gEq, Gau

def get_nc_data(instance, case_name, var, VarLab, regrid=1):

    file_path = '/carnegie/nobackup/scratch/lduan/CMIP6/monthly/'
    DaysInMonths = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    
    try:
        timestamp     = instance.get_timestamp(case_name)
        num_of_files  = len(timestamp)
        data_path     = file_path + instance.Name + '/' + case_name + '/'
        # Step 1, get all data, return VarGet
        if num_of_files == 1:
            postfix = instance.Name + '_' + str(case_name) + '_' + str(VarLab) + '_' + str(instance.Grids) + '_' + str(timestamp[0])
            if var == 'net':
                fopen1 = cdms.open(data_path + str('rsdt') + '_Amon_' + postfix)
                fopen2 = cdms.open(data_path + str('rsut') + '_Amon_' + postfix)
                fopen3 = cdms.open(data_path + str('rlut') + '_Amon_' + postfix)
                VarGet = fopen1('rsdt', squeeze=1) - fopen2('rsut', squeeze=1) - fopen3('rlut', squeeze=1)
                fopen1.close(); fopen2.close(); fopen3.close()
            else:
                fopen  = cdms.open(data_path + str(var) + '_Amon_' + postfix)
                VarGet = fopen(var, squeeze=1)
                fopen.close()
        else:
            for files_idx in range(num_of_files):
                postfix = instance.Name + '_' + str(case_name) + '_' + str(VarLab) + '_' + str(instance.Grids) + '_' + str(timestamp[files_idx])
                if var == 'net':
                    fname1 = data_path + str('rsdt') + '_Amon_' + postfix;    fopen1 = cdms.open(fname1)
                    fname2 = data_path + str('rsut') + '_Amon_' + postfix;    fopen2 = cdms.open(fname2)
                    fname3 = data_path + str('rlut') + '_Amon_' + postfix;    fopen3 = cdms.open(fname3)
                    VarGet_tmp = fopen1('rsdt', squeeze=1) - fopen2('rsut', squeeze=1) - fopen3('rlut', squeeze=1)
                    fopen1.close(); fopen2.close(); fopen3.close()
                else:
                    fopen      = cdms.open(data_path + str(var) + '_Amon_' + postfix)
                    VarGet_tmp = fopen(var, squeeze=1)
                    fopen.close()
                if files_idx == 0:
                    VarGet, lat_tmp, lon_tmp = VarGet_tmp, VarGet_tmp.getAxis(1), VarGet_tmp.getAxis(2)
                else:
                    VarGet                   = np.r_[VarGet, VarGet_tmp]
            VarGet = MV.array(VarGet)
            VarGet.setAxis(1, lat_tmp)
            VarGet.setAxis(2, lon_tmp)

        # Step 2, Selecte time periods, return VarReshape
        if case_name == 'historical':    length = int(2014-1850+1)
        if case_name == 'ssp126':        length = int(2099-2015+1)
        if case_name == 'ssp245':        length = int(2099-2015+1)
        if case_name == 'ssp370':        length = int(2099-2015+1)
        if case_name == 'ssp585':        length = int(2099-2015+1)
        if case_name == 'piControl':     length = int(VarGet.shape[0]/12)
        if case_name == 'abrupt-4xCO2':  length = int(VarGet.shape[0]/12)
        VarReshape = MV.zeros([length,instance.Res[0],instance.Res[1]])
        VarReshape.setAxis(1, VarGet.getAxis(1))
        VarReshape.setAxis(2, VarGet.getAxis(2))
        for lat_idx in range(instance.Res[0]):
            for lon_idx in range(instance.Res[1]):
                reshape_array = VarGet[:,lat_idx,lon_idx].reshape(-1,12)
                average_array = (cdutil.averager(reshape_array, axis=1, weights=DaysInMonths))[:length]
                VarReshape[:, lat_idx, lon_idx] = average_array
        # Step 3, Regrid
        if regrid == 1:
            g = cdms.open('./Regrid/tas_' + instance.Name + '_' + str(case_name) + '_' + str(VarLab) + '.nc', 'w')
            # Main text grid
            axis1    = cdms.createEqualAreaAxis(64)
            Gaussian = cdms.createGaussianGrid(64)
            axis2    = Gaussian.getAxis(1)
            gEquArea = cdms.createRectGrid(axis1, axis2)
            VarRegrid_main = VarReshape.regrid(gEquArea,regridTool="esmf",regridMethod="conservative")
            VarRegrid_main.id = 'tEquArea'
            g.write(VarRegrid_main)
            # Regrid to CanESM5 
            canesm5_open = cdms.open('./tas_Amon_CanESM5_historical_r1i1p1f1_gn_185001-201412.nc')
            tas_canesm5 = canesm5_open('tas', squeeze=1)[0]
            canesm5_open.close()
            gCanESM5 = tas_canesm5.getGrid()
            VarCanESM5 = VarReshape.regrid(gCanESM5,regridTool="esmf",regridMethod="conservative")
            VarCanESM5.id = 'tCanESM5'
            g.write(VarCanESM5)
        else:
            print ('regrid model grids')

    except Exception as e:
        print ('error met, return 0')
        print (e)
        return 0, 0, 0
    