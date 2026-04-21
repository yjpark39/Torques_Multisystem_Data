import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import splev, splrep, griddata 

params = {
            'font.family' : 'Times'
        }
matplotlib.rcParams.update(params)


datadir  = '/Users/yjpark/YJ/Projects/Multisystem/Figures/fig1/sources/'
datadir1 = '/Users/yjpark/YJ/Projects/Multisystem/Figures/fig1/sources/data_energymap/'
datadir2 = '/Users/yjpark/YJ/Projects/Multisystem/Figures/fig1/sources/data_energycurve/'


eref = -6.7150814  # BNBNBN (1.08, 1.08)


# ----- Figure Generation -----
fig_width   = 6.9 # inches
golden_mean = (np.sqrt(5)-1.0)/2.0    # Aesthetic ratio
fig_height = fig_width*golden_mean*1.3 # height in inches

fig = plt.figure(figsize=(fig_width, fig_height))
msize, fsize = 3, 8

gs0 = gridspec.GridSpec(3, 2, figure=fig)
gs0.update(wspace=0.3, hspace=0.5) # set the spacing between axes.

# ----- Panel (a) : ENERGY MAP -----
ax1s = [fig.add_subplot(gs00)  for gs00 in gs0[0, 0].subgridspec(1, 3)]
ax2s = [fig.add_subplot(gs00)  for gs00 in gs0[1, 0].subgridspec(1, 3)]
ax3s = [fig.add_subplot(gs00)  for gs00 in gs0[2, 0].subgridspec(1, 3)]

for stype, axs in zip(['BNBNBN', 'NBBNBN', 'BNNBBN'],
                       [ax1s, ax2s, ax3s]):
    for th12_deg, natom, ax in zip([1.084549, 1.538500, 2.004628],
                                 [16746, 8322, 4902],
                            axs):
        val = np.genfromtxt(f"{datadir1}energymap_{stype}_{th12_deg:.2f}.dat")#, skip_header=1)
        
        XX, YY, data0 = val[:,0], val[:,1]*np.sqrt(3), (val[:,-1]/natom-eref)*1000
        vvmin, vvmax  = np.min(data0), np.max(data0) 
        print(stype, f"{th12_deg:.6f}", f"{vvmin:.2f}", f"{vvmax:.2f}")
        # ax.scatter(XX,YY, s=msize, c=data0, vmin=vvmin, vmax=vvmax, cmap='jet')

        num       = 1601
        margin    = 0.1
        L         = np.sqrt(3)
        x         = np.linspace(0, 1         ,num, endpoint=True)
        y         = np.linspace(0, np.sqrt(3),num, endpoint=True)

        val_sp    = griddata((XX, YY),data0,
                                (x[None,:], y[:,None]), method='linear') 

        im = ax.imshow(val_sp, vmin=vvmin, vmax = vvmax,  
                        extent=[0, 1,0, np.sqrt(3)],origin="lower",cmap='jet')

        ax.set_xlim(0,1)
        ax.set_ylim(0, np.sqrt(3))
        ax.set_xticks([0, 1])
        ax.set_yticks(np.linspace(0, np.sqrt(3), 4, endpoint=True))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        if stype=='BNBNBN': ax.set_title("$\\theta_{12}="+f"{th12_deg:.2f}"+"^{\\circ}$", fontsize=fsize, fontname='times')


# ----- Panel (b) : ENERGY CURVE -----
axRs = [fig.add_subplot(gs0[i, 1]) for i in range(3)] 

inds_BNBNBN   = [[0,1,2,3,-2,-1], # 1.08
                 [0,1,2,3,-2,-1], # 1.54
                 [0,1,2,-2,-1]]   # 2.00
inds_NBBNBN   = [[0,1,-3,-2,-1],  # 1.08
                 [0,1,2,-2,-1],   # 1.54
                 [0,1,-3,-1]]     # 2.00
inds_BNNBBN   = [[0,1,3,-3,-1],   # 1.08
                 [0,1,2,3,4,-3,-2,-1], # 1.54
                 [0,1,2,-2,-1]]   # 2.00

for stype, ax, mtype, stack_name, spl_inds in zip(['BNBNBN', 'NBBNBN', 'BNNBBN'],
                            axRs, 
                            ['o','^','s'],
                            ["$\\overline{\\rm AAA}$", "$\\overline{\\rm AAC^\\prime}$", "$\\overline{\\rm AA^\\prime A}$"],
                            [inds_BNBNBN, inds_NBBNBN, inds_BNNBBN]):
    for th12_deg, mcolor, spl_ind in zip([1.084549, 1.538500, 2.004628],
                                ['C0', 'C1', 'C2'],
                                spl_inds):
        val = np.genfromtxt(f"{datadir2}energycurve_{stype}_{th12_deg:.2f}.dat", skip_header=1)
        ang32_degs, etots = val[:,1], val[:,2]
        ax.plot(ang32_degs, (etots-eref)*1000,'-', ms= msize, marker=mtype, color=mcolor, lw=0.5, label="$\\theta_{12} = "+f"{th12_deg:.2f}"+"^{\\circ}$ - "+f"{stack_name}")

        ind   = list(ang32_degs).index(th12_deg)

        # Fitting curves
        spl    = splrep(val[spl_ind,1],val[spl_ind,2])
        theta  = np.linspace(np.min(val[:,1]),np.max(val[:,1]))
        fitted = splev(theta,spl)
        
        ax.plot(theta,(fitted-eref)*1000,"--",color=mcolor,linewidth=0.9)
        ax.fill_between(ang32_degs, (etots-eref)*1000, (splev(ang32_degs,spl)-eref)*1000 , color=mcolor, alpha=0.3)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)


        print(f"{stype}_{th12_deg:.2f}")
        ind=list(ang32_degs).index(th12_deg)
        ang = ang32_degs
        val = (etots-eref)*1000
        slope_L = (val[ind]-val[ind-1])/np.deg2rad(ang[ind]-ang[ind-1])
        slope_R = (val[ind+1]-val[ind])/np.deg2rad(ang[ind+1]-ang[ind])
        print(f"Slope: {ang[ind-1]},{ang[ind]},{ang[ind+1]}: {slope_L:.2f}, {slope_R:.2f}")

        ind  = np.where(ang32_degs == th12_deg)[0][0]
        val1 = (splev(np.array([th12_deg]),spl)-eref)*1000
        print(f"Binding E:  {ang[ind]:.6f}, {val[ind]:.3f}, {val1[0]:.3f}, {val1[0]-val[ind]:.3f} \n")

        ax.set_ylabel("$E^{tot}$ (meV/atom)", fontsize=fsize, fontname='times')
        if stype=='BNNBBN': ax.set_xlabel("$\\theta_{32}$", fontsize=fsize, fontname='times')

        ax.set_xlim(0,3.1)
        ax.set_xticks(np.linspace(0, 3, 7, endpoint=True))

        if stype=='BNBNBN': 
            ax.set_ylim(-1,2)
            ax.set_yticks(np.linspace(-1, 2, 7, endpoint=True))
        else:
            ax.set_ylim(-0.5,2.5)
            ax.set_yticks(np.linspace(-0.5, 2.5, 7, endpoint=True))
             
        ax.set_xticklabels([f"{i:.1f}"+"$^{\\circ}$" for i in np.linspace(0, 3, 7, endpoint=True)])
        ax.set_title(f'{stype[:2]}/{stype[2:4]}/{stype[4:]}', fontsize=fsize, fontname='times')
        ax.legend(loc='lower right', fontsize=fsize-3, framealpha=1)
        ax.tick_params(labelsize=fsize)
        # print(th12_deg, val[val[:,1]==th12_deg,1][0], (val[val[:,1]==th12_deg,2][0]-eref)*1000)
        ax.vlines(th12_deg,
                   ymin=-1, 
                   ymax=(etots[ind]-eref)*1000,  
                   alpha=0.5, lw=2,
                   color=mcolor)
        ax.grid('on', alpha=0.5)


fig.savefig(f"{datadir}fig1_0.pdf")
fig.savefig(f"{datadir}fig1_0.png",dpi=300 )
