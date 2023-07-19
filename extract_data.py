import xarray as xr
import numpy as np


def Rrs_data(file):
    fp = file
    data = xr.open_dataset(fp)
    wavebands = [400, 412, 443, 490, 510, 560, 620, 665, 674, 682, 709]
    
    Rrs = []
    
    for waveband in wavebands:
        rhos = data['rhos_' + str(waveband)].values
        Rrs.append(rhos)
    
    Rrs = np.array(Rrs)
    Rrst=np.transpose(Rrs)
    
    return Rrst
    
    
