import numpy as np
import matplotlib.pyplot as plt
# import ROOT
import os
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

#######################################################################################################################
#######################################################################################################################
###################                  Parametres a changer :                         ###################################
#######################################################################################################################
#######################################################################################################################


### Calibration :

# Remplir la liste par les données mesurées à l'oscilloscope (pour les tensions 70,75,80,85,90,95,100,105,110)
calibration_reel = [34.1,40.8,47.7,51.0,54.4,57.8,61.1,64.6,67.9,71.1,74.6] #mV
# Remplir la liste par les erreurs sur les mesures à l'oscilloscope pour les données précédentes
calibration_erreur = [19,20,17,16,18,21,18,20,19,20,21] #uV
# Rentrer l'adresse du fichier de calib et son nom (Pour Windows : mettre "\\" pour "\"
adresse_fichier_calib = "C:\\Users\\molle\\Documents\\LPSC_data\\spectro_230522\\"
nom_fichier_calib = "alphaCCE_20220523_SamGimliTyrion_calib.txt"

### Spectroscopie

# Rentrer l'adresse du fichier de spectro et son nom
adresse_fichier_spectro = "C:\\Users\\molle\\Documents\\LPSC_data\\spectro_230522\\"
nom_fichier_spectro = "spectro_230522_Sam_263V.txt"
# Rentrer le nom du diamant
nom_diamant = 'Sam'
# Rentrer la date
date = "23/05/22"

#######################################################################################################################
#######################################################################################################################
###################                  Programme :                                    ###################################
#######################################################################################################################
#######################################################################################################################

energie_reelle = np.array(calibration_reel)*10**-3 * 10**-12 * 13.6/(1.6*10**-19)
# 10**13 pour mV en V ; 10**-12 pour la capa du préampli de charge ; 13.6 pour l'énergie spécifique d'ionisation
erreur_energie = np.array(calibration_erreur)**10**-6 * 10**-12  * 13.6/(1.6*10**-19)

os.chdir(adresse_fichier_calib)
data_spectro =np.loadtxt(nom_fichier_calib,delimiter=',')

# fonction pour le fit de la calib
def gauss_function(x,a,x0,sigma):
    return(a*np.exp(-(x-x0)**2/(2*sigma**2)))

indices, _ = find_peaks(data_spectro,height=100,distance = 100)

mean_pic = []
sigma_pic = []

for pics in range(len(indices)):
    data_fit=[]
    zone_fit = []
    for plage in range(1000):
        data_fit.append(data_spectro[indices[pics]-500+plage])
        zone_fit.append(indices[pics]-500+plage)
    popt, pcov = curve_fit(gauss_function,zone_fit,data_fit,p0=[120,indices[pics],500])
    mean_pic.append(popt[1])
    sigma_pic.append(popt[2])


fit_calib = np.polyfit(mean_pic,energie_reelle,1)
### si besoin de vérifier la calibration, décommenter les lignes suivantes
# plt.figure()
# plt.errorbar(x=mean_pic,y=np.array(mean_pic)*fit_calib[0]+fit_calib[1],xerr=sigma_pic,yerr=np.array(sigma_pic)*fit_calib[0]+fit_calib[1])
# plt.legend()
# plt.title("Calibration Energie bins")
# plt.xlabel("Bins")
# plt.ylabel("Energie en eV")


polarisation_sam = [-430,-400,-300,-200,-150,-100,-50,0,50,100,150,200,263,300,400,500]
fichier_data = ["spectro_250522_Sam_m430V.txt","spectro_250522_Sam_m400V.txt","spectro_250522_Sam_m300V.txt","spectro_250522_Sam_m200V.txt","spectro_250522_Sam_m150V.txt","spectro_240522_Sam_m100V.txt",
                "spectro_240522_Sam_m50V.txt","0","spectro_240522_Sam_50V.txt","spectro_240522_Sam_100V.txt","spectro_240522_Sam_150V.txt","spectro_240522_Sam_200V.txt","spectro_230522_Sam_263V.txt",
                "spectro_240522_Sam_300V.txt","spectro_240522_Sam_400V.txt","spectro_240522_Sam_500V.txt"]
means_fichier = []
erreur_fichier = []
xbin = 2**8
for file in fichier_data:
    if(file=="0"):
        means_fichier.append(0)
        erreur_fichier.append(0)
    else:
        data_spectro = np.loadtxt(file, delimiter=',')
        data_spectro_moy = [sum([data_spectro[i*xbin+j] for j in range(int(xbin))]) for i in range(int(65536./xbin))]
        indices, _ = find_peaks(data_spectro_moy, height=100, distance=1000)
        popt, pcov = curve_fit(gauss_function,[ i  for i in range(int(65536./xbin)) ] , data_spectro_moy, p0=[1000, indices[0], 500])
        plt.figure()
        plt.plot([(fit_calib[0] * i*xbin + fit_calib[1]) * 10 ** -6 for i in range(int(65536./xbin))],data_spectro_moy)
        plt.plot([(fit_calib[0] * i*xbin + fit_calib[1]) * 10 ** -6 for i in range(int(65536./xbin))],gauss_function( [i for i in range(int(65536./xbin))],*popt))
        plt.title(file)
        means_fichier.append((fit_calib[0] * popt[1]*xbin + fit_calib[1]) * 10 ** -6)
        erreur_fichier.append((abs(fit_calib[0] * popt[2]*xbin + fit_calib[1]) * 10 ** -6))
plt.figure()
plt.errorbar(x=np.array(polarisation_sam)/540.,y=np.array(means_fichier)/5.470 ,yerr=erreur_fichier, label="CCE")
plt.title("Collecte de charge " + "Sam" + " " + date)
plt.xlabel("Champ electrique (V/um)")
plt.ylabel("CCE")
plt.errorbar(x=[-1,1],y=[1,1],linestyle='dotted',color="red",label="100% CCE")
plt.legend()



plt.show()