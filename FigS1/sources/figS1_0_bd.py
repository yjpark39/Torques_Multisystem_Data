
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import splev, splrep #, griddata # interp1d


params = {
        'font.family' : 'Times'
        }
matplotlib.rcParams.update(params)
plt.rcParams['text.usetex'] = True

datadir2write = "/Users/yjpark/YJ/Projects/Multisystem/Figures/figS1/sources/"

ensref = -6.7150814  # BNBNBN (1.08, 1.08)


data1   = np.genfromtxt(f"{datadir2write}data_efield0.00/data_ref/energy_wo_coul.dat", 
                        skip_header=1)

rcut, lambda0, TapOX = 32, 3.2, 'True'
data2   = np.genfromtxt(f"{datadir2write}data_efield0.00/data_coul_shield/energy_rcut{rcut}_lambda{lambda0}_Tap{TapOX}.dat", 
                        skip_header=1)

rcut, fcut = 16, -7
data3   = np.genfromtxt(f"{datadir2write}data_efield0.00/data_coul_long/energy_rcut{rcut}_fcut{fcut}.dat", 
                        skip_header=1)

angref = 1.084549


cond1 = np.logical_and( data1[:,0] == angref , data1[:,1] == angref ); print(data1[cond1,0:2])
cond2 = np.logical_and( data2[:,0] == angref , data2[:,1] == angref ); print(data2[cond2,0:2])
cond3 = np.logical_and( data3[:,0] == angref , data3[:,1] == angref ); print(data3[cond3,0:2])

eref1 = (data1[cond1,-1]/data1[cond1,-3])[0]*1000; print(f'w/o coulomb      case : {eref1/1000:18.10f} eV/atom; E_ref       = {eref1-ensref*1000:12.6f} meV/atom; {eref1-ensref*1000-(eref1-ensref*1000):12.6f} meV/atom')
eref2 = (data2[cond2,-1]/data2[cond2,-3])[0]*1000; print(f'coul/shield      case : {eref2/1000:18.10f} eV/atom; E_ref^shield= {eref2-ensref*1000:12.6f} meV/atom; {eref2-ensref*1000-(eref1-ensref*1000):12.6f} meV/atom')
eref3 = (data3[cond3,-1]/data3[cond3,-3])[0]*1000; print(f'coul/long        case : {eref3/1000:18.10f} eV/atom; E_ref^long  = {eref3-ensref*1000:12.6f} meV/atom; {eref3-ensref*1000-(eref1-ensref*1000):12.6f} meV/atom')

fig      = plt.figure(figsize=(6,6))
msize, fsize = 7, 16
msize, fsize = 4, 16

ax1 = fig.add_axes([0.16, 0.63, 0.62, 0.35])
ax2 = fig.add_axes([0.16, 0.1 , 0.62, 0.35])

for iangg, angg in enumerate( [1.084549, 1.538500, 2.004628] ):
    cond1 = data1[:,0] == angg 
    cond2 = data2[:,0] == angg 
    cond3 = data3[:,0] == angg 

    if iangg == 0:
        
        ax1.plot(data1[ cond1 ,1], (data1[ cond1 ,-1]/data1[ cond1 ,-3])*1000-eref1, 'o:' , label="Without \\texttt{coul/shield}",  lw=0.8, color=f'C{iangg}',ms=msize, alpha=0.3)
        ax1.plot(data2[ cond2 ,1], (data2[ cond2 ,-1]/data2[ cond2 ,-3])*1000-eref2, '^-' , label="With    \\texttt{coul/shield}",  lw=0.8, color=f'C{iangg}',ms=msize-1)#, alpha=0.3)
        ax2.plot(data1[ cond1 ,1], (data1[ cond1 ,-1]/data1[ cond1 ,-3])*1000-eref1, 'o:' , label="Without \\texttt{coul/long}"  ,  lw=0.8, color=f'C{iangg}',ms=msize, alpha=0.3)
        ax2.plot(data3[ cond3 ,1], (data3[ cond3 ,-1]/data3[ cond3 ,-3])*1000-eref3, 's-' , label="With    \\texttt{coul/long}"  ,  lw=0.8, color=f'C{iangg}',ms=msize-1)#, alpha=0.3)

        th,ens = data1[ cond1 ,1], (data1[ cond1 ,-1]/data1[ cond1 ,-3])*1000-eref1
        ind    = list(th).index(angg)
        spl0   = splrep(th[[0,-1]], ens[[0,-1]], k=1)
        ax1.fill_between(th, ens, splev(th,spl0) , color=f'C{iangg}', alpha=0.2)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)

        th,ens = data2[ cond2 ,1], (data2[ cond2 ,-1]/data2[ cond2 ,-3])*1000-eref2
        ind    = list(th).index(angg)
        spl0   = splrep(th[[0,-1]], ens[[0,-1]], k=1)
        ax1.fill_between(th, ens, splev(th,spl0) , color=f'C{iangg}', alpha=0.4)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)

        th,ens = data1[ cond1 ,1], (data1[ cond1 ,-1]/data1[ cond1 ,-3])*1000-eref1
        ind    = list(th).index(angg)
        spl0   = splrep(th[[0,-1]], ens[[0,-1]], k=1)
        ax2.fill_between(th, ens, splev(th,spl0) , color=f'C{iangg}', alpha=0.2)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)

        th,ens = data3[ cond3 ,1], (data3[ cond3 ,-1]/data3[ cond3 ,-3])*1000-eref3
        ind    = list(th).index(angg)
        spl0   = splrep(th[[0,-1]], ens[[0,-1]], k=1)
        ax2.fill_between(th, ens, splev(th,spl0) , color=f'C{iangg}', alpha=0.4)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)

    else:
        ax1.plot(data1[ cond1 ,1], (data1[ cond1 ,-1]/data1[ cond1 ,-3])*1000-eref1, 'o:' ,lw=0.8, color=f'C{iangg}',ms=msize, alpha=0.3)
        ax1.plot(data2[ cond2 ,1], (data2[ cond2 ,-1]/data2[ cond2 ,-3])*1000-eref2, '^-' ,lw=0.8, color=f'C{iangg}',ms=msize)#, alpha=0.3)
        ax2.plot(data1[ cond1 ,1], (data1[ cond1 ,-1]/data1[ cond1 ,-3])*1000-eref1, 'o:' ,lw=0.8, color=f'C{iangg}',ms=msize, alpha=0.3)
        ax2.plot(data3[ cond3 ,1], (data3[ cond3 ,-1]/data3[ cond3 ,-3])*1000-eref3, 's-' ,lw=0.8, color=f'C{iangg}',ms=msize)#, alpha=0.3)

        th,ens = data1[ cond1 ,1], (data1[ cond1 ,-1]/data1[ cond1 ,-3])*1000-eref1
        ind    = list(th).index(angg)
        spl0   = splrep(th[[0,-1]], ens[[0,-1]], k=1)
        
        ax1.fill_between(th, ens, splev(th,spl0) , color=f'C{iangg}', alpha=0.2)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)

        th,ens = data2[ cond2 ,1], (data2[ cond2 ,-1]/data2[ cond2 ,-3])*1000-eref2
        ind    = list(th).index(angg)
        spl0   = splrep(th[[0,-1]], ens[[0,-1]], k=1)
        
        ax1.fill_between(th, ens, splev(th,spl0) , color=f'C{iangg}', alpha=0.4)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)

        th,ens = data1[ cond1 ,1], (data1[ cond1 ,-1]/data1[ cond1 ,-3])*1000-eref1
        ind    = list(th).index(angg)
        spl0   = splrep(th[[0,-1]], ens[[0,-1]], k=1)
        
        ax2.fill_between(th, ens, splev(th,spl0) , color=f'C{iangg}', alpha=0.2)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)

        th,ens = data3[ cond3 ,1], (data3[ cond3 ,-1]/data3[ cond3 ,-3])*1000-eref3
        ind    = list(th).index(angg)
        spl0   = splrep(th[[0,-1]], ens[[0,-1]], k=1)
        
        ax2.fill_between(th, ens, splev(th,spl0) , color=f'C{iangg}', alpha=0.4)  # ax.fill_betweenx(y, x1, x2, color='k', alpha=0.3)

    ax1.axvline(x=angg, ls='-', color=f'C{iangg}', alpha=0.5)
    ax2.axvline(x=angg, ls='-', color=f'C{iangg}', alpha=0.5)

    
ax1.axhline(y=0, ls='-', color='gray', alpha=0.5)
ax2.axhline(y=0, ls='-', color='gray', alpha=0.5)

ax1.set_xlabel("$\\theta_{32}\\ (^{\\circ}$)", fontsize=fsize, fontname='times')
ax2.set_xlabel("$\\theta_{32}\\ (^{\\circ}$)", fontsize=fsize, fontname='times')


ax1.set_xlim(0.5,2.5); ax1.set_xticks(np.linspace(0.5, 2.5,5, endpoint=True))
ax2.set_xlim(0.5,2.5); ax2.set_xticks(np.linspace(0.5, 2.5,5, endpoint=True))


ax1.set_ylim(-0.5,2.5); ax1.set_yticks(np.linspace(-0.5, 2.5, 7, endpoint=True))
ax2.set_ylim(-0.5,2.5); ax2.set_yticks(np.linspace(-0.5, 2.5, 7, endpoint=True))

ax1.legend(  fontsize=fsize-3, loc='upper left' , ncol=1, framealpha=1)#, title="No Coulomb")
ax2.legend(  fontsize=fsize-3, loc='upper left' , ncol=1, framealpha=1)#, title="No Coulomb")

ax1.tick_params(labelsize=fsize) 
ax2.tick_params(labelsize=fsize) 
ax1.set_ylabel("$E_{\\rm tot}$ (meV/atom)", fontsize=fsize, fontname='times')
ax2.set_ylabel("$E_{\\rm tot}$ (meV/atom)", fontsize=fsize, fontname='times')

fig.savefig(f"{datadir2write}figS1_0_bd.pdf")

plt.rcParams['text.usetex'] = False