# Purpose: Is to determine the chi values from a subimage of the
# images given. We do this by taking the subimage of a galaxy
# starting at the center and moving out
#
# run simultaneous_chi_magir.py 20190703-1345_sersic_coarse_simultaneous_100_psfcoarse J0826 F814W
#
import sys
import os
import glob
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from photutils import CircularAperture
from photutils import aperture_photometry

dir = sys.argv[1]
gal = sys.argv[2]
band = sys.argv[3]
fits_files = glob.glob(dir+'/'+gal+'*'+band+'*output.fits')
band_files = glob.glob(dir+'/'+gal+'*'+band+'*band')
subimages_chivalues = open('Chivalues_of_subimages.dat', 'a+')
subimages_chivalues.write("Subimages_chi_values\n")
mag1 = np.zeros(len(band_files))
mag2 = np.zeros(len(band_files))
chi_from_our_calculations = np.zeros(len(band_files))
chi_one_our_calculations = np.zeros(len(band_files))

#xcen = 100
xcen = 50
ycen = xcen
dx = 5 
#dx = 5
dy = dx

for i in range(0, len(fits_files)):
    print(fits_files[i], band_files[i])
    hdu = fits.open(fits_files[i])
    data, header = hdu[0].data, hdu[0].header
    with open(band_files[i]) as f:
        content = f.readlines()
        
        v_unc, v_unc_head = hdu[8].data, hdu[8].header
        v_res, v_res_head = hdu[4].data, hdu[4].header

        v_unc_image_stamp = v_unc[(ycen-dy):(ycen+dy), (xcen-dx):(xcen+dx)]
        v_res_image_stamp = v_res[(ycen-dy):(ycen+dy), (xcen-dx):(xcen+dx)]

        j_unc, j_unc_head = hdu[9].data, hdu[9].header
        j_res, j_res_head = hdu[5].data, hdu[5].header

        j_unc_image_stamp = j_unc[(ycen-dy):(ycen+dy), (xcen-dx):(xcen+dx)]
        j_res_image_stamp = j_res[(ycen-dy):(ycen+dy), (xcen-dx):(xcen+dx)]
        
        #print(res_image_stamp)
        #print(unc_image_stamp)
        #chi_from_our_calculations_for_v[i] = np.sum((res_image_stamp/unc_image_stamp)**2)/((101**2)*3)
        #chi_from_our_calculations_for_u[i] = np.sum((res_image_stamp/unc_image_stamp)**2)/((101**2)*3)
        chi_from_our_calculations[i] = (np.sum((j_res_image_stamp/j_unc_image_stamp)**2)+np.sum((v_res_image_stamp/v_unc_image_stamp)**2))/(((len(v_res_image_stamp)**2+len(j_res_image_stamp)**2))*1)

        chi_one_our_calculations[i] = np.sum((v_res_image_stamp/v_unc_image_stamp)**2)/(((len(v_res_image_stamp))**2)*1)
        
        #print(content[47])
        #mag[i] = np.float(content[47][4:13])
        mag1[i] = np.float(content[47][4:10])
        #mag2[i] = np.float(content[48][4:13])
        mag2[i] = np.float(content[47][11:18])
        #print(chi_from_our_calculations[i])
        #print(chi_from_our_calculations_for_u[i])

mag1_1d = np.unique(mag1)
mag2_1d = np.unique(mag2)
chi_2d = np.zeros([len(mag1_1d), len(mag2_1d)])
chi_one = np.zeros([len(mag1_1d), len(mag2_1d)])
for i in range(0,len(mag1_1d)):
    for j in range(0, len(mag2_1d)):
        test = np.where((mag1 == mag1_1d[i]) & (mag2 == mag2_1d[j]))
        print(mag1[test], mag2[test], chi_from_our_calculations[test])
        chi_2d[i,j] = chi_from_our_calculations[test[0][0]]
        chi_one[i,j] = chi_one_our_calculations[test[0][0]]

name = 'chi_values_'+gal+'_magir_'+band+'.pdf'

with PdfPages(name) as pdf:
    fig = plt.figure()

    plt.scatter(mag1, mag2, marker='o', color='orange')
    #plt.yscale('log')
    #plt.ylim([0.1, 3.])
    plt.xlabel('mag1: F814W')
    plt.ylabel('mag2: F160W')
    plt.title(dir+'/'+gal+'_'+band)

    for i in range(0, len(band_files)):
        plt.text(mag1[i], mag2[i], str(chi_from_our_calculations[i]), fontsize=5)

    pdf.savefig()
    plt.close()

    print('info from chi_2d')
    fig = plt.figure()
    print(mag1_1d, mag2_1d, chi_2d)
    plt.contourf(mag2_1d, mag1_1d, chi_2d, 20, cmap='RdGy')
    plt.colorbar()

    plt.xlabel('mag2: F160W')
    plt.ylabel('mag1: F814W')
    pdf.savefig()
    plt.close()

    fig = plt.figure()

    chi_min = np.min(chi_2d)
    #levels = np.array([1.0, 4.00, 9.00])+chi_min
    levels = np.array([2.3, 4.61, 9.21])*4.+chi_min
    cs = plt.contour(mag2_1d, mag1_1d, chi_2d, levels, colors=['blue', 'green', 'red'])
    #plt.clabel(cs, inline=1, fontsize=14)
    #plt.xlim([0,np.max(mag2)*0.5])
    #plt.ylim([0, 2])
    plt.xlabel('mag2: F160W', fontsize=14)
    plt.ylabel('mag1: F814W', fontsize=14)
    labels = ['68%', '90%', '99%']
    #for i in range(len(labels)):
    #    cs.collections[i].set_label(labels[i])

    pzero = cs.collections[0].get_paths()[0]
    vzero = pzero.vertices
    xzero = vzero[:,0]
    yzero = vzero[:,1]

    if (len(cs.collections[0].get_paths()) > 1):
        pone = cs.collections[0].get_paths()[1]
        vone = pone.vertices
        xone = vone[:,0]
        yone = vone[:,1]

        x = np.append(xzero, xone)
        y = np.append(yzero, yone)
    else:
        x = xzero
        y = yzero
    print(x,y)
    print(np.min(x), np.max(x))
    print((np.min(x) + np.max(x))/2, (np.max(x) - np.min(x))/2)
    print(np.min(y), np.max(y))
    print((np.min(y) + np.max(y))/2, (np.max(y) - np.min(y))/2)
    print(np.min(x)*0.025, np.max(x)*0.025)
    plt.legend(loc='upper right', prop={'size': 15})

    pdf.savefig()
    plt.close()

    print('info from chi_one')
    fig = plt.figure()
    print(mag1_1d, mag2_1d, chi_one)
    plt.contourf(mag2_1d, mag1_1d, chi_one, 20, cmap='RdGy')
    plt.colorbar()

    plt.xlabel('mag1: F814W')
    plt.ylabel('mag2: F160W')
    pdf.savefig()
    plt.close()

    fig = plt.figure()

    chi_min = np.min(chi_one)
    #levels = np.array([1.0, 4.00, 9.00])+chi_min
    levels = np.array([2.3, 4.61, 9.21])+chi_min
    cs = plt.contour(mag2_1d, mag1_1d, chi_one, levels, colors=['blue', 'green', 'red'])
    #plt.clabel(cs, inline=1, fontsize=14)
    #plt.xlim([0,np.max(mag2)*0.5])
    #plt.ylim([0, 2])
    plt.xlabel('mag2: F160W', fontsize=14)
    plt.ylabel('mag1: F814W', fontsize=14)
    labels = ['68%', '90%', '99%']
    #for i in range(len(labels)):
    #    cs.collections[i].set_label(labels[i])

    pzero = cs.collections[0].get_paths()[0]
    vzero = pzero.vertices
    xzero = vzero[:,0]
    yzero = vzero[:,1]

    if (len(cs.collections[0].get_paths()) > 1):
        pone = cs.collections[0].get_paths()[1]
        vone = pone.vertices
        xone = vone[:,0]
        yone = vone[:,1]

        x = np.append(xzero, xone)
        y = np.append(yzero, yone)
    else:
        x = xzero
        y = yzero
    print(x,y)
    print(np.min(x), np.max(x))
    print((np.min(x) + np.max(x))/2, (np.max(x) - np.min(x))/2)
    print(np.min(y), np.max(y))
    print((np.min(y) + np.max(y))/2, (np.max(y) - np.min(y))/2)
    print(np.min(x)*0.025, np.max(x)*0.025)
    plt.legend(loc='upper right', prop={'size': 15})

    pdf.savefig()
    plt.close()

    
os.system('open %s &' % name)

