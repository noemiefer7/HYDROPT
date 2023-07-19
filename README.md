# Remote sensing for Sentinel-3 datas using the HydroLight Optimization

Needed libraries : numpy, matplotlib, xarray, skimage, lmfit

These codes have been made to analyze the Sentinel-3 (L1 format) datas that you can obtain from the Copernicus open hub access. 
To do this analyze, the Acolite and HYDROPT open sources have been used.

First of all, you should run the code nammed 'launch_acolite.py' so as to do the atmospheric corrections on your image and also obtain the surface reflectance that would be in an NC file. The input folder would be the folder containing the sentinel-3 datas and the output one can be anything you want. I advice you to select a polygon from your image by using the latitute and the longitude : the images from sentinel-3 are huge so it would take a lot of time. 

Once you obtain the reflectance, you can run the 'main.py' programm after having enter the name (and the filepath if the file is not in the same folder) of the NC file in the fancy bracket in this line :
''' python '''
file='{}.nc'
''''''''''''''

Depending of the size of your data, the computing time can be long or not. 

The 'main.py' programm will return the concentration maps of the phytoplankton and the CDOM. 

