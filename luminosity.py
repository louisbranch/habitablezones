import numpy as np
from astropy.constants import sigma_sb, R_sun, L_sun

def luminosity_vs_radius(R, T_eff_constant=5778):
    L = 4 * np.pi * (R_sun.value*R)**2 * sigma_sb.value * T_eff_constant**4
    return np.log10(L/L_sun.value)

def luminosity_vs_teff(T_eff, R_constant=R_sun.value):
    L = 4 * np.pi * R_constant**2 * sigma_sb.value * T_eff**4
    return np.log10(L/L_sun.value)
