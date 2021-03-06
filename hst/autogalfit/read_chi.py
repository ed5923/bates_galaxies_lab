# Aleks Diamond-Stanic, February 7, 2019
# goal: read information from galfit output files to construct chi-squared contours in terms of re and magnitude
import sys
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

dir = sys.argv[1]
gal = sys.argv[2]
band = sys.argv[3]
files = glob.glob(dir+'/'+gal+'_'+band+'*.band')
print(files)
chi = np.zeros(len(files))
mag = np.zeros(len(files))
sizepix = np.zeros(len(files))

mag
for i in range(0, len(files)):
    print(files[i])
    with open(files[i]) as f:
        content = f.readlines()
        chi[i] = np.float(content[3][14:19])
        mag[i] = np.float(content[47][4:13])
        sizepix[i] = np.float(content[48][4:13])
        print(chi[i], mag[i], sizepix[i])

mag_1d = np.unique(mag)
sizepix_1d = np.unique(sizepix)
chi_2d = np.zeros([len(mag_1d), len(sizepix_1d)])
#count = 0
for i in range(0, len(mag_1d)):
    for j in range(0, len(sizepix_1d)):
        test = np.where((mag == mag_1d[i]) & (sizepix == sizepix_1d[j]))
        print(mag[test], sizepix[test], chi[test])
        chi_2d[j,i] = chi[test[0]]
        #print(mag[count], mag_1d[i])
        #print(sizepix[count], sizepix_1d[j]) 
        #count = count+1
        
        
        
name = 'chi_values_'+gal+'_'+band+'.pdf'

with PdfPages(name) as pdf:   
    fig = plt.figure()

    plt.scatter(mag, sizepix, marker='o', color='orange')
    plt.yscale('log')
    plt.ylim([0.1, 3.])
    plt.ylabel('Half-Light radius in pixels')
    plt.xlabel('Magnitude')
    plt.title(dir+'/'+gal+'_'+band)

    for i in range(0, len(files)):
        plt.text(mag[i], sizepix[i], str(chi[i]), fontsize=5)

    pdf.savefig()
    plt.close()

    fig = plt.figure()

    plt.contourf(mag_1d, sizepix_1d, chi_2d, 20, cmap='RdGy')
    #plt.clim(0,20)
    plt.colorbar()
    
    plt.ylabel('Half-Light radius in pixels')
    plt.xlabel('Magnitude')
    pdf.savefig()
    plt.close()

    fig = plt.figure()

    #plt.contour(mag_1d, sizepix_1d, chi_2d)

    chi_min = np.min(chi_2d)
    #levels = np.array([chi_min, chi_min+1, chi_min+2.71, chi_min+4.00, chi_min+6.63, chi_min+9.00])##np.arange(10)/2 + chi_min. these level correspond with the 68, 95.4, 99.73, value in 1 as stated by the paper labelled confidence limits on estimated model parameters. 
    levels = np.array([1.0, 4.00, 9.00])+chi_min
    cs = plt.contour(mag_1d, sizepix_1d, chi_2d, levels, colors=['blue', 'green', 'red'])
    plt.clabel(cs, inline=1, fontsize=14)
    plt.ylim([0, 2])
    plt.ylabel('Half-Light radius in pixels', fontsize=14)
    plt.xlabel('Magnitude', fontsize=14)
    labels = ['68%', '95%', '99.7%']
    #labels = ['68%', '90%','95%','99%','99.7%']
    for i in range(len(labels)):
        cs.collections[i].set_label(labels[i])

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
    print(np.min(y)*0.025, np.max(y)*0.025)
    #plt.axvline(x=np.min(x), color='black')
    #plt.axvline(x=np.max(x), color='black')
    #plt.axhline(y=np.min(y), color='black')
    #plt.axhline(y=np.max(y), color='black')
    plt.legend(loc='upper right', prop={'size': 15})
    
    pdf.savefig()
    plt.close()
    
os.system('open %s &' % name)
    
