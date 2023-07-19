import xarray as xr
import numpy as np
import skimage.color
import skimage.filters


def mask_creation(nc_file):
    # Opening of the NC file
    nc = xr.open_dataset(nc_file)
    
    # Extract RGB datas 
    blue_band = np.array(nc['rhos_412'])
    green_band = np.array(nc['rhos_560'])
    red_band = np.array(nc['rhos_665'])
    
    # RGB image creation
    rgb_image = np.dstack((red_band ,green_band ,blue_band)) 

    # Conversion into gray image
    gray_image=skimage.color.rgb2gray(rgb_image)
    
    # Application of a gaussian filter
    blurred_image = skimage.filters.gaussian(gray_image, sigma=1.0)
    
    # Automatic finding of the image threshold
    t = skimage.filters.threshold_otsu(blurred_image)
    
    # Mask creation
    mask=blurred_image<t
    
    # Conversion of the mask into uint8 
    mask=mask.astype('uint8')
    
    return mask





