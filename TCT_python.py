"""
Script d'analyse de TCT - Full Python
Date de création : 18/01/2023
Date de modification : 18/01/2023
Créateur : Robin Molle
"""

import numpy as np
import os
import glob
from scipy.optimize import curve_fit
from mpmath import gamma
import matplotlib.pyplot as plt
import warnings
import sys
import readTrc as rT
from scipy.optimize import OptimizeWarning
warnings.simplefilter("error", OptimizeWarning)
warnings.filterwarnings("error")


#time, amplitude, metadata = rT.readTrc(filename + str(waveform) + '.trc')



