
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

params = {
            'font.family' : 'Times'
        }
matplotlib.rcParams.update(params)

# datadir = "/Users/yjpark/YJ/Projects/Multisystem/ElectroStaticBenchmark_t3BN/efield0.0/"
datadir2write = "/Users/yjpark/YJ/Projects/Multisystem/Figures/figS1/sources/"

def Vfunc(r_ij, lam=0.7, rcut=16, Tap_on=False):
    r_ij = np.abs(r_ij)
    VV = (r_ij**3+(1/lam)**3)**(-1/3)
    if Tap_on:
        fac = 20*(r_ij/rcut)**7 - 70*(r_ij/rcut)**6 + 84*(r_ij/rcut)**5 - 35*(r_ij/rcut)**4 + 1
        VV *= fac
    return  VV


rcut = 10
rr   = np.linspace(0,rcut, 51, endpoint=True)

lam1, lam2, lam3       = 0.7, 1.0, 3.2
V1   = Vfunc(rr, lam=lam1, rcut=rcut, Tap_on=True)
V2   = Vfunc(rr, lam=lam2, rcut=rcut, Tap_on=True)
V3   = Vfunc(rr, lam=lam3, rcut=rcut, Tap_on=True)
V4   = Vfunc(rr, lam=3.2 , rcut=32  , Tap_on=True)


fig          = plt.figure(figsize=(3,6))
msize, fsize = 5, 16
ax1          = fig.add_axes([0.38, 0.63 , 0.57, 0.35])
ax2          = fig.add_axes([0.38, 0.1 , 0.57, 0.35])

ax1.plot(rr, 1/np.abs(rr),ls='-', color='k', lw=2.5, label="$V_\\text{bare}$")

ax1.plot(rr,   V1, 'o',color='C0',lw=2,ms=msize+1, label="$(\\lambda, r_{\\rm cut})=("+f"{lam1} [1/\AA], {rcut} [\AA])")
ax1.plot(rr,   V2, 'o',color='C1',lw=2,ms=msize  , label="$(\\lambda, r_{\\rm cut})=("+f"{lam2} [1/\AA], {rcut} [\AA])")

ax1.plot(rr,   V4, 'o',color='C3', lw=2,ms=msize , label="$(\\lambda, r_{\\rm cut})=("+f"{3.2 } [1/\AA], {32  } [\AA])")
ax1.plot(rr,   V3, 'o',color='C2',lw=2,ms=msize-1, label="$(\\lambda, r_{\\rm cut})=("+f"{lam3} [1/\AA], {rcut} [\AA])")


ax1.set_xlabel('r ($\\AA$)', fontsize=fsize, fontname='times')
ax1.set_ylabel('V(r)'      , fontsize=fsize, fontname='times')


ax1.set_xlim(0, rcut); ax1.set_xticks(np.linspace(0, rcut, 6, endpoint=True))
ax1.set_ylim(-0.1, 1.6); ax1.set_yticks(np.linspace(0, 1.5, 4, endpoint=True))


ax1.tick_params(labelsize=fsize)
ax1.axvline(x= 0   , ls='-', color='gray')
ax1.axvline(x=-rcut, ls='-', color='gray')
ax1.axvline(x= rcut, ls='-', color='gray')



fcut    = -5
data    = np.genfromtxt(f"{datadir2write}data_coul_long_c/energy_fcut{fcut}.dat", skip_header=1)
fcut    = -6
data2   = np.genfromtxt(f"{datadir2write}data_coul_long_c/energy_fcut{fcut}.dat", skip_header=1)
fcut    = -7
data3   = np.genfromtxt(f"{datadir2write}data_coul_long_c/energy_fcut{fcut}.dat", skip_header=1)


ensref  = data3[-1,-1]/data3[-1,-3]


ax2.plot( data[ :,0], (data[ :,-1]/data[ :,-3]-ensref)*1000, 'ko-' ,ms=msize, label="$f_\\text{cut}=10^{-5}$eV/\AA")
ax2.plot( data2[:,0], (data2[:,-1]/data2[:,-3]-ensref)*1000, 'bo-' ,ms=msize, label="$f_\\text{cut}=10^{-6}$eV/\AA")
ax2.plot( data3[:,0], (data3[:,-1]/data3[:,-3]-ensref)*1000, 'ro-' ,ms=msize, label="$f_\\text{cut}=10^{-7}$eV/\AA")
ax2.set_xlabel("$r_{cut} (\AA)$", fontsize=fsize-2, fontname='times')
ax2.set_xlim(0,20); ax2.set_xticks(np.linspace(0,20, 5, endpoint=True))
ax2.set_ylim(-0.02,0.06); ax2.set_yticks(np.linspace(-0.02,0.06, 5, endpoint=True))

ax2.tick_params(labelsize=fsize)

ax2.set_ylabel("$E_{\\rm tot}$", fontsize=fsize, fontname='times')
ax2.set_ylabel("$E_{\\rm tot}-E_{\\rm ref}$", fontsize=fsize, fontname='times')

fig.savefig(f"{datadir2write}figS1_0_ac.pdf")