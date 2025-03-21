# -*- coding: utf-8 -*-
"""

Calling:
--------
Calculation of ET0 is doned aither by et0_pm (preferentially) or et0_pm_simple for a full meteo station
Those are normally called by meteo_files.meteo_process_daily()

Description:
-------------
Calculation of Reference Evapotranspiration ET0 with the Penman-Monteith equation.
Code written after ET0 Calculator (Dirk Raes, Reference Manual, version 3.2, sept 2012)
This document basically reflects the description made in Allen et al, 1998, but in a more computational way.

The calculation includes aternative equations in case of missing input data, but Temperature is always needed:
 * ea, Actual Vapor pressure is calculated in different ways
 * rn, Net radiation is also alculated in different ways
 
 *** Note that in this code, unknown value are indicated with -9999.***

Measurements:
-------------

AIR TEMPERATURE:
	T: In traditional and modern automatic weather stations the air temperature is measured inside shelters (Stevenson screens or ventilated radiation shields) 
	placed in line with World Meteorological Organization (WMO) standards at 2 m above the ground.

AIR HUMIDITY:
	RH: Relative humidity is measured directly with hygrometers.The measurement is based on the nature of some material such as hair, which changes its length in response to changes in air humidity, or using a capacitance plate, where the electric capacitance changes with RH.
	EA: Vapour pressure can be measured indirectly with psychrometers which measure the temperature difference between two thermometers, the so-called dry and wet bulb thermometers.
	TDEW: The dewpoint temperature is measured with dewpoint meters. The underlying principle of some types of apparatus is the cooling of the ambient air until dew formation occurs. The
	
RADIATION:
	RS: Solar radiation can be measured with pyranometers, radiometers or solarimeters.
	RN: Net longwave and net shortwave radiation can be measured by recording the difference in output between sensors facing upward and downward.
	n: Where pyranometers are not available, solar radiation is usually estimated from the
	duration of bright sunshine. The actual duration of sunshine, n, is measured with a Campbell- Stokes sunshine recorder.

WIND SPEED:

	UZ: Wind speed is measured with anemometers. The anemometers commonly used in weather stations are composed of cups or propellers which are turned by the force of the wind. By counting the number of revolutions over a given time period, the average wind speed over the measuring period is computed.
	Where no wind data are available within the region, a value of 2 m/s can be used as a temporary estimate. This value is the average over 2 000 weather stations around the globe.


"""
from math import *
# import .config

from .meteo_unit import *


# ========== Atmospheric parameters =============

# Atmospheric pressure (P)
# The atmospheric pressure, P, is the pressure exerted by the weight of the earth's atmosphere
# where P atmospheric pressure [kPa],
#	   z elevation above sea level [m]. 

def Atm_Press(z):
	P=101.3 * pow(((293 -0.0065*z)/293),5.26)
	
	# if config.debug==2 : print("Atm_Press",z,P)
	return(P)
	
#Psychrometric contant (γ) 
#The value of the latent heat varies as a function of temperature. As λ
#varies only slightly over normal temperature ranges a single value of 2.45 MJ kg-1
#is considered in the program. This corresponds with the calculation procedure for the FAO 
#Penman-Monteith equation.
#The fixed value for λ is the latent heat for an air temperature of about 20°C. 
#
# γ psychrometric constant [kPa °C-1],
#P atmospheric pressure [kPa],
#λ latent heat of vaporization, 2.45 [MJ kg -1],
#cp specific heat at constant pressure, 1.013 10-3[MJ kg-1°C-1],
#ε ratio molecular weight of water vapour/dry air = 0.622. 

def psychrometric_const(P):
	lb=2.45
	cp=1.013*0.001
	epsilon=0.622
	gamma=(cp*P)/(epsilon*lb)
	gamma=0.664742*0.001*P
	
	# if config.debug==2 : print("psychrometric_const",P, gamma)
	return(gamma)

# ================ Air temperature  =========

def tmean(Tmean,tmin,tmax):
	if Tmean!=-9999:
		tmean=Tmean
	elif tmin==-9999 or tmax==-9999:
		tmean=-9999 # ET0 cannot be calculated
	else: tmean=(tmax+tmin)/2.

	# if config.debug==2 : print("tmean",Tmean,tmin,tmax)	
	return(tmean)

# =========== AIR HUMIDITY ==================

# Saturation vapour pressure as a function of air temperature
#where e°(T) saturation vapour pressure at the air temperature T [kPa],
#	T air temperature [°C],
#	exp[..] 2.7183 (base of natural logarithm) raised to the power [..].	 
#
# d'après http://cires.colorado.edu/~voemel/vp.html, cette eq est celle de Magnus Tetens
	
def e0t_from_tair(T):
	e0t=0.6108*exp(17.27*T/(T+237.3))
	
	# if config.debug==2 : print("e0t_from_tair",T,e0t)
	return(e0t)

# Mean saturation vapour pressure for a day (es)
# where es saturation vapour pressure [kPa],
#	e°(Tmax) saturation vapour pressure at the mean daily maximum air temperature [kPa],
#	e°(Tmin) saturation vapour pressure at the mean daily minimum air temperature [kPa]. 

def msvp_day(tmin,tmax):
	es=(e0t_from_tair(tmax)+e0t_from_tair(tmin))/2.
	
	# if config.debug==2 : print("msvp_day",tmin,tmax,es)
	return(es)

# Slope of saturation vapour pressure curve (∆) 
# where ∆ slope of saturation vapour pressure curve at air temperature T[kPa °C-1],
#	T air temperature [°C],
#	exp[..] 2.7183 (base of natural logarithm) raised to the power [..]. 

def ssvp(T):
	delta= 4098 * 0.6108 * exp((17.27*T)/(T+237.3)) / pow(237.3+T,2)
	
	# if config.debug==2 : print("ssvp",T,delta)
	return(delta)
	

# Actual vapour pressure (ea) derived from dewpoint temperature
# where ea actual vapour pressure [kPa],
#	Tdew, dew point temperature [°C]. 

def ea_from_tdew(Tdew):
	ea=e0t_from_tair(Tdew)
	
	# if config.debug==2 : print("ea_from_tdew",Tdew,ea)
	return(ea)

# Actual vapour pressure (ea) derived from psychrometric data
#	where ea actual vapour pressure [kPa],
#	e°(Twet) saturation vapour pressure at wet bulb temperature [kPa],
#	γ psychrometric constant of the instrument [kPa °C-1],
#	Tdry-Twet wet bulb depression, with Tdry the dry bulb and Twet the wet bulb temperature [°C]. 

def ea_from_psyconst(apsy,P,Tdry,Twet):
	psy_inst=apsy*P
	ea=e0t_from_tair(twet)-psy_inst*(Tdry-Twet)
	
	# if config.debug==2 : print("ea_from_psyconst",apsy,P,Tdry,Twet,ea)
	return(ea)

#Actual vapour pressure (ea) derived from relative humidity data
#	where ea actual vapour pressure [kPa],
#	e°(Tmin) saturation vapour pressure at daily minimum temperature [kPa],
#	e°(Tmax) saturation vapour pressure at daily maximum temperature [kPa],
#	RHmax maximum relative humidity [%],
#	RHmin minimum relative humidity [%]. 
#	For RHmean, (Smith, 1992).

def ea_from_rhminrhmax(tmin,tmax,rhmin,rhmax):
	ea=(e0t_from_tair(tmin)*rhmax/100. + e0t_from_tair(tmax)*rhmin/100.)/2.
	
	# if config.debug==2 : print("ea_from_rhminrhmax",tmin,tmax,rhmin,rhmax,ea)
	return(ea)

def ea_from_rhmax(tmin,rhmax):
	ea=e0t_from_tair(tmin)*rhmax/100.
	
	# if config.debug==2 : print("ea_from_rhmax",tmin,rhmax,ea)
	return(ea)

def ea_from_rhmean(tmean,rhmean):
	ea=e0t_from_tair(tmean)*rhmean/100.
	
	# if config.debug==2 : print("ea_from_rhmean",tmean,rhmean,ea)
	return(ea)
	
#def ea_calculation(ea,Tmin,Tmax,Tmean,Rhmin,Rhmax,Rhmean,apsy,P,Tdry,Twet):

def ea_calculation(ea,Tdew, Tmin,Tmax,Tmean,Rhmin,Rhmax,Rhmean):
	if ea<=-9999:
		if Tdew>-9999:
			ea=ea_from_tdew(Tdew)
		#elif Tdry!=-9999 and Twet!=-9999:
		#	ea=ea_from_psyconst(apsy,P,Tdry,Twet)
		elif Tmin>-9999 and Tmax>-9999 and Rhmin>-9999 and Rhmax>-9999:
			ea=ea_from_rhminrhmax(Tmin,Tmax,Rhmin,Rhmax)
		elif Tmin>-9999 and Rhmax>-9999:	
			ea=ea_from_rhmean(tmean,Rhmean)
		elif Tmean>-9999 and Rhmean>-9999:	
			ea=ea_from_rhmean(tmean,Rhmean)
		elif Tmin>-9999:
			# Before using Tmin in Eq. 3.7, the number of degrees specified in the Data and ETo menu
			# (Missing air humidity in the Input data description sheet) will be subtracted from Tmin. 
			const_adj=0 
			ea=ea_from_tdew(Tmin-const_adj)
		else:
			ea=-9999
	return(ea)

# ============= RADIATION ==========================

#Extraterrestrial radiation (Ra)
#The extraterrestrial radiation, Ra, for each day of the year and for different latitudes is
#estimated from the solar constant, the solar declination and the time of the year
#
#	where Ra extraterrestrial radiation [MJ m-2day-1],
#	Gsc solar constant = 0.0820 MJ m-2 min-1,
#	dr inverse relative distance Earth-Sun (Equation 3.16),
#	ωs sunset hour angle (Equation 3.18) [rad],
#	φ latitude [rad] (Equation 3.15),
#	δ solar declination (Equation 3.17) [rad]. 

def Extraterrestrial_radiation(lat,jday):
	lat_rad=lat*pi/180.
	dr=1 + 0.033 * cos(2*pi/365*jday)
	soldecl=0.409*sin((2*pi/365*jday) - 1.39)
	sunset_angle=acos(-tan(lat_rad)*tan(soldecl))
	   
	ra= (24*60/pi)* 0.082 * dr * (sunset_angle * sin(lat_rad) * sin(soldecl) + cos(lat_rad) * cos(soldecl) * sin(sunset_angle))

	# if config.debug==2 : print("Extraterrestrial_radiation",lat,jday,ra)
	return(ra)
	
def Daylight_hours(lat,jday):
	lat_rad=lat*pi/180.
	soldecl=0.409*sin((2*pi)/365*jday - 1.39)
	sunset_angle=acos(-tan(lat_rad)*tan(soldecl))
	N=24/pi*sunset_angle
	
	# if config.debug==2 : print("Daylight_hours",lat,jday,N)
	return(N)

#Solar radiation (Rs)
#If the solar radiation, Rs, is not measured, it can be calculated with the Angstrom formula,
#which relates solar radiation to extraterrestrial radiation and relative sunshine duration:
#	where Rs solar or shortwave radiation [MJ m-2 day -1],
#	n actual duration of sunshine [hour],
#	N maximum possible duration of sunshine or daylight hours [hour],
#	n/N relative sunshine duration [-],
#	Ra extraterrestrial radiation [MJ m-2 day-1],
#	as regression constant, expressing the fraction of extraterrestrial radiation reaching the earth on overcast days (n = 0),
#	as+bs fraction of extraterrestrial radiation reaching the earth on clear days (n = N).
#
#The default values for as and bs are 0.25 and 0.50. 
#	

def Solar_radiation(lat,jday,n):
	const_as=0.25
	const_bs=0.5
	ra=Extraterrestrial_radiation(lat,jday)
	N=Daylight_hours(lat,jday)
	rs=(const_as+const_bs*n/N)*ra
	
	# if config.debug==2 : print("Solar_radiation",lat,jday,n,rs)
	return(rs)

#Solar radiation from cloudiness (Rs)
#If the solar radiation, Rs, is not measured, it can be calculated with the Angstrom formula,
#which relates solar radiation to extraterrestrial radiation and relative sunshine duration:
#    where Rs solar or shortwave radiation [MJ m-2 day -1],
#    n actual duration of sunshine [hour],
#    N maximum possible duration of sunshine or daylight hours [hour],
#    n/N relative sunshine duration [-], is equivalent to cloudiness cF
#    Ra extraterrestrial radiation [MJ m-2 day-1],
#    as regression constant, expressing the fraction of extraterrestrial radiation reaching the earth on overcast days (n = 0),
#    as+bs fraction of extraterrestrial radiation reaching the earth on clear days (n = N).
#
#The default values for as and bs are 0.25 and 0.50. 
#    

def Solar_radiation_cloudiness(lat,jday,cF):
	const_as=0.25
	const_bs=0.5
	ra=Extraterrestrial_radiation(lat,jday)
	rs=(const_as+const_bs*cF/100.)*ra
	return(rs)

#adjusted Hargreaves’ radiation formula
#	 where Ra extraterrestrial radiation [MJ m-2 d-1],
#	Tmax maximum air temperature [°C],
#	Tmin minimum air temperature [°C],
#	kRs adjustment coefficient [°C-0.5]. 
# Indicative default values are 0.16 for interior locations and 0.19 for coastal locations

def Solar_radiation_Hargreaves(tmax,tmin,ra,interior):
	if interior==1:
		krs=0.16
	else:
		krs=0.19
	rs=krs*sqrt(tmax-tmin)*ra
	
	# if config.debug==2 : print("Solar_radiation_Hargreaves:",tmax,tmin,ra,interior,rs)
	return(rs)

# Clear-sky solar radiation (Rso)
# The calculation of the clear-sky radiation, Rso, when n = N, is required for computing net longwave radiation. 
#	where Rso clear-sky solar radiation [MJ m-2 day-1],
#	z station elevation above sea level [m],
#	Ra extraterrestrial radiation [MJ m-2 day-1]. 

def Clearsky_radiation_z(ra,z):
	rso=(0.75+0.00002*z)*ra
	
	# if config.debug==2 : print("Clearsky_radiation_z:",ra,z,rso)
	return(rso)
	
def Clearsky_radiation_0(ra):
	const_as=0.25
	const_bs=0.5	
	rso=(const_as+const_bs)*ra
	
	# if config.debug==2 : print("Clearsky_radiation_0:",ra,rso)
	return(rso)
	
# Net solar or net shortwave radiation (Rns)
#	where Rns net solar or shortwave radiation [MJ m-2 day-1],
#	α albedo or canopy reflection coefficient for the reference crop [dimensionless],
#	Rs the incoming solar radiation [MJ m-2 day-1]. 
#
# If net solar radiation needs to be calculated when computing ETo, the fixed value of 0.23 
	
def Net_shortwave_radiation(albedo,rs):
	rns=(1-albedo)*rs
	
	# if config.debug==2 : print("Net_shortwave_radiation:",albedo,rs,rns)
	return(rns)

# Net longwave radiation (Rnl)
#	where Rnl net outgoing longwave radiation [MJ m-2 day-1],
#	σ Stefan-Boltzmann constant [ 4.903 10-9 MJ K-4m-2 day-1],
#	Tmax,K maximum absolute temperature during the 24-hour period [K = °C+ 273.16],
#	Tmin,K minimum absolute temperature during the 24-hour period [K = °C+ 273.16],
#	ea actual vapour pressure [kPa],
#	Rs/Rso relative shortwave radiation (limited to ≤1.0),
#	Rs measured or calculated (Equation 3.20) solar radiation [MJ m-2 day -1],
#	Rso calculated (Equation 3.21, 3.22) clear-sky radiation [MJ m-2 day -1]. 

def Net_longwave_radiation(Tmin,Tmax,ea,rs,rso):
	stef_boltz=4.903*pow(10,-9)

	Tmink=Tmin+273.16
	Tmaxk=Tmax+273.16

	rnl=stef_boltz * .5 * (pow(Tmink,4)+pow(Tmaxk,4)) * (0.34 -0.14*sqrt(ea)) * (1.35*(rs/rso)-0.35)
	
	# if config.debug==2 : print("Net_longwave_radiation:",Tmin,Tmax,ea,rs,rso,rnl)
	return(rnl)
	
#Net radiation (Rn)
#The net radiation (Rn) is the difference between the incoming net shortwave radiation (Rns)
# and the outgoing net longwave radiation (Rnl)

def Net_Radiation(rns,rnl):
	rn=rns-rnl
	
	# if config.debug==2 : print("Net_longwave_radiation:",rns,rnl,rn)
	return(rn)

def Rn_calculation(lat,jday,z,rn,rs,n,tmin,tmax,ea,interior,albedo,cloudiness=-9999):
	if(rn<=-9999): # If net radiation (Rn) is missing, Rn is cacultated by Eq. 3.25
		ra=Extraterrestrial_radiation(lat,jday)
		
		if(rs<=-9999): # If solar radiation is missing
			if n>-9999: # if the hours of bright sunshine are known
				rs=Solar_radiation(lat,jday,n)
			elif cloudiness!=-9999: # if cloudiness is known
				rs=Solar_radiation_cloudiness(lat,jday,cloudiness)
			elif tmin>-9999 and tmax>-9999: # if Tmin and Tmax are known
				rs=Solar_radiation_Hargreaves(tmax,tmin,ra,interior)
				

		rso=Clearsky_radiation_z(ra,z)				
		rnl=Net_longwave_radiation(tmin,tmax,ea,rs,rso)			   
		rns=Net_shortwave_radiation(albedo,rs)
		rn=Net_Radiation(rns,rnl)
	return(rn)
	
# ============== WIND SPEED ================
# Adjustment of wind speed to standard height
# To adjust wind speed data obtained from instruments placed at elevations other than the standard height of 2 m
#	where u2 wind speed at 2 m above ground surface [m s-1],
#	uz measured wind speed at z m above ground surface [m s-1],
#	z height of measurement above ground surface [m]. 

def u2_z(uz,z):
	u2=uz*4.87/log(67.8*z - 5.42)
	
	# if config.debug==2 : print("u2_z:",uz,z,u2)
	return(u2)

# ========== Reference evapotranspiration (FAO Penman-Monteith) ========
# The relatively accurate and consistent performance of the Penman-Monteith approach (Allen et al., 1998) in
# both arid and humid climates has been indicated in both the ASCE and European studies.

def et0_pm(lat,jday,z,rn,rs,n,ea,Tdew,Tmean,Tmin,Tmax,interior,Rhmin,Rhmax,Rhmean,uz,h,albedo,cloudiness=-9999):
	
	Tmean=tmean(Tmean,Tmin,Tmax)
	
	# if no temperature, we are lost
	if Tmean<=-9999:
		return(-9999)

	# if we only have temepartures, we can still calculate Hargreaves and Samani	
	if Rhmin<=-9999 and Rhmax<=-9999 and Rhmean<=-9999 and rs<=Radiation_wm2_to_Mjm2day(-9999) and rn<=-9999 and  Tdew<=-9999:
		ra=Extraterrestrial_radiation(lat,jday)
		et0=0.0023*(Tmean+17.8)*sqrt(Tmax-Tmin)*ra*0.408
		# if config.debug>=1 : print("Hargreaves!")
		return(et0)

	# at this point, we suppose we have everything needed to calculate some version of ET0	
	print(Tmean, Tmin, Tmax, rs, Rhmean, Rhmax, Rhmin, uz)
	P=Atm_Press(z)
	psy_const=psychrometric_const(P)
	delta=ssvp(Tmean)
	G=0.
	es=msvp_day(Tmin,Tmax)
	ea=ea_calculation(ea,Tdew, Tmin,Tmax,Tmean,Rhmin,Rhmax,Rhmean)
	rn=Rn_calculation(lat,jday,z,rn,rs,n,Tmin,Tmax,ea,interior,albedo,cloudiness)
	u2=u2_z(uz,h)
	

	et0=( 0.408*delta*(rn-G) + psy_const*(900./(Tmean+273.))*u2*(es-ea) ) / ( delta+psy_const*(1.+0.34*u2) )
	
	# if config.debug==2 : print("et0_pm:",et0)
	return(et0)


#
# Direct FAO56 equation for a complete meteo station (T°, Hr, u2, rs), with rs in w/m2/day
# Michel Le Page 2011
#

def et0_pm_simple(day1,alt,hmes,lat,tmoy,tmin,tmax,vv,hrmoy,hrmin,hrmax,rs):
	if ((hrmax-hrmin)<.1 or tmin==tmax): return(0)
	try: 
		conv_rad=lat * pi / 180.
		u2= vv * 4.87 / log(67.8*hmes-5.42)
		rs_mj= rs*24*3600*0.000001
		dr= 1+0.033*cos(2*pi*day1/365)
		d= 0.409*sin((2*pi*day1/365)-1.39)
		ws= acos(-tan(conv_rad)*tan(d))
		ra= (24*60/pi)*0.082*dr*(ws*sin(conv_rad)*sin(d)+cos(conv_rad)*cos(d)*sin(ws))
		rso= ra*(0.75+0.00002*alt)
		es= (0.6108*exp(17.27*tmin/(tmin+237.3))+0.6108*exp(17.27*tmax/(tmax+237.3)))/2
		ea= (hrmin*0.6108*exp(17.27*tmax/(tmax+237.3))+hrmax*0.6108*exp(17.27*tmin/(tmin+237.3)))/(2*100)
		rnl= 4.9*pow(10,-9)*0.5*(pow((tmin+273),4)+pow((tmax+273),4))*(0.34-0.14*sqrt(ea))*(1.35*(rs_mj/rso)-0.35)
		rn=(1-0.23)*rs_mj-rnl
		
		delta= 4098*0.6108*exp(17.27*tmoy /(tmoy +237.3))/pow((tmoy +237.3),2)
		et0= (0.408*delta*(rn)+(900*0.063/(tmoy+273))*u2*(es-ea))/(delta+0.063*(1+0.34*u2))
		return(et0)
	except:
		return(0)


#if __name__ == "__main__":
#
#	# INITIALISATIONS
#	albedo=0.23	 # Albedo for the FAO-56 Reference Grass
#	
#	lat=31.64	   # Latitude of the point in decimal degrees
#	z=600.		  # altitude in meters
#	interior=1.	 # In the case, there is no measurement os Solar radiation, indicate 1 for a point in the interior, 0 for a point on the coast
#	
#	jday=55.		# day since 1st of january of the year
#	
#	# AIR TEMPERATURE
#	
#	Tmean=12.92	 # The average of all measured Temperatures of the day in Celsius degrees
#	Tmin=10.		# The minimum Temperature of the day in Celsius degrees
#	Tmax=17.		# The maximum Temperature of the day in Celsius degrees
#	
#	# AIR HUMIDITY
#	
#	ea=-9999.	   # if measured, put ea here, else -9999.
#	Tdew=-9999.	 # if measured, put the Dew Point Temperature her, else -9999.
#	Rhmean=-9999	# The average of all Rh measured	
#	Rhmin=-9999	  # The minimum Relative Humidity of the day
#	Rhmax=-9999	  # The maximum Relative Humidity of the day
#
#	# RADIATION
#	
#	rn=-9999.	   # is measured, put Net Radiation here, else -9999
#	n=-9999.		# if measured, put the number of hours of clear sky her, else -9999.
#	rs_wm2=-9999   # The average of solar or shortwave radiation in W/m2. If not measured: -9999.
#	rs=Radiation_wm2_to_Mjm2day(rs_wm2)	# conversion of rs to Mj/m2/day
#
#	# WIND SPEED
#
#	uz=2			# Averaged wind speed of the day in m/s default=2
#	h=2.			# Height of measurement of Wind Speed in meters
#
#	et0=et0_pm(lat,jday,z,rn,rs,n,ea,Tdew,Tmean,Tmin,Tmax,interior,Rhmin,Rhmax,Rhmean,uz,h,albedo)
#	
#	et0_simple=et0_pm_simple(jday,z,h,lat,Tmean,Tmin,Tmax,uz,Rhmean,Rhmin,Rhmax,rs_wm2)
#	
#	print("TEST:",et0,et0_simple)
#
#	# ======= LECTURE D'UN FICHIER ===============
#	# date tmoy tmin tmax u2moy, u2min u2max hrmoy rswm2 hrmin hrmax
#	#2014-02-24 12.925000 10.00 16.99 1.881250 0.23 3.63 76.977708 164.149583 55.47 95.72 2.28557028581390603119 2.58957971379204355163 2.04300987542061971315 0.00 744.60
#
#	with open("d:\\Python\R3_et0.txt") as f:
#		Ligs = list(f)
#		jday=2
#		for Lig in Ligs:
#			try:
#				L=Lig.split(" ")
#				Date_text=L[0]
#				D=Date_text.split("-")
#				from datetime import *
#				jday=abs(date(int(D[0]),int(D[1]),int(D[2]))-date(int(D[0]),1,1)).days +1
#				Tmean=float(L[1])
#				Tmin=float(L[2])
#				Tmax=float(L[3])
#				uz=float(L[4])
#				Rhmean=float(L[7])
#				rs_wm2=float(L[8])
#				Rhmin=float(L[9])
#				Rhmax=float(L[10])
#				Rainf=float(L[14])			
#				rs=Radiation_wm2_to_Mjm2day(rs_wm2)
#				#print(jday,Tmean,Tmin,Tmax,uz,Rhmin,Rhmax,Rhmean,rs)
#				et0=et0_pm(lat,jday,z,rn,rs,n,ea,Tdew,Tmean,Tmin,Tmax,interior,Rhmin,Rhmax,Rhmean,uz,h,albedo)
#				rs=-9999. 
#				et02=et0_pm(lat,jday,z,rn,rs,n,ea,Tdew,Tmean,Tmin,Tmax,interior,Rhmin,Rhmax,Rhmean,uz,h,albedo)
#				
#				#et0_simple=et0_pm_simple(jday,z,h,lat,Tmean,Tmin,Tmax,uz,Rhmean,Rhmin,Rhmax,rs_wm2)
#				print(Date_text,jday,et0,et02,Rainf)
#			except:
#				print("")
#				#print(Date_text,Tmean,Tmin,Tmax,uz,Rhmin,Rhmax,Rhmean,rs)
