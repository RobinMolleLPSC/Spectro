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


adresse_fichier_courant_de_fuite = "Y:\\diamant\\Mesures diamants\\Diamant arrivage 2022\\ALMAX\\Grincheux\\Courant de fuite\\"
nom_fichier_courant_de_fuite = "LeakCurr_20230117_Grincheux_Al_GLOBAL.txt"
# nom_fichier_courant_de_fuite2 = "LeakCurr_20221026_Sam_Al_GLOBAL.txt"

#######################################################################################################################
#######################################################################################################################
###################                         Programme :                                    ############################
#######################################################################################################################
#######################################################################################################################


os.chdir(adresse_fichier_courant_de_fuite)
Polarisation = []
Courant = []
std_courant = []
with open(nom_fichier_courant_de_fuite, "r") as f :
    data_leakage_current = f.readlines()

    date = data_leakage_current[4][1:11]
    nom_diamant = data_leakage_current[8][21:-2]
    epaisseur = float(data_leakage_current[13][13:-5])

    i=47
    while data_leakage_current[i]!='*' and i<len(data_leakage_current)-1:
        i +=1

    for j in [k+47 for k in range(i-47-1)]:
        sep = 0
        while data_leakage_current[j][sep]!='\t' and sep<13:
            sep+=1
        sep2 = sep+1
        while data_leakage_current[j][sep2]!='\t' and sep2<25:
            sep2+=1
        sep3 = sep2 + 1
        while data_leakage_current[j][sep3] != '\n':
            sep3 += 1
        Polarisation.append(float(data_leakage_current[j][:sep]))
        Courant.append(float(data_leakage_current[j][sep+1:sep2]))
        std_courant.append(float(data_leakage_current[j][sep2+1:sep3]))

    plt.figure()
    plt.errorbar(x = Polarisation,y=Courant,yerr=std_courant,marker='s', mew=0.01)
    titre = 'Leakage Current : ' + nom_diamant + ' - ' + date
    plt.title(titre)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Leakage Current (A)")
    plt.yscale('log')
    plt.xscale('linear')

    titre_fig = 'leakage_current_' + nom_diamant + '_' + date[:2] + date[3:5] + date[6:11] + '_lin_log.png'
    plt.savefig(titre_fig)

    plt.figure()
    plt.errorbar(x=Polarisation, y=Courant, yerr=std_courant,marker='s', mew=0.01)
    titre = 'Leakage Current : ' + nom_diamant + ' - ' + date
    plt.title(titre)
    plt.xlabel("Voltage (V)")
    plt.ylabel("Leakage Current (A)")
    plt.yscale('log')
    plt.xscale('symlog')

    titre_fig = 'leakage_current_'+nom_diamant+'_'+date[:2]+date[3:5]+date[6:11]+'_log_log.png'
    plt.savefig(titre_fig)

# Polarisation2 = []
# Courant2 = []
# std_courant2 = []
# with open(nom_fichier_courant_de_fuite2, "r") as f:
#     data_leakage_current2 = f.readlines()
#
#     date2 = data_leakage_current2[4][1:11]
#     nom_diamant2 = data_leakage_current2[8][21:-2]
#     epaisseur2 = float(data_leakage_current2[13][13:-5])
#
#     i = 47
#     while data_leakage_current2[i] != '*' and i < len(data_leakage_current2) - 1:
#         i += 1
#
#     for j in [k + 47 for k in range(i - 47 - 1)]:
#         sep = 0
#         while data_leakage_current2[j][sep] != '\t' and sep < 13:
#             sep += 1
#         sep2 = sep + 1
#         while data_leakage_current2[j][sep2] != '\t' and sep2 < 25:
#             sep2 += 1
#         sep3 = sep2 + 1
#         while data_leakage_current2[j][sep3] != '\n':
#             sep3 += 1
#         Polarisation2.append(float(data_leakage_current2[j][:sep]))
#         Courant2.append(float(data_leakage_current2[j][sep + 1:sep2]))
#         std_courant2.append(float(data_leakage_current2[j][sep2 + 1:sep3]))
#
# plt.figure()
#
# plt.errorbar(x=Polarisation2,y=Courant2,yerr=std_courant2,label="Before irradiation")
# plt.errorbar(x=Polarisation,y=Courant,yerr=std_courant,label="After irradiation")
# plt.title("Leakage current before and after irradiation : Sam")
# plt.xlabel("Voltage (V)")
# plt.ylabel("Leakage Current (A)")
# plt.yscale('log')
# plt.xscale('linear')
# plt.legend()

# plt.show()

print("End of the program")