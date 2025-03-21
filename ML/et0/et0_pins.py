import torch
import torch.nn as nn
import torch.optim as optim
from cProfile import run
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import mode
from data_science_toolkit.dataframe import DataFrame
from chart import *
from data_science_toolkit.model import Model
from data_science_toolkit.vectorizer import Vectorizer
import numpy as np
from data_science_toolkit.lib import Lib
import datetime
import pandas as pd
import time
from sklearn.ensemble import ExtraTreesRegressor
import sklearn
import optuna
from xgboost import XGBClassifier, XGBRegressor, plot_importance
from sklearn.metrics.pairwise import cosine_similarity
from dateutil.relativedelta import *
import json
import gzip
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from data_science_toolkit.dataframe import DataFrame
# from climatefiller import ClimateFiller
from torch.utils.data import TensorDataset, DataLoader
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
import math
from sklearn.model_selection import train_test_split
import numpy as np

# Stephan Boltzmann constant (W m-2 K-4)
SB = 5.670373e-8
# heat capacity of dry air at constant pressure (J kg-1 K-1)
C_PD = 1003.5
# heat capacity of water vapour at constant pressure (J kg-1 K-1)
C_PV = 1865
# gas constant for dry air (rd), J/(kg*degK)
GAS_CONSTANT_FOR_DRY_AIR = 287.04
# acceleration of gravity (m s-2)
G = 9.8
# the density of water kg m-3
DENSITY_OF_WATER = 1000 
SOLAR_CONSTANT_MJ_MIN = 0.08202 # Solar constant (G_sc) in MJ/m²/min 
SOLAR_CONSTANT_MJ_HOUR = 4.9212 # Solar constant (G_sc) in MJ/m²/h 
SOLAR_CONSTANT_W_PER_M2 = 1367 # Solar constant (G_sc) in W/m² 
ALBEDO = 0.23  # Albedo coefficient for grass reference surface
CP = 1.013e-3  # Specific heat of air at constant pressure (MJ/kg°C)
EPSILON = 0.622  # Ratio molecular weight of water vapor/dry air
PI = torch.pi
LATENT_HEAT_OF_VAPORIZATION = 2.45  # Latent heat of vaporization for water (MJ/kg)
SIGMA = 0.000000004903  # Stefan-Boltzmann constant in MJ/K4/m2/day

def pressure(z):
    ''' Calculates the barometric pressure above sea level.

    Parameters
    ----------
    z: float
        height above sea level (m).

    Returns
    -------
    p: float
        air pressure (Kpa).'''
        
    P0 = 101.325  # Standard atmospheric pressure at sea level in kPa
    L = 0.0065    # Standard lapse rate in °C/m
    p = P0 * (((293 - (L * z)) / (293)) ** 5.26)

    return p

def latent_heat_of_vaporization(ta_c):
    """
    Estimate the latent heat of vaporization of water as a function of temperature, in MJ/kg.
    
    Parameters:
    - temp_celsius: float, temperature in degrees Celsius
    
    Returns:
    - lambda_v: float, latent heat of vaporization in MJ/kg
    """
    # Constants for water vaporization (values in J/g)
    # This approximation assumes a linear decrease from 2501.3 J/g at 0°C to 2264.7 J/g at 100°C
    
    # Adjust latent heat based on temperature
    lambda_v = 2.501 - (0.002361 * ta_c)
    return lambda_v

def sunset_hour_angle(lat, declination):
    """
    Calculate the sunset hour angle in radians.

    Parameters:
    latitude (float): Latitude in decimal degrees.
    declination (float): Solar declination in radians.

    Returns:
    float: Sunset hour angle in radians.
    """
    # Convert latitude to radians
    lat_rad = lat * (torch.pi / 180.0)
    
    # Calculate the sunset hour angle using the formula
    omega = torch.arccos(-torch.tan(lat_rad) * torch.tan(declination))
    
    return omega

def solar_declination(doy):
    """
    Calculate the solar declination in radians for a given day of the year using a precise trigonometric model.

    Parameters:
    - doy: int, day of the year (1 through 365 or 366)

    Returns:
    - declination: float, solar declination in radians
    """
    # Convert day of the year to radians within the sine function
    declination_radians = 0.409 * torch.sin(((2 * PI * doy) / 365) - 1.39)

    return declination_radians

def inverse_relative_distance_factor(doy):
        """
        Calculate the inverse relative distance factor (dr) for Earth-Sun based on the day of the year.
        
        Parameters:
        - day_of_year: int, the day of the year (1 to 365 or 366 for a leap year)
        
        Returns:
        - dr: float, the inverse relative distance factor (dimensionless)
        
        Description:
        This function uses the cosine function to calculate the Earth-Sun distance variation effect.
        """
        return 1 + (0.033 * torch.cos((2 * PI * doy) / 365))

def extraterrestrial_radiation_daily(lat, doy):
    """
    Calculate extraterrestrial radiation (Ra) for a given latitude and day of the year.

    Parameters:
    lat (float): Latitude in degrees. Positive for the northern hemisphere, negative for southern.
    doy (int): Day of the year (1 through 365 or 366).

    Returns:
    float: Extraterrestrial radiation in MJ/m^2/day.
    """
    
    lat_rad = lat * (torch.pi / 180.0)
    
    # Calculate the inverse relative distance Earth-Sun (dr)
    dr = inverse_relative_distance_factor(doy)
    
    # Calculate the solar declination (δ):
    delta = solar_declination(doy)
    
    # Calculate the sunset hour angle
    omega = sunset_hour_angle(lat, delta)
    
    # Calculate the extraterrestrial radiation
    ra = ((24 * 60) / PI) * SOLAR_CONSTANT_MJ_MIN * dr * ((omega * torch.sin(lat_rad) * torch.sin(delta)) + (torch.cos(lat_rad) * torch.cos(delta) * torch.sin(omega)))
    
    return ra

def psychrometric_constant(elevation, ta_c):
    """
    Calculate the psychrometric constant for a given altitude.

    Parameters:
    altitude (float): Altitude above sea level in meters.

    Returns:
    float: Psychrometric constant in kPa/°C.
    """
    
    lambda_v = latent_heat_of_vaporization(ta_c)  # Latent heat of vaporization (MJ/kg)
    
    # Calculate atmospheric pressure based on altitude
    p = pressure(elevation)
    
    # Calculate psychrometric constant
    gamma = (CP * p) / (EPSILON * lambda_v)
    
    return gamma

def saturation_vapor_pressure(ta_c):
    """
    Calculate saturation vapor pressure (es) in kPa given temperature (T) in Celsius
    
    """
    # Calculate saturation vapor pressure (es) using Magnus-Tetens formula
    es = 0.6108 * torch.exp((17.27 * ta_c) / (ta_c + 237.3))
    return es

def slope_saturation_vapor_pressure_curve(t_c, method='standard'):
    """
    Calculate the slope of the saturation vapor pressure curve at a given temperature.
    
    Parameters:
    - temp_celsius: float, temperature in degrees Celsius
    
    Returns:
    - delta: float, slope of the vapor pressure curve in kPa/°C
    """
    # Calculate saturation vapor pressure at the current temperature
    es = saturation_vapor_pressure(t_c)
    
    # Calculate the slope of the vapor pressure curve
    delta = (4098 * es) / ((t_c + 237.3) ** 2)
    return delta

# Define the model
class SimpleRegressionNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleRegressionNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.soft_plus = nn.Softplus()
        self.rrelu = nn.RReLU()
        self.tanh = nn.Tanh()
        self.elu = nn.ELU() 
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.elu(x)
        x = self.fc2(x)
        x = self.elu(x)
        x = self.fc3(x)
        return x
    
def et0_priestley_taylor_daily(input, alpha=1.5041): 
        # input variables
        # T = 25.0  # air temperature in degrees Celsius
        # RH = 60.0  # relative humidity in percent
        # u2 = 2.0  # wind speed at 2 m height in m/s
        # Rs = 15.0  # incoming solar radiation in MJ/m2/day
        # lat = 35.0  # latitude in degrees
        input_vector = input.clone()
        #ta_mean, rs_mean, rh_mean, lat, elevation, doy =  row['ta_mean'], row['rs_mean'], row['rh_mean'], row['lat'], row['elevation'], row['doy']
        G = 0  # Soil heat flux density (MJ/m2/day)
        
        # 0'ta_mean', 1'ta_max', 2'ta_min', 3'doy', 4'lat', 5'rh_mean', 6'rh_max', 7'rh_min', 8'ws_mean', 9'rs_mean', 10'elevation'
        ta_max, ta_min, doy, lat, rh_max, rh_min, rs_mean, elevation  =  input_vector[:, 0], input_vector[:, 1], input_vector[:, 2], input_vector[:, 3], input_vector[:, 4], input_vector[:, 5], input_vector[:, 6], input_vector[:, 7]
        
        rs_mean *= 0.0864  # convert watts per square meter to megajoules per square meter 0.0288 = 60x60x8hours or 0.0864 for 24 hours

        ta_mean = (ta_max + ta_min) / 2
        ta_max_kelvin = ta_max + 273.16  # air temperature in Kelvin
        ta_min_kelvin = ta_min + 273.16  # air temperature in Kelvin
        
        # saturation vapor pressure in kPa
        es_max = 0.6108 * torch.exp((17.27 * ta_max) / (ta_max + 237.3))
        es_min = 0.6108 * torch.exp((17.27 * ta_min) / (ta_min + 237.3))
        
        # actual vapor pressure in kPa
        ea_max_term = es_max * (rh_min / 100)
        ea_min_term = es_min * (rh_max / 100)
        ea = (ea_max_term + ea_min_term) / 2
        
        # in the absence of rh_max and rh_min
        #ea = (rh_mean / 100) * es
        
        # when using equipement where errors in estimation rh min can be large or when rh data integrity are in doubt use only rh_max term
        #ea = ea_min_term  
        
        delta = slope_saturation_vapor_pressure_curve(ta_mean) # slope of the vapor pressure curve in kPa/K
        
        # psychrometric constant in kPa/K
        gamma = psychrometric_constant(elevation, ta_mean)
        
        
        # Calculate extraterrestrial radiation
        ra = extraterrestrial_radiation_daily(lat, doy)
        
        # Calculate clear sky solar radiation
        rso = (0.75 + (2e-5 * elevation)) * ra
        
        # Calculate net solar shortwave radiation 
        rns = (1 - ALBEDO) * rs_mean
        
        # Calculate net longwave radiation
        
        rnl = SIGMA * (((torch.pow(ta_max_kelvin, 4) + torch.pow(ta_min_kelvin, 4)) / 2) * (0.34 - (0.14 * torch.sqrt(ea))) * ((1.35 * (rs_mean / rso)) - 0.35))
        
        # Calculate net radiation
        rn = rns - rnl
    
        et0 = (alpha * delta * (rn - G) * 0.408) / (delta + gamma)
        # output result
        return et0
  
def et0_makkink(input, c1=0.61, c2=0.12):
    """
    Calculate the reference evapotranspiration using the Priestley-Taylor method.

    Parameters:
    alpha (float): Empirical coefficient, typically around 1.26.
    Delta (float): Slope of the saturation vapor pressure curve at air temperature (kPa/°C).
    gamma (float): Psychrometric constant (kPa/°C).
    Rn (float): Net radiation at the crop surface (MJ/m²/day).
    G (float): Soil heat flux (MJ/m²/day), often assumed to be zero for daily calculations.

    Returns:
    float: Estimated ET0 in mm/day.
    """
    input_vector = input.clone()
    # rs_mean
    ta_mean = input_vector[:, 0]
    # ta_mean
    rs_mean = input_vector[:, 1]
    # elevation
    elevation = input_vector[:, 2]
    
    delta = slope_saturation_vapor_pressure_curve(ta_mean)
    gama = psychrometric_constant(elevation, ta_mean)
    lam = latent_heat_of_vaporization(ta_mean)
    
    # convert units
    rs_mean *= 0.0864  # convert watts per square meter to megajoules per square meter 0.0288 = 60x60x8hours or 0.0864 for 24 hours
    
    et0 = ((c1 * delta * rs_mean) / ((delta + gama) * lam)) - c2
    return et0

def et0_hargreaves_samani(input, c=0.0039, a=15.2, b=0.35):
    input_vector = input.clone()
    #print(input_vector)
    ta_mean, ta_max, ta_min, doy, lat  =  input_vector[:, 0], input_vector[:, 1], input_vector[:, 2], input_vector[:, 3], input_vector[:, 4]
    
    ra = extraterrestrial_radiation_daily(lat, doy)
    
    # convert ra from MJ/m2/day to mm/day
    ra *= 0.408
    
    temperature_range = ta_max - ta_min
    
    # et0 = 0.0023 * (ta_mean + 17.8) * ((ta_max - ta_min) ** 0.5) * 0.408 * ra
    
    et0 = c * (ta_mean + a) * (temperature_range ** b) * ra

    return et0
 
# Physics-based equation
def physics_equation(inputs, targets):
    # Assuming x is a 2D tensor with two input features (adjust indices based on your data)
    # print(x - targets)
    #print(inputs)

    #et0 = et0_priestley_taylor_daily(inputs, alpha=1.2353)
    #et0 = et0_makkink(inputs, c1=0.82, c2=0)
    et0 = et0_abtew(inputs)
    et0 =  et0.unsqueeze(1)
    # Compute the mean absolute error (MAE) loss
    # Define the criterion
    criterion = nn.MSELoss()
    mse = criterion(et0, targets)
    loss = mse
    return loss

def et0_abtew(input, k1=0.5762):
    """
    Calculate the reference evapotranspiration using the Priestley-Taylor method.

    Parameters:
    alpha (float): Empirical coefficient, typically around 1.26.
    Delta (float): Slope of the saturation vapor pressure curve at air temperature (kPa/°C).
    gamma (float): Psychrometric constant (kPa/°C).
    Rn (float): Net radiation at the crop surface (MJ/m²/day).
    G (float): Soil heat flux (MJ/m²/day), often assumed to be zero for daily calculations.

    Returns:
    float: Estimated ET0 in mm/day.
    """
    input_vector = input.clone()
    
    rs_mean = input_vector[:, 0]
    rs_mean *= 0.0864  # convert watts per square meter to megajoules per square meter 0.0288 = 60x60x8hours or 0.0864 for 24 hours
    
    lambda_v = LATENT_HEAT_OF_VAPORIZATION
    K1 = k1
    
    
    et0 = (K1 * rs_mean) / lambda_v
    return et0

# Train and evaluate the model
def train_and_evaluate(theta=0.5, epochs_nbr=1000, data_path='./weather_data_daily.csv'):
    # Initialize the model
    # Best hyperparameters:  {'hidden_size': 7, 'lr': 0.0001, 'batch_size': 8} old
    # Best hyperparameters:  {'hidden_size': 8, 'lr': 4e-05, 'batch_size': 4}
    input_dim = 1  # number of features
    output_size = 1
    hidden_layers_size = 4
    lr = 4e-05
    batch_size = 4
    shuffle_data = True

    # Transformer
    #model = TransformerRegressionModel(input_dim, model_dim, num_heads, num_encoder_layers, num_outputs)

    # Simple Neural Network
    model = SimpleRegressionNN(input_dim, hidden_layers_size, output_size)

    data_r3 = DataFrame(data_path)
    data_r3.column_to_date('datetime')
    data_r3.reindex_dataframe('datetime')
    data_r3.keep_columns(['et0_pm', 'rs_mean'])

    # scaling
    #data_r3.scale_columns(['ta_mean', 'ta_max', 'ta_min', 'rh_mean', 'rh_max', 'rh_min', 'ws_mean', 'rs_mean' ])
    #data_r3.scale_columns(['et0_pm'])
    #data_r3.convert_dataframe_type()

    target = data_r3.get_column('et0_pm').values
    features = data_r3.drop_column('et0_pm')
    features_train, features_test, target_train, target_test = train_test_split(features,
                                                                                target, 
                                                                                test_size=0.2,
                                                                                random_state=2,
                                                                                shuffle=shuffle_data)
    # Convert to PyTorch tensors
    features_train_tensor = torch.tensor(features_train.values, dtype=torch.float32)
    target_train_tensor = torch.tensor(target_train, dtype=torch.float32).view(-1, 1)  # Reshape to a column vector
    features_test_tensor = torch.tensor(features_test.values, dtype=torch.float32)
    # Define DataLoader for training
    train_dataset = TensorDataset(features_train_tensor, target_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle_data)
    # Define DataLoader for testing
    test_dataset = TensorDataset(features_test_tensor)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=shuffle_data)

    # Training the model
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    losses = []
    r2_scores = []
    rmse_scores = []
    rmse_scores = []
    theta = 0.5
    model.train()
    for epoch in range(epochs_nbr):
        epoch_loss = 0.0
        batch = 0
        #model.train()
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss_data_driven = criterion(outputs, targets)

            # Add physics-based regularization term
            loss_physics = physics_equation(inputs, targets)

            # Total loss with regularization
            loss =  ((1 - theta) * loss_data_driven) + (theta * loss_physics)
            
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            batch += 1

        # Calculate average loss for the epoch
        average_epoch_loss = epoch_loss / batch
        losses.append(average_epoch_loss)
        print(f'Epoch {epoch} | Loss: {average_epoch_loss}')
        #print(f'Epoch {epoch + 1}, Loss: {average_epoch_loss}')

    r2_scores = []
    rmse_scores = []
    r_scores = []

    # evaluation with scaling
    """# Evaluate the model
    model.eval()train_and_evaluate
train_and_evaluate
    with torch.no_grad():
        predictions_scaled = model(x)
        predictions = data_r3.vectorizer.inverse_transform(predictions_scaled.numpy())
        y_rescaled = data_r3.vectorizer.inverse_transform(y.numpy())
        r2 = r2_score(y_rescaled, predictions)
        rmse = math.sqrt(mean_squared_error(y_rescaled, predictions))
        print(f'RMSE: {rmse:.4f}, R2: {r2:.4f}')"""

    # test on the whole dataset
    # Deep Learning no scaling
    with torch.no_grad():
        model.eval()
        predictions = model(features_test_tensor)
        
        
        # Convert predictions to a NumPy array for compatibility with sklearn metrics
        predictions_np = predictions.numpy()
        target_test_np = target_test.reshape(-1, 1)  # Ensure the target test data is a 2D array for correlation calculation
        # Calculate Pearson correlation coefficient using NumPy
        predictions_flat = predictions_np.flatten()
        target_test_flat = target_test_np.flatten()
        
        r = np.corrcoef(predictions_flat, target_test_flat)[0, 1]
        r2 = r2_score(target_test, predictions)
        rmse = math.sqrt(mean_squared_error(target_test, predictions))
        
        r2_scores.append(r2)
        rmse_scores.append(rmse)
        r_scores.append(r)
        #model.train()
    print('PINNs model performance:-------------------------------')
    print(f'RMSE: {rmse_scores}, R2: {r2_scores}, R: {r_scores}')


    print(f'Physics-based model performance::-------------------------------')
    predictions_physic_based = et0_abtew(features_test_tensor)
    r2 = r2_score(target_test, predictions_physic_based)
    r = np.corrcoef(predictions_physic_based, target_test)[0, 1]
    rmse = math.sqrt(mean_squared_error(target_test, predictions_physic_based))
    print(f'RMSE: {rmse:.4f}, R2: {r2:.4f}, R: {r:.4f}')

# train_and_evaluate(0)
train_and_evaluate()