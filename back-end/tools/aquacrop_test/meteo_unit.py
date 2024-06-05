# -*- coding: utf-8 -*-
"""
"""
import config

# ==============   CONVERSIONS ===============

def Farenheit_to_celsius(F):
	return((F-32)*5/9)

# --- Vapour pressure: standard unit is kilo Pascal ---
def Vapour_pressure_millibar_to_kPa(e):
	return(0.1*e)
def Vapour_pressure_psi_to_kPa(e):
	return(6.89476*e)
def Vapour_pressure_atm_to_kPa(e):
	return(101.325*e)
def Vapour_pressure_mmHg_to_kPa(e):
	return(0.133322*e)
	
# --- Wind speed: standard unit is meter per second (m/s) -----
def WindSpeed_kmperday_to_ms(vv):
	return(vv/86.4)
def WindSpeed_knot_to_ms(vv): # miles per hour, knot
	return(0.5144*vv)
def WindSpeed_fts_to_ms(vv): # foot per second
	return(0.3048*vv)	
	
# ---Radiation: standard unit is megajoules per square meter per day (MJ/m2.day) ---
def Radiation_wm2_to_Mjm2day(R): # Watt/m2
	if(R==config.meteo_missing):return(config.meteo_missing)
	return(0.0864*R)
def Radiation_Jcm2day_to_Mjm2day(R): #Joule per cm2 per day
	return(0.01*R)
def Radiation_mmday_to_Mjm2day(R): #equivalent evaporation mm/day
	return(2.45*R)
def Radiation_calcm2day_to_Mjm2day(R): # calories per cm2 per day
	return(0.041868*R)

# Evapotranspiration: standard unit is millimeter per day (mm/day) 
def Evapotranspiration_MJm2day_mmday(E): 
	return(0.408*E)
def Evapotranspiration_Wm2day_mmday(E): 
	return(0.408*0.0864*E)  # 0.03526 *E   
def Evapotranspiration_mmday_Wm2day(E): 
	return(28.367*E)