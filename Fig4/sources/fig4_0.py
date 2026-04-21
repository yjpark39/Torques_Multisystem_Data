import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import splev, splrep, griddata 

params = {
              'font.family' : 'Times'
}
matplotlib.rcParams.update(params)

datadir  = '/Users/yjpark/YJ/Projects/Multisystem/Figures/fig4/sources/'
datadir1 = '/Users/yjpark/YJ/Projects/Multisystem/Figures/fig4/sources/data_energymap/'
datadir2 = '/Users/yjpark/YJ/Projects/Multisystem/Figures/fig4/sources/data_energycurve/'

eref = -6.95728737246473 # GBNBN/Typ2/AAA

# ----- Figure Generation -----
fig_width   = 6.9 #6.9 # inches
golden_mean = (np.sqrt(5)-1.0)/2.0    # Aesthetic ratio
fig_height = fig_width*golden_mean*1 # height in inche
fig = plt.figure(figsize=(fig_width, fig_height))
msize, fsize = 3, 10

gs0 = gridspec.GridSpec(2, 2, figure=fig, width_ratios=[1.2,1.6])
gs0.update(wspace=0.4   , hspace=0.5) # set the spacing between axes.

# ----- Panel (a) : ENERGY MAP -----
FLAG = "_12x12" # dummy flag for reading the data

ax1s = [fig.add_subplot(gs00)  for gs00 in gs0[0, 0].subgridspec(1, 2)]
ax2s = [fig.add_subplot(gs00)  for gs00 in gs0[1, 0].subgridspec(1, 2)]
for sysname, axs in zip(['GBNBN', 'GBNNB'],
                       [ax1s, ax2s]):
    for stype, stype_name, ax in zip(["1", "2"],["Type I","Type II"],
                            axs):
        val = np.genfromtxt(f"{datadir1}energymap_{sysname}_Typ{stype}{FLAG}.dat", skip_header=1)

        XX0, YY0, data00 = val[:,0], val[:,1]*np.sqrt(3)/2, val[:,-1]/val[:,-3]

        XX, YY, data0 = [], [], []
        for ddi, ddj in [[0,0],[1/2, np.sqrt(3)/2], [-1/2, np.sqrt(3)/2]]:
            XX.append(XX0 + ddi) 
            YY.append(YY0 + ddj)
            data0.append(data00)
        XX = np.array(XX).ravel()
        YY = np.array(YY).ravel()

        XX = 1-XX
        YY = np.sqrt(3)-YY
        data0 = np.array(data0).ravel()

        vvmin, vvmax  = np.min(data0), np.max(data0)
        print(f"{sysname}_Typ{stype}: EMIN, EMAX : ({(vvmin-eref)*1000:.2f}, {(vvmax-eref)*1000:.2f})") 
        # ax.scatter(XX,YY, s=msize, c=data0, vmin=vvmin, vmax=vvmax, cmap='jet')

        num       = 1601
        margin    = 0.1
        L         = np.sqrt(3)
        x         = np.linspace(0, 1         ,num, endpoint=True)
        y         = np.linspace(0, np.sqrt(3),num, endpoint=True)

        val_sp    = griddata((XX, YY),data0,
                                (x[None,:], y[:,None]), method='linear') # , method='cubic')

        im = ax.imshow(val_sp, vmin=vvmin, vmax = vvmax,  #, cmap='gist_ncar')
                        extent=[0, 1,0, np.sqrt(3)],origin="lower",cmap='jet')

        ax.set_aspect('equal')
        ax.set_xlim(0,1)
        ax.set_ylim(0, np.sqrt(3))
        ax.set_xticks([0, 1])
        ax.set_yticks(np.linspace(0, np.sqrt(3), 4, endpoint=True))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        # if sysname=='GBNBN': ax.set_title(f"{stype_name}", fontsize=fsize, fontname='times')
        ax.set_title(f"{stype_name}", fontsize=fsize, fontname='times')


# ----- Panel (b) : ENERGY CURVE -----
axRs = [fig.add_subplot(gs0[i, 1]) for i in range(2)] 

inds_GBNBN   = [[0,1, -3,-2,-1], # I
               [0,1,   -3,-2,-1]] # II
inds_GBNNB   = [[0,1, -3,-2,-1],  # I
                [0,1, -3,-2,-1]]     # II

for sysname, ax, mtype, stack_names, stack_names2, stack_names3, spl_inds, mcolors, th32_deg, th32_deg_2times in zip(
                            ['GBNBN', 'GBNNB'],
                            axRs, 
                            ['o','o','s'],
                            [["$\\overline{\\rm AAA}$", "$\\overline{\\rm AAC}$"], 
                             ["$\\overline{\\rm A^{\\prime}AB}$", "$\\overline{\\rm A^{\\prime}AA}$"]],
                             [["AB", "AA"],["AA", "AB"]],
                             [["AC", "AB"],["AC", "AC"]],
                            [inds_GBNBN, inds_GBNNB],
                            [['C0', 'C1'],['C2', 'C3']],
                            [0.579824, 0.579824],
                            [1.170136, 1.170136]):
    
    ax.vlines(th32_deg,
        ymin=-0.2, 
        ymax=0.8,   
        alpha=0.5, lw=2,
        color='gray')

    for stype, stype_name, mcolor, stack_name,stack_name2,stack_name3, spl_ind, th12_deg in zip(
                                ["1", "2"],["Type I", "Type II"],
                                mcolors, stack_names,stack_names2,stack_names3,spl_inds,
                                [1.202325, -1.202855]):
        val = np.genfromtxt(f"{datadir2}energycurve_{sysname}_Typ{stype}.dat", skip_header=1)
        ang32_degs, etots = val[:,1], val[:,-1]/val[:,2]


        ax.plot(ang32_degs, (etots-eref)*1000,mtype, ms= msize, color=mcolor, lw=0.5, label=f"{stype_name}  ( {stack_name} )") #, label="$\\theta_{12} = "+f"{th12_deg:.3f}"+"\\degree$ - "+f"{stack_name}")

        val_2 = np.genfromtxt(f"{datadir2}energycurve_{sysname}_Typ{stype}.{stack_name2}.dat", skip_header=1)
        ang32_degs_2, etots_2 = val_2[:,1], val_2[:,-1]/val_2[:,2]

        val_3 = np.genfromtxt(f"{datadir2}energycurve_{sysname}_Typ{stype}.{stack_name3}.dat", skip_header=1)
        ang32_degs_3, etots_3 = val_3[:,1], val_3[:,-1]/val_3[:,2]

        # Fitting curves
        etots_combined = etots.copy()
        for ang32_2, etot_2 in zip(ang32_degs_2, etots_2):
            ind_2 = list(ang32_degs).index(ang32_2)
            if etot_2 < etots_combined[ind_2]:
                etots_combined[ind_2] = etot_2
        for ang32_3, etot_3 in zip(ang32_degs_3, etots_3):
            ind_3 = list(ang32_degs).index(ang32_3)
            if etot_3 < etots_combined[ind_3]:
                etots_combined[ind_3] = etot_3

        angs_max, etots_max = ang32_degs_2.copy(), etots_2.copy()
        for ang32_0, etot_0 in zip(ang32_degs, etots):
            try:
                ind_0 = list(angs_max).index(ang32_0)
                if etot_0 > etots_max[ind_0]:
                    etots_max[ind_0] = etot_0
            except:
                continue
        for ang32_3, etot_3 in zip(ang32_degs_3, etots_3):
            try:
                ind_3 = list(angs_max).index(ang32_3)
                if etot_3 > etots_max[ind_3]:
                    etots_max[ind_3] = etot_3
            except:
                continue

        angs_min, etots_min = ang32_degs_2.copy(), etots_2.copy()
        for ang32_0, etot_0 in zip(ang32_degs, etots):
            try:
                ind_0 = list(angs_min).index(ang32_0)
                if etot_0 <= etots_min[ind_0]:
                    etots_min[ind_0] = etot_0
            except:
                continue
        for ang32_3, etot_3 in zip(ang32_degs_3, etots_3):
            try:
                ind_3 = list(angs_min).index(ang32_3)
                if etot_3 <= etots_min[ind_3]:
                    etots_min[ind_3] = etot_3
            except:
                continue
        
        ax.plot(ang32_degs, (etots_combined-eref)*1000,'-', marker=mtype, ms=msize, color=mcolor, lw=0.5)#, label=f"{stype_name}  ( {stack_name} )") #, label="$\\theta_{12} = "+f"{th12_deg:.3f}"+"\\degree$ - "+f"{stack_name}")


        ax.plot(angs_min, (etots_min-eref)*1000,"o", ms=msize+1, color=mcolor, lw=0.1, mfc="w")#, label=f"{stype_name}  ( {stack_name} )") #, label="$\\theta_{12} = "+f"{th12_deg:.3f}"+"\\degree$ - "+f"{stack_name}")

        ax.errorbar(angs_min, (etots_min-eref)*1000, np.vstack(( np.zeros_like(etots_min), (etots_max-etots_min)*1000)), fmt="none", color=mcolor, capsize=4, capthick=1, elinewidth=1)#, barsabove=True)

        spl    = splrep(ang32_degs[spl_ind],etots_combined[spl_ind])
        theta  = np.linspace(np.min(ang32_degs),np.max(ang32_degs))
        fitted = splev(theta,spl)
        
        ax.plot(theta,(fitted-eref)*1000,"--",color=mcolor,linewidth=0.9)

        ax.fill_between(ang32_degs, (etots_combined-eref)*1000, (splev(ang32_degs,spl)-eref)*1000 , color=mcolor, alpha=0.3)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)

        # print(fitted[0])

        ind=list(ang32_degs).index(th32_deg)
        ang = ang32_degs
        val = (etots-eref)*1000
        slope_L = (val[ind]-val[ind-1])/np.deg2rad(ang[ind]-ang[ind-1])
        slope_R = (val[ind+1]-val[ind])/np.deg2rad(ang[ind+1]-ang[ind])
        print(f"Slope: {ang[ind-1]},{ang[ind]},{ang[ind+1]}: {slope_L:.2f}, {slope_R:.2f}")

        ind  = np.where(ang32_degs == th32_deg)[0][0]
        val1 = (splev(np.array([th32_deg]),spl)-eref)*1000
        print(f"Binding E:  {ang[ind]:.6f}, {val[ind]:.3f}, {val1[0]:.3f}, {val1[0]-val[ind]:.3f}")


        ax.set_ylabel("$E^{tot}$ (meV/atom)", fontsize=fsize, fontname='times')
        # if stype=='BNNBBN': 
        ax.set_xlabel("$\\theta_{32}$", fontsize=fsize, fontname='times')

        
        ax.set_xlim(-0.1,1.6)
        ax.set_xticks(np.linspace(0, 1.5, 4, endpoint=True))
        ax.set_xticklabels([f"{i:.1f}"+"$^{\\circ}$" for i in np.linspace(0, 1.5, 4, endpoint=True)])

        if  sysname == "GBNBN":
            ax.set_ylim(-0.05,0.55)
            ax.set_yticks(np.linspace(0,0.5, 6, endpoint=True))
        elif sysname== "GBNNB":
            ax.set_ylim( 0.2,0.8)
            ax.set_yticks(np.linspace(0.2,0.8, 7, endpoint=True))
        ax.set_title(f'{sysname[0]}/{sysname[1:3]}/{sysname[3:]}', fontsize=fsize, fontname='times')
        
        ax.legend(loc='upper center', fontsize=fsize-3, framealpha=1, ncols=2)
        ax.tick_params(labelsize=fsize)

        print('')
        ax.grid('on', alpha=0.5)

    
fig.savefig(f"{datadir}fig4_0.pdf")
fig.savefig(f"{datadir}fig4_0.png",dpi=300 )
