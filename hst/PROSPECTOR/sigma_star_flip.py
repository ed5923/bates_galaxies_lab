import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
from astropy.cosmology import FlatLambdaCDM
from astropy.constants import G
from astropy import constants as const
from astropy import units as u

galaxies =              ['J0826','J0901','J0905','J0944','J1107','J1219','J1341','J1506','J1558','J1613','J2116','J2140']
#nuc_best_mass = np.array([10.20, 10.07,  10.41,  10.14,  10.11,  10.72,  10.51,  10.18,  9.81,  10.52,  10.68,  10.74])
nuc_best_mass =  np.array([10.27, 10.11,  10.41,  10.20,  10.11,  10.45,  10.51,  10.18,  9.85,  10.65,  10.68,  10.56])
#nuc_up_mass =    np.array([0.26,  0.28,   0.29,   0.18,   0.34,   0.25,   0.15,   0.21,  0.12,   0.20,   0.15,   0.25])
nuc_up_mass =     np.array([0.04,  0.05,   0.29,   0.11,   0.34,   0.10,   0.15,   0.21,  0.11,   0.07,   0.15,   0.10])
#nuc_lo_mass =    np.array([0.24,  0.25,   0.24,   0.18,   0.31,   0.42,   0.25,   0.20,  0.16,   0.23,   0.25,   0.27])
nuc_lo_mass =     np.array([0.05,  0.06,   0.24,   0.16,   0.31,   0.07,   0.25,   0.20,  0.11,   0.13,   0.25,   0.07])

#vflow = np.array([          1228,  1206,   2470,   1778,   1828,   1830,    875,   1211,   829,   2416,   1456,    606])
vflow = np.array([           1600,  1700,   3000,   2100,   1828,   2250,   2000,   2050,  1350,   2600,   1900,   1100])

nuc_up_mass = np.sqrt(nuc_up_mass**2 + 0.1**2)
nuc_lo_mass = np.sqrt(nuc_lo_mass**2 + 0.1**2)

tot_best_mass = np.array([10.57, 10.47, 10.67, 10.52, 10.57, 11.40, 10.53, 10.57, 10.79, 11.50, 10.94, 10.92])
tot_up_mass = np.array([0.01, 0.01, 0.03, 0.03, 0.02, 0.11, 0.04, 0.02, 0.09, 0.10, 0.06, 0.02])
tot_up_mass = np.sqrt(tot_up_mass**2 + 0.075**2)
tot_lo_mass = np.array([0.01, 0.01, 0.03, 0.02, 0.01, 0.11, 0.03, 0.02, 0.06, 0.11, 0.06, 0.03])
tot_lo_mass = np.sqrt(tot_lo_mass**2 + 0.075**2)

re_best = np.array([0.0151, 0.0149, 0.0105, 0.0099, 0.0156, 0.0257, 0.0127, 0.0118, 0.0387, 0.1289, 0.0216, 0.0145]) 
re_unc = np.array([0.0031, 0.0033, 0.0027, 0.0030, 0.0041, 0.0038, 0.0023, 0.0025, 0.0064, 0.0157, 0.0046, 0.0045])
re_best_arc = re_best * u.arcsec

z = np.array([0.603, 0.459, 0.712, 0.514, 0.467, 0.451, 0.658, 0.608, 0.402, 0.449, 0.728, 0.752])


cosmo = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Om0=0.3)

re_best_kpc = re_best_arc / cosmo.arcsec_per_kpc_proper(z)

sigma_star_corr = np.array([0.96/0.5, 0.97/0.5, 0.98/0.5, 0.99/0.5, 0.97/0.5, 0.93/0.5, 0.97/0.5, 0.98/0.5, 0.88/0.5, 0.58/0.5, 0.92/0.5, 0.96/0.5])

sigma_star_1kpc = 10**nuc_best_mass / (2. * np.pi * 1**2) * sigma_star_corr

sigma_star_best = 10**nuc_best_mass / (2. * np.pi * re_best_kpc**2) * u.kpc * u.kpc

sigma_star_hi = 10**(nuc_best_mass + nuc_up_mass) / (2. * np.pi * (re_best_kpc-(re_unc/re_best*re_best_kpc))**2) * u.kpc * u.kpc

sigma_star_lo = 10**(nuc_best_mass - nuc_lo_mass) / (2. * np.pi * (re_best_kpc+(re_unc/re_best*re_best_kpc))**2) * u.kpc * u.kpc

sigma_star_hi_re = 10**(nuc_best_mass) / (2. * np.pi * (re_best_kpc-(re_unc/re_best*re_best_kpc))**2) * u.kpc * u.kpc

sigma_star_lo_re = 10**(nuc_best_mass) / (2. * np.pi * (re_best_kpc+(re_unc/re_best*re_best_kpc))**2) * u.kpc * u.kpc

sigma_star_hi_mass = 10**(nuc_best_mass + nuc_up_mass) / (2. * np.pi * (re_best_kpc)**2) * u.kpc * u.kpc

sigma_star_lo_mass = 10**(nuc_best_mass - nuc_lo_mass) / (2. * np.pi * (re_best_kpc)**2) * u.kpc * u.kpc



filename = 'sigma_star_flip.pdf'

with PdfPages(filename) as pdf:
    
    fig = plt.figure()

    vel_array = np.arange(101)*30

    plt.axvline(x=3e11, color='#2ca02c', linestyle='dashed')
    plt.axvspan(3e11/2, 3e11*2, alpha=0.5, color='#2ca02c')
    
    #plt.plot(vel_array, vel_array)

    eb = plt.errorbar(sigma_star_best, vflow, xerr=[sigma_star_best-sigma_star_1kpc,np.zeros(len(vflow))], fmt='none', elinewidth=1, color='#ff7f0e', label=r'[$\Sigma_{1}$, $\Sigma_{r_e}$]')
    eb[-1][0].set_linestyle('dotted') #eb1[-1][0] is the LineCollection objects of the errorbar lines

    plt.errorbar(sigma_star_best, vflow, xerr=[sigma_star_best-sigma_star_lo, sigma_star_hi-sigma_star_best], fmt='none', elinewidth=1, label=r'$r_e$ and mass uncertainty')
    #plt.plot(vel_array, vel_array/3, linestyle='--')
    #plt.errorbar(vflow, sigma_star_best, yerr=[sigma_star_best-sigma_star_lo_mass, sigma_star_hi_mass-sigma_star_best], fmt='o')    
    plt.errorbar(sigma_star_best, vflow, xerr=[sigma_star_best-sigma_star_lo_re, sigma_star_hi_re-sigma_star_best], fmt='none', elinewidth=3, label=r'$r_e$ uncertainty')
    #plt.xlim(0,3500)
    plt.scatter(sigma_star_best, vflow, label=r'$\Sigma (r=r_e)$', color='#ff7f0e')

    
    plt.scatter(sigma_star_1kpc, vflow, marker='*', label=r'$\Sigma (r=1$ kpc)', color='#ff7f0e')

    plt.text(3.5e11, 750, r'$\Sigma=\Sigma_{Eddington}$', rotation=90, fontsize=14)


    
    plt.xlim(1e9, 3e12)
    
    #plt.ylim(800,3200)
    plt.ylim(-500,3200)
    plt.ylabel(r'Observed Outflow Velocity [km s$^{-1}$]', fontsize=13)
    plt.xlabel(r'Central Stellar Surface Density [M$_\odot$ kpc$^{-2}$]', fontsize=13)
    plt.xscale('log')
    plt.tick_params(axis='both', which='major', labelsize=12)

    plt.legend(fontsize=12, loc='lower left')

    #for i in range(0, len(galaxies)):
    #    plt.text(sigma_star_best[i], vflow[i], galaxies[i])
    
    pdf.savefig()
    plt.close()

    

os.system('open %s &' % filename)
