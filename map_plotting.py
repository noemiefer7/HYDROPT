import matplotlib.pyplot as plt

def plot_map(phyto, cdom, mask):

    carte_phyto = phyto*mask
    carte_cdom = cdom*mask
    
    fig,axs=plt.subplots(1,2,figsize=(10,10))
    
    im0=axs[0].imshow(carte_phyto, cmap='jet', vmin=0, vmax=10**(-8))
    axs[0].set_title('Phytoplankton map')
    fig.colorbar(im0, ax=axs[0],fraction=0.046, pad=0.04)
    
    im1=axs[1].imshow(carte_cdom, cmap='jet', vmin=0, vmax=1)
    axs[1].set_title('CDOM map')
    fig.colorbar(im1, ax=axs[1],fraction=0.046, pad=0.04)


