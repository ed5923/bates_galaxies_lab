import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from astropy.io import fits
from astropy.io import ascii
from astropy.cosmology import WMAP9 as cosmo
from scipy.constants import parsec as prsc
from scipy.constants import c as lightspeed
import astropy.units as u
import matplotlib.ticker as ticker
import pandas as pd
from uncertainties import ufloat_fromstr
from uncertainties import ufloat
from uncertainties import umath
from matplotlib.ticker import ScalarFormatter




# Importing the Umeh table
table = ascii.read('C:/Users/Chris/Documents/GitHub/bates_galaxies_lab/hst/umeh_table.dat')
umeh_names = np.array(table.field('Galaxy'))
umeh_w4mag = np.array(table.field('w4_mag'))
umeh_w4unc = np.array(table.field('w4_unc'))
# Redshifts for the galaxies in Umeh table taken from Tremonti table
umeh_Z_T = np.array([0.6031527, 0.45889184, 0.711421, 0.51383984, 0.46653742, 0.45092207, 0.66115844, 0.6080914,
                     0.402196, 0.44924328, 0.72798246, 0.7509297])
umeh_shortnames = np.array(['J0826+4305', 'J0901+0314', 'J0905+5759', 'J0944+0930', 'J1107+0417', 'J1219+0336',
                            'J1341-0321', 'J1506+5402', 'J1558+3957', 'J1613+2834', 'J2116-0634', 'J2140+1209'])

# Creating arrays with the Tremonti table
ChristyTablePath = 'files/hizea_wind_ancillary.fit'
ChristyTable = fits.open(ChristyTablePath)
ShortNames = ChristyTable[1].data['SHORT_NAME']
ChristyMass = ChristyTable[1].data['MASS']
ChristySFR = ChristyTable[1].data['SFR']
ChristyV50 = ChristyTable[1].data['VAVG']
ChristyV98 = ChristyTable[1].data['VMAX']
ChristyAge = ChristyTable[1].data['LW_AGE']
ChristyZ = ChristyTable[1].data['Z']

# Importing data pertaining to Hg/Hb Ratios
ratioscsv = pd.read_csv('Hb-Hg-ratios.csv')
rat_str = np.array(ratioscsv['Hg/Hb Ratio'])
rat_unc = np.array([ufloat_fromstr(i) for i in rat_str])
ratiofullnames = ratioscsv['Unnamed: 0']
rationames = np.array([x[21:26] for x in ratiofullnames])
rationamenumbers = np.array([int(x[1:]) for x in rationames])
ratio_indxs = np.argsort(rationamenumbers)


# The strong_MgII_abs tells whether the flux goes to zero for this particular line. I write False for galaxies
# Jose didn't include in his April Thesis Presentation: 1107, 1712, 3118
class OurGalaxy:
    def __init__(self, name, sfr, sfr_u, logmass, mass_upunc, mass_lowunc, v50, v98, strong_MgII_abs, MTTMaGEVels):
        self.name = name
        self.sfr = sfr
        self.sfr_u = sfr_u
        self.logmass = logmass
        self.mass_upunc = mass_upunc
        self.mass_lowunc = mass_lowunc
        self.v50 = v50
        self.v98 = v98
        self.strong_MgII_abs = strong_MgII_abs
        self.MTTMaGEVels = MTTMaGEVels

 # galaxies  J1125, J1232, J1450, J1713, and J2118 have no mass from pospector
J0826 = OurGalaxy('J0826+4305',  10.6,   1.2,    10.71,  0.02,   0.01,   850.21,    1220.36, True, [995.96, 1319.68])
J0901 = OurGalaxy('J0901+0314',  6.5,    0.5,    10.59,  0.01,   0.01,   0,         0,       False, [1199.32, 1506.72])
J0905 = OurGalaxy('J0905+5759',  14.3,   1.5,    10.75,  0.02,   0.02,   2476.77,   2913.18, True, [2350.23, 2556.89])
J0944 = OurGalaxy('J0944+0930',  5.2,    0.7,    10.74,  0.04,   0.03,   1241,      1747.79, True, [1205.41, 1654.76])
J1107 = OurGalaxy('J1107+0417',  5.8,    0.4,    10.68,  0.02,   0.02,   1626.14,   1995.31, False, [1419.17, 1930.34])
J1125 = OurGalaxy('J1125-0145',  2.5,    0.8,    0,      0,      0,      0,         0,       False, [np.nan, np.nan])
J1219 = OurGalaxy('J1219+0336',  3.8,    0.5,    11.34,  0.02,   0.02,   1586.07,   1818.08, True, [1575.3, 1799.78])
J1232 = OurGalaxy('J1232+0723',  2.48,   0.32,   0,      0,      0,      44.93,     347.02,  False, [250.12, 675.4])
J1341 = OurGalaxy('J1341-0321',  19.7,   1.6,    10.61,  0.02,   0.02,   711.96,    1700.5,  False, [618.22, 1086.92])
J1450 = OurGalaxy('J1450+4621',  5,      4,      0,      0,      0,      406.4,     1189.78, True, [482.23, 1444.45])
J1506 = OurGalaxy('J1506+5402',  21.3,   1.1,    10.65,  0.02,   0.03,   1998.43,   1499.38, False, [1268.41, 1747.68])
J1558 = OurGalaxy('J1558+3957',  6.61,   0.34,   10.97,  0.02,   0.02,   571.05,    1010.25, False, [770.64, 925.13])
J1613 = OurGalaxy('J1613+2834',  5.9,    0.4,    11.34,  0.02,   0.01,   1876.04,   2518.87, False, [1046.79, 1708.13])
J1713 = OurGalaxy('J1713+2817',  0.9,    0.7,    0,      0,      0,      414.55,    302.87,  False, [526.67, 861.52])
J2116 = OurGalaxy('J2116-0634',  9.4,    2.7,    11.6,   0.04,   0.05,   0,         0,       False, [835.74, 1401.02])
J2118 = OurGalaxy('J2118+0017',  4.02,   0.34,   0,      0,      0,      0,         0,       False, [np.nan, np.nan])
J2140 = OurGalaxy('J2140+1209',  4.2,    2,      11.12,  0.05,   0.05,   282.11,    584.13,  True, [262.35, 597.32])




# Organizing our data
ourgals = [J0826, J0901, J0905, J0944, J1107, J1125, J1219, J1232, J1341,
           J1450, J1506, J1558, J1613, J1713, J2116, J2118, J2140]
ourgalnames = [x.name for x in ourgals]
ourmass = [x.logmass for x in ourgals]
ourmasserr = [[x.mass_lowunc for x in ourgals], [x.mass_upunc for x in ourgals]]
ourV50 = np.array([x.v50 for x in ourgals])
ourV98 = np.array([x.v98 for x in ourgals])
oursfr = np.array([x.sfr for x in ourgals])
oursfrunc = np.array([x.sfr_u for x in ourgals])
strong_MgII_abs = np.array([x.strong_MgII_abs for x in ourgals])
bradna_Cmask = [True if x in ourgalnames else False for x in ShortNames]
strong_MgII_abs = np.array([x.strong_MgII_abs for x in ourgals])

# Data from Tremonti Table
TremontiGalaxies = np.array([[ShortNames[i], ChristyMass[i], ChristySFR[i], ChristyV50[i], ChristyV98[i]]
                             for i in range(0, len(ShortNames)) if ShortNames[i] in ourgalnames])
mass_T = [float(x[1]) for x in TremontiGalaxies]
HiresV98 = [ChristyV98[i] for i in range(0, len(ChristyV98)) if ShortNames[i] in ourgalnames]
HiresAge = [ChristyAge[i] for i in range(0, len(ChristyAge)) if ShortNames[i] in ourgalnames]

# Data from MaGE and MMT
mmtmage_v50 = np.array([x.MTTMaGEVels[0] for x in ourgals])
mmtmage_v98 = np.array([x.MTTMaGEVels[1] for x in ourgals])


# Getting uncertainty for Tremonti SFR as 0.2 dex
TremSFR = 10**ChristySFR  # since ChristySFR is log(SFR)
tlsfr = 10**(ChristySFR-0.2)
thsfr = 10**(ChristySFR+0.2)
TremUpperSFRUnc = thsfr - TremSFR
TremLowerSFRUnc = TremSFR - tlsfr
# Propagating uncertainty for ratios
TremSFR_u = np.array([ufloat(ChristySFR[x], 0.2) for x in range(0, len(ChristySFR))])
oursfr_u = np.array([ufloat(oursfr[x], oursfrunc[x]) for x in range(0, len(oursfr))])
SFR_ratio = (10**TremSFR_u[bradna_Cmask])/oursfr_u
SFR_ratio_n = np.array([x.n for x in SFR_ratio])
SFR_ratio_s = np.array([x.s for x in SFR_ratio])




# The galaxies for which mass is 0 above have no mass calculated by prospector
# The following statement fills in those blanks with mass from the Tremonti table
for i in range(0, len(ourmass)):
    if ourmass[i] == 0:
        ourmass[i] = mass_T[i]



# Getting the flux #######

# function to return a flux in maggies given an AB magnitude
def flux(mag):
    flux = 8.2839 * 1e-23 * 10. ** (mag / (-2.5))
    return flux

# Function to get luminosity (taken from cb galaxy fits sfr analysis tools)
# But we need vSv. WHat's v?

def get_fv(LV,Z):

    lum_dis = (cosmo.luminosity_distance(umeh_Z_T))*(1/u.Mpc)*(prsc*10**6)*(10**6)
    luminosity = (LV)*4*np.pi*(lum_dis**2)

    return luminosity

umeh_w4flux = flux(umeh_w4mag)

# Get frequencies for each galaxy
freq = ((lightspeed*(10**6))/22.194)*(1+umeh_Z_T)

# Get vobs fobs
vf = get_fv(umeh_w4flux*freq, umeh_Z_T)

#UmehMask
ChristyUmehMask = [True if i in umeh_shortnames else False for i in ShortNames]
ChrstUmehSFR = ChristySFR[ChristyUmehMask]
##### Got Flux and ARrays to Plot ##########

# ---------------- Getting the attenuation
def attenuate(current_ratio):
    if current_ratio > 0:
        A_hbeta = (-2.5 / (4.60 - 5.12)) * umath.log10(0.469 / current_ratio) * 4.60
    if current_ratio <= 0:
        A_hbeta = ufloat(0, 0)

    return A_hbeta
A_hbeta = np.array([attenuate(r) for r in rat_unc])
hb_correction = 10**(A_hbeta/2.5)
sorted_hb_corr = hb_correction[ratio_indxs]
sort_hb_corr_n = np.array([x.n for x in sorted_hb_corr])
sort_hb_corr_s = np.array([x.s for x in sorted_hb_corr])

# Adding an additional 0.1 dex calibration error to our Hb sfr
logoursfr = np.log10(oursfr)
blsfr = 10**(logoursfr-0.1)
bhsfr = 10**(logoursfr+0.1)
BradUpperSFRUnc = bhsfr - oursfr
BradLowerSFRUnc = oursfr - blsfr


# ------------------------------- Plotting...
plt.close('all')

# fig = plt.figure(figsize=(12, 9))
fig = plt.figure(1)
plt.tight_layout()
def figure1():
    # ----------------------------- PLOT 1
    # Plotting Mass Tremonti vs Mass Pospector

    ax = fig.add_subplot(2, 3, 1)

    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    ax.set_ylim(10.4, 11.4)
    ax.set_xlim(10.4, 11.4)

    ax.set_xlabel("Mass Prosp")
    ax.set_ylabel("Mass Tremonti")

    # Use these instead once we get all mass values
    # plt.ylim(np.amin([x.logmass for x in ourgals]+[x.logmass_T for x in ourgals])-0.3,
    #          np.amin([x.logmass for x in ourgals]+[x.logmass_T for x in ourgals])+0.3)
    # plt.xlim(np.amin([x.logmass for x in ourgals]+[x.logmass_T for x in ourgals])-0.3,
    #          np.amin([x.logmass for x in ourgals]+[x.logmass_T for x in ourgals])+0.3)

    # plot y=x line
    ax.plot(np.linspace(9, 12, 16), np.linspace(9, 12, 16), "--", lw=0.5, color="black", alpha=0.3)
    ax.scatter(ourmass, mass_T)
    ax.errorbar(ourmass, mass_T, xerr=ourmasserr, ls='none')

    # ------------------------------- PLOT 2
    # Plotting Stellar Age vs VMAX from Tremonti Data

    for i in range(0, len(ourgals)):
        ax.annotate(ourgals[i].name, (ourmass[i]-0.02, mass_T[i]+0.02))

    ax2 = fig.add_subplot(2, 3, 2)
    ax2.set_ylabel("VMax Tremonti")
    ax2.set_xlabel("Stellar Age Tremonti")

    ax2.scatter(ChristyAge, ChristyV98, c='blue')
    ax2.scatter(HiresAge, HiresV98, c='red')
    for i in range(0, len(ourgals)):
        if ShortNames[i] in ourgalnames:
            ax2.annotate(ourgals[i].name, (HiresAge[i]+0.02, HiresV98[i]-0.02))

    # ------------------------------- PLOT 3 SFR vs nu_f
    # plotting LV vs SFR
    ax3 = fig.add_subplot(2, 3, 3)
    ax3.scatter(ChrstUmehSFR, np.log10(vf*7.8e-10))
    ax3.set_xlabel(r"Tremonti SFR $log_{10}(\frac{M_{\bigodot}}{year})$")
    ax3.set_ylabel(r"$\nu$ $L_{\nu}$ $log_{10}(\frac{erg}{s})$")

    # ------------------------------- PLOT 4
    # Plotting my velocities versus Christy's

    #Old plot plotting VBradna vs VTremonti
    ax4 = fig.add_subplot(2, 3, 4)
    #ax4.plot(np.linspace(-3100, 0, 100), np.linspace(-3100, 0, 100), "--", lw=0.5, color="black", alpha=0.3)
    v50_zero_mask = (ourV50 != 0)
    v98_zero_mask = (ourV98 != 0)
    # ax4.scatter([(-1)*x for x in ourV50 if x != 0],
    #             [ChristyV50[bradna_Cmask][i] for i in range(0, len(ourV50)) if ourV50[i] != 0], c='skyblue')
    # ax4.scatter([(-1)*x for x in ourV98 if x != 0],
    #             [ChristyV98[bradna_Cmask][i] for i in range(0, len(ourV98)) if ourV98[i] != 0], c='blue')
    ax4.scatter(((-1)*ourV50[v50_zero_mask])-ChristyV50[bradna_Cmask][v50_zero_mask],
                ChristyV50[bradna_Cmask][v50_zero_mask], c='skyblue')
    ax4.scatter(((-1)*ourV98[v98_zero_mask])-ChristyV98[bradna_Cmask][v98_zero_mask],
                ChristyV98[bradna_Cmask][v98_zero_mask], c='blue')



    ax4.set_ylabel("Christy's Velocity " + r"$\frac{km}{s}$")
    ax4.set_xlabel("Bradna Velocity - Tremonti Velocity " + r"($\frac{km}{s}$)")

    # -------------------------------- PLOT 5
    # Plotting SFR Hb versus SFR Tremonti
    ax4 = fig.add_subplot(2, 3, 5)
    ax4.plot(np.linspace(0, 3, 10), np.linspace(0, 3, 10), "--", lw=0.5, color="black", alpha=0.3)
    ax4.scatter(ChristySFR[bradna_Cmask], np.log10(oursfr), s=4, c='skyblue')
    ax4.scatter(ChristySFR[bradna_Cmask][strong_MgII_abs], np.log10(oursfr)[strong_MgII_abs], s=4, c='red')
    ax4.set_xlabel(r"Christy SFR $log_{10}(\frac{M_{\bigodot}}{year})$")
    ax4.set_ylabel(r"Bradna $SFR_{H\beta}$ $log_{10}(\frac{M_{\bigodot}}{year})$")

    # -------------------------------- PLOT 6
    # plt.close('all')
    # # fig = plt.figure(figsize=(12, 9))
    # fig = plt.figure()
    # plt.tight_layout()
    # ax5 = fig.add_subplot(1, 1, 1)

    ax5 = fig.add_subplot(2, 3, 6)
    ax5.scatter(10**ChristySFR[bradna_Cmask], (10**ChristySFR[bradna_Cmask])/oursfr, s=4, c='skyblue')
    ax5.scatter(10**ChristySFR[bradna_Cmask][strong_MgII_abs], ((10**ChristySFR[bradna_Cmask])/oursfr)[strong_MgII_abs],
                s=4, c='red')
    ax5.set_ylabel(r"Tremonti SFR/Bradna SFR")
    ax5.set_xlabel(r"Tremonti $SFR\_IR$ $\frac{M_{\bigodot}}{year}$")
    ax5.set_yscale("log")
    # Customizing Ticks
    ax5.yaxis.set_ticklabels([])
    ax5majors = np.concatenate((np.arange(0, 400, 100), np.array([1, 10])), axis=0)
    ax5majorlabels = [str(x) for x in ax5majors]
    ax5.yaxis.set_major_locator(ticker.FixedLocator(ax5majors))
    ax5.yaxis.set_major_formatter(ticker.FixedFormatter(ax5majorlabels))
    ax5.tick_params(which='major', labelsize=10)


    ax5minors = np.concatenate((np.arange(0, 10, 1), np.arange(20, 100, 10)), axis=0)
    ax5mminorlabels = [str(x) for x in ax5minors]
    ax5.yaxis.set_minor_locator(ticker.FixedLocator(ax5minors))
    ax5.yaxis.set_minor_formatter(ticker.FixedFormatter(ax5mminorlabels))
    ax5.tick_params(which='minor', color='grey', labelsize=8)

    ax5.grid(b=True, which='major', color='g', linestyle='-', alpha=0.2)
    ax5.grid(b=True, which='minor', color='purple', linestyle='--', alpha=0.2)

def figure2(): # plots AAS figs
    # -------------- Plotting figure Hbeta correction vs SFR ratio for AAS 2019 poster
    aasfig = plt.figure(2)
    plt.tight_layout()

    # ax6 = aasfig.add_subplot(1, 1, 1)
    # ax6.plot(np.linspace(0, 20, 10), np.linspace(0, 20, 10), "--", lw=0.5, color="black", alpha=0.3)
    # ax6.scatter((10**ChristySFR[bradna_Cmask])/oursfr, sort_hb_corr_n)
    # ax6.set_xlabel(r"Tremonti SFR/Bradna SFR")
    # ax6.set_ylabel(r"$10^{A(H\beta)/2.5}$")
    ax6 = aasfig.add_subplot(1, 1, 1)
    ax6.plot(np.linspace(0, 50, 10), np.linspace(0, 50, 10), "--", lw=2, color="black", alpha=0.3)
    #ax6.scatter(SFR_ratio_n, sort_hb_corr_n)
    # Looking at the array "ourgals" and knowing beforhand how to label galaxies, I now define masks to index
    # Galaxies and their explanations
    lowsfr_mask = [2, 3]
    escapingrad_mask = [11, 12]
    dustatt_mask = [1, 8]
    allmasks = [1, 2, 3, 8, 11, 12]
    ax6.scatter(SFR_ratio_n[lowsfr_mask], sort_hb_corr_n[lowsfr_mask], c='r', label='recently quenched SFR?', marker="x")
    ax6.scatter(SFR_ratio_n[escapingrad_mask], sort_hb_corr_n[escapingrad_mask], c='g',
                label='diluted shells = escaping ionizing photons?', marker="P")
    ax6.scatter(SFR_ratio_n[dustatt_mask], sort_hb_corr_n[dustatt_mask], c='m',
                label='explained by dust attenuation', marker="^")
    remaining_SFR_ratio_n = np.delete(SFR_ratio_n, allmasks)
    remaining_sort_hb_corr_n = np.delete(sort_hb_corr_n, allmasks)
    ax6.scatter(remaining_SFR_ratio_n, remaining_sort_hb_corr_n)
    ax6.errorbar(SFR_ratio_n, sort_hb_corr_n, xerr=SFR_ratio_s, yerr=sort_hb_corr_s, ls='none', lw=0.5)

    ax6.loglog()
    for axis in [ax6.xaxis, ax6.yaxis]:
        axis.set_major_formatter(ScalarFormatter())
    ax6.set_xlabel(r"SFR(IR) / SFR(H$\beta$)", fontsize=18)
    ax6.set_ylim([1, 50])
    ax6.set_xlim([1, 50])
    ax6.set_ylabel(r"H$\beta$ correction $=10^{A(H\beta)/2.5}$", fontsize=18)
    ax6.legend()

    # -------------- Plotting figure SFR_Hbeta vs SFR_IR for AAS 2019 poster
    aasfig2 = plt.figure(3)
    plt.tight_layout()

    ax7 = aasfig2.add_subplot(1, 1, 1)
    ax7.plot(np.linspace(0, 500, 100), np.linspace(0, 500, 100), "--", lw=1.5, color="black", alpha=0.3)
    ax7.scatter(10**ChristySFR[bradna_Cmask], oursfr, s=15)
    ax7.errorbar(10**ChristySFR[bradna_Cmask], oursfr, xerr=[TremLowerSFRUnc[bradna_Cmask], TremUpperSFRUnc[bradna_Cmask]],
                 yerr=[(oursfrunc + BradLowerSFRUnc), (oursfrunc + BradUpperSFRUnc)], ls='none', lw=0.5)
    #ax7.scatter(ChristySFR[bradna_Cmask][strong_MgII_abs], np.log10(oursfr)[strong_MgII_abs], s=4, c='red')
    ax7.loglog()
    for axis in [ax7.xaxis, ax7.yaxis]:
        axis.set_major_formatter(ScalarFormatter())
    ax7.set_ylim([1, 200])
    ax7.set_xlim([1, 600])
    ax7.set_xlabel(r"SFR(IR)", fontsize=18)
    ax7.set_ylabel(r"$SFR(H\beta)$, no dust correction", fontsize=18)

def figure3(): #figures related to thesis
    # --------------- Plots for after AAS; mostly related to thesis
    thesis_sheet = plt.figure(4)
    ax8 = thesis_sheet.add_subplot(1, 1, 1)
    ax8.plot(np.linspace(0, 200, 10), np.linspace(0, 200, 10), "--", lw=2, color="black", alpha=0.3)
    #ax6.scatter(SFR_ratio_n, sort_hb_corr_n)
    # Looking at the array "ourgals" and knowing beforhand how to label galaxies, I now define masks to index
    # Galaxies and their explanations
    lowsfr_mask = [2, 3]
    escapingrad_mask = [11, 12]
    dustatt_mask = [1, 8]
    allmasks = [1, 2, 3, 8, 11, 12]
    ax8.scatter(SFR_ratio_n[lowsfr_mask], sort_hb_corr_n[lowsfr_mask], c='r', label='recently quenched SFR?', marker="x")
    ax8.scatter(SFR_ratio_n[escapingrad_mask], sort_hb_corr_n[escapingrad_mask], c='g',
                label='diluted shells = escaping ionizing photons?', marker="P")
    ax8.scatter(SFR_ratio_n[dustatt_mask], sort_hb_corr_n[dustatt_mask], c='m',
                label='explained by dust attenuation', marker="^")
    remaining_SFR_ratio_n = np.delete(SFR_ratio_n, allmasks)
    remaining_sort_hb_corr_n = np.delete(sort_hb_corr_n, allmasks)
    ax8.scatter(remaining_SFR_ratio_n, remaining_sort_hb_corr_n)
    ax8.errorbar(SFR_ratio_n, sort_hb_corr_n, xerr=SFR_ratio_s, yerr=sort_hb_corr_s, ls='none', lw=0.5)
    for i in range(0, len(ourgals)):
        ax8.annotate(ourgals[i].name, (SFR_ratio_n[i], sort_hb_corr_n[i]), fontsize=6, rotation=45)
    ax8.loglog()
    for axis in [ax8.xaxis, ax8.yaxis]:
        axis.set_major_formatter(ScalarFormatter())
    ax8.set_xlabel(r"SFR(IR) / SFR(H$\beta$)", fontsize=18)
    # ax8.set_ylim([1, 50])
    # ax8.set_xlim([1, 50])
    ax8.set_ylabel(r"H$\beta$ correction $=10^{A(H\beta)/2.5}$", fontsize=18)
    ax8.legend()

    thesis_sheet2 = plt.figure(4)
    # Plotting my HIRES velocities versus Christy's

    ax9 = fig.add_subplot(2, 2, 1)
    #ax9.plot(np.linspace(-3100, 0, 100), np.linspace(-3100, 0, 100), "--", lw=0.5, color="black", alpha=0.3)
    v50_zero_mask = (ourV50 != 0)
    v98_zero_mask = (ourV98 != 0)
    ax9.scatter(((-1)*ourV50[v50_zero_mask])-ChristyV50[bradna_Cmask][v50_zero_mask],
                ChristyV50[bradna_Cmask][v50_zero_mask], c='skyblue')
    ax9.scatter(((-1)*ourV98[v98_zero_mask])-ChristyV98[bradna_Cmask][v98_zero_mask],
                ChristyV98[bradna_Cmask][v98_zero_mask], c='blue')

    ax9.set_xlabel("HIRES Velocity - Tremonti Velocity " + r"($\frac{km}{s}$)")
    ax9.set_ylabel("Christy's Velocity " + r"$\frac{km}{s}$")

    # Plotting my MMT MaGE velocities versus Christy's

    ax10 = fig.add_subplot(2, 2, 2)
    #ax10.plot(np.linspace(-3100, 0, 100), np.linspace(-3100, 0, 100), "--", lw=0.5, color="black", alpha=0.3)
    v50_zero_mask = (mmtmage_v50 != np.nan)
    v98_zero_mask = (mmtmage_v98 != np.nan)
    ax10.scatter(((-1)*mmtmage_v50[v50_zero_mask])-ChristyV50[bradna_Cmask][v50_zero_mask],
                ChristyV50[bradna_Cmask][v50_zero_mask], c='skyblue')
    ax10.scatter(((-1)*mmtmage_v98[v98_zero_mask])-ChristyV98[bradna_Cmask][v98_zero_mask],
                ChristyV98[bradna_Cmask][v98_zero_mask], c='blue')

    ax10.set_xlabel("MMT/MaGE Velocity - Tremonti Velocity " + r"($\frac{km}{s}$)")
    ax10.set_ylabel("Christy's Velocity " + r"$\frac{km}{s}$")

    ax11 = fig.add_subplot(2, 2, 3)
    v50_zero_mask = (ourV50 != 0)
    v98_zero_mask = (ourV98 != 0)
    print((-1)*ourV50[v50_zero_mask])
    ax11.plot(np.linspace(-3100, 0, 100), np.linspace(-3100, 0, 100), "--", lw=0.5, color="black", alpha=0.3)
    ax11.scatter((-1)*ourV50[v50_zero_mask], (-1)*mmtmage_v50[v50_zero_mask], c='skyblue')
    ax11.scatter((-1)*ourV98[v98_zero_mask], (-1)*mmtmage_v98[v98_zero_mask], c='blue')
    ax11.set_xlabel("HIRES Vels")
    ax11.set_ylabel("MaGE and MMT Vels")







#figure1()
#figure1()
figure3()

#plt.savefig("comparison.png", bbox_inches="tight", dpi=1800)
plt.show(block=False)



