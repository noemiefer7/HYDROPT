# Before to use this code, you should run the code launch_acolite with
# your Sentinel-3 folder. 
# You will then obtain an nc file that you will use with the 
# Rrs_data() function to extract the Rrs values



import hydropt.hydropt as hd
import numpy as np
import lmfit
from math import ceil
from hydropt.bio_optics import H2O_IOP_DEFAULT, a_phyto_base_HSI
from extract_data import Rrs_data
from mask import mask_creation
from map_plotting import plot_map


waveband = np.arange(400, 711, 5)


######## IOP of the water ##########

#Importation of the inherent optical properties (IOP) of water from the
# ```bio_optics``` module and creation an optical model for this component"
# as follows:
def clear_nat_water(*args):
    return H2O_IOP_DEFAULT.T.values

def phytoplankton(*args):
    chl = args[0]
    a = a_phyto_base_HSI.absorption.values
    bb = np.repeat(.014 * 0.18, len(a))
    return chl * np.array([a, bb])

def cdom(*args):
    a_440 = args[0]
    a = np.array(np.exp(-0.017 * (waveband - 440)))
    bb = np.zeros(len(a))
    return a_440 * np.array([a, bb])

   
#Creation of the bio optical model 
bio_opt = hd.BioOpticalModel()
bio_opt.set_iop(
    wavebands = waveband,
    water = clear_nat_water,
    phyto = phytoplankton,
    cdom = cdom)



############ Reflectance values ############

# NC file obtained with launch_acolite()
file='{}.nc'

# Reflectance values from the nc file
rho_s = Rrs_data(file)

# Numbers of rows, columns and bands (=11) of the reflectance array
[R,C,B] = rho_s.shape

# Number of bands contained in the waveband array
num_bands = len(waveband)

# Interpolation of the reflectance so as to have a third dimension egal to 63
rho_s_extend = np.empty(( R, C, num_bands ))
c = 0
for i in range (B):
    for j in range (int(ceil(num_bands)/B) + 1):
        if c+j==63:
            break
        rho_s_extend[:,:,c+j] = rho_s[:,:,i]
    c+= 6



############ Inversion of the model #################

# Creation of the foward model from the bio optical model
fwd_model = hd.PolynomialForward(bio_opt)

# Initiate an inversion model
inv_model = hd.InversionModel(
        fwd_model = fwd_model,
        minimizer = lmfit.minimize)  

# Initiate the paramaters
x0 = lmfit.Parameters()
x0.add('phyto',value = .5,min = 1E-9)
x0.add('cdom',value = .01,min = 1E-9)

# Arrays that will contained the phyto and cdom value of each pixel
phyto = np.empty((R, C))
cdom = np.empty((R, C))

# Model inversion
for i in range(R):
    print(i)
    for j in range(C):
        # Squeeze the reflectance into an array of two dimensions
        Rrs_mesure = rho_s_extend[i, j, :]
        # Inversion/fitting model
        xhat = inv_model.invert(y=Rrs_mesure, x=x0)
        #Extraction of the phyto values
        phyto[i, j] = xhat.last_internal_values[0]
        #Extraction of the cdom values
        cdom[i, j] = xhat.last_internal_values[1]


# Transposition of the arrays
phyto_transpose=np.transpose(phyto)
cdom_transpose=np.transpose(cdom)

mask = mask_creation(file)
plot_map(phyto_transpose,cdom_transpose,mask)