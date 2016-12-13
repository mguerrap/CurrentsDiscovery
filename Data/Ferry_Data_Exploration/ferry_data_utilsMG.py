import numpy as np
import pandas as pd
import xarray as xr
from netCDF4 import Dataset
from matplotlib import path

def ferry_data_download(URL):
	"""Downloads the ADCP data from ferry"""
	#Inputs:
	# URL with the location of the ferry NetCDF file
	#Outputs:
	# An object containing the link to the ferry data
	ferry = xr.open_dataset(URL)

	return(ferry)

def ferry_data_QC(ferry,TH_abs,TH_u,TH_d):
	"""Gets the variables and pass a QC to estimate final velocities"""
	#Inputs: ferry data in an xarray DataSet, treshold for absolute 
	# velocities, TH for true velicities, TH for depth
	#Outputs: Quality Controled ferry data in a xarra DataSet

	# QC1: make nan all Absolute velocities that are greater than 6.5 m/s
	absu =  ferry.eastward_absolute_water_velocity.where(
		(abs(ferry.eastward_absolute_water_velocity) < TH_abs) &
		(abs(ferry.northward_absolute_water_velocity) < TH_abs))
	absv =  ferry.northward_absolute_water_velocity.where(
		(abs(ferry.eastward_absolute_water_velocity) < TH_abs) &
		(abs(ferry.northward_absolute_water_velocity) < TH_abs))
	absw =  ferry.vertical_absolute_water_velocity.where(
		(abs(ferry.eastward_absolute_water_velocity) < TH_abs) &
		(abs(ferry.northward_absolute_water_velocity) < TH_abs))
	# Get bottom track velocity for reference 
	# and also clean for TH in abs velocity
	east_btv = ferry.eastward_bottom_tracking_velocity.where(
		(abs(ferry.eastward_absolute_water_velocity) < TH_abs) &
		(abs(ferry.northward_absolute_water_velocity) < TH_abs))
	north_btv = ferry.northward_bottom_tracking_velocity.where(
		(abs(ferry.eastward_absolute_water_velocity) < TH_abs) & 
		(abs(ferry.northward_absolute_water_velocity) < TH_abs))
	vert_btv = ferry.vertical_bottom_tracking_velocity.where(
		(abs(ferry.eastward_absolute_water_velocity) < TH_abs) &
		(abs(ferry.northward_absolute_water_velocity) < TH_abs))
	# Estimate u_true = abs_u + east_bt_v
	u_true = absu + east_btv
	v_true = absv + north_btv
	w_true = absw + vert_btv
	U = np.sqrt(u_true**2 + v_true**2)
	# QC2: check that u_true and v_true are less than 4 m/s
	u_true = u_true.where((u_true < TH_u) & (v_true < TH_u) & (U < TH_u))
	v_true = v_true.where((u_true < TH_u) & (v_true < TH_u) & (U < TH_u))
	w_true = w_true.where((u_true) < TH_u & (v_true < TH_u) & (U < TH_u))
	U = U.where((u_true) < TH_u & (v_true < TH_u) & (U < TH_u))
	# Add true velocity data to the dataset
	ferry['u_true'] = u_true
	ferry['v_true'] = v_true
	ferry['w_true'] = w_true
	ferry['Horizontal_speed'] = U
	#Remove first 5 rows of depth
	ferryQC = ferry.isel(depth = slice(TH_d, None))
	return(ferryQC)