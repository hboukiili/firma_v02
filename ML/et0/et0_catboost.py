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
# from data_science_toolkit import ClimateFiller
from torch.utils.data import TensorDataset, DataLoader
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
import math
from sklearn.model_selection import train_test_split
import numpy as np
import joblib

import pandas as pd


# data_r3 = DataFrame('/app/tools/et0/weather_data.csv') 
# data_r3.column_to_date('datetime')
# data_r3.reindex_dataframe('datetime')
# data_r3.show()

# #data_r3.keep_columns(['et0_pm', 'ta_mean', 'ta_max', 'ta_min', 'rh_mean', 'rh_max', 'rh_min', 'ws_mean', 'rs_mean' ])
# data_r3.keep_columns(['et0_pm', 'ta_max', 'rs_mean', 'rh_mean'])
# data_r3.show()

# #print(data_r3.similarity_measure('et0_pm', 'et0_hs_bc', 'ts'))


# y, x = data_r3.get_column('et0_pm'), data_r3.drop_column('et0_pm')

# model = Model(x, y, 'cb')
# model.train()
# print(model.report())

# joblib.dump(model, "./et0_model.pkl")

# print("✅ Model trained and saved as et0_model.pkl")



import pandas as pd
import joblib

# Load trained model
model = joblib.load("et0_model.pkl")

# Define new weather data with correct order
new_weather_data = pd.DataFrame({
    "ta_max": [32.5,24,42,12,90],       
    # "ta_min": [20.3,20,39,30,99],       
    # "ta_mean": [26.4],      
    # "rh_max": [75],         
    # "rh_min": [30],       
    "rh_mean": [50,70,80,90,49],        
    "rs_mean": [200,100,100,99,120],       
    # "wind_speed_10m": [2.5]
})


# Predict ET0
predicted_et0 = model.predict(new_weather_data)

print("🔮 Predicted ET0:", predicted_et0[0], "mm/day")

