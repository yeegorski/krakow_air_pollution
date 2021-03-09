#!/usr/bin/env python
# coding: utf-8

# In[4]:


# import all libraries needed
import numpy as np
import pandas as pd
import pickle

# create the special class that to be used to predict on new data
class air_pollution_model():
    
    # class constructor
    def __init__(self,model_file):
        # read the saved 'model' file
        with open('model','rb') as model_file:
            self.reg = pickle.load(model_file)
            self.data = None
    
    # take a data file and preprocess it
    def load_and_clean_data(self, data_file):
        """
        Load and prepare the data for the model.
        
        data_file is expected to have the following columns:
        * temperature (degrees Celcius)
        * humidity (values in the range from 0 to 1)
        * pressure (hPa)
        * windSpeed (km/h)
        * visibility (km)
        * windBearing (degrees)
        * time (%Y-%m-%d %H:%M:%S)

        """
        # import the data
        df = pd.read_csv(data_file)
        # store the data in a new variable for later use
        self.df_with_predictions = df.copy()
        
        # turn wind direction into dummy variables
        def wind_direction(direction):
            if direction > 45 and direction <= 135:
                return 'east_wind'
            elif direction > 135 and direction <= 225:
                return 'south_wind'
            elif direction > 225 and direction <= 315:
                return 'west_wind'
            else:
                return 'north_wind'
            
        df['windBearing'] = df['windBearing'].apply(wind_direction)
        wind_bearing_columns = pd.DataFrame(columns = ['east_wind','north_wind','west_wind','south_wind'])
        wind_bearing_columns[pd.get_dummies(df['windBearing']).columns] = pd.get_dummies(df['windBearing'])
        wind_bearing_columns.fillna(0, inplace = True)
        wind_bearing_columns.drop(['north_wind'],axis=1,inplace = True)
        
        # concatenate column values
        df = pd.concat([df,wind_bearing_columns], axis=1)
        # drop wind bearing feature
        df.drop(['windBearing'], axis = 1, inplace = True)
        
        # change the unit of speed from km/h to m/s
        df['windSpeed'] = df['windSpeed']/3.6
        
        # convert dates to datetime format
        df['time'] = pd.to_datetime(df['time'],format = '%Y-%m-%d %H:%M:%S')
        
        # create new feature month
        df['month'] = df['time'].apply(lambda time: time.month)

        # create new feature hour
        df['hour'] = df['time'].apply(lambda time: time.hour)

        # create new feature weekday
        df['weekday'] = df['time'].apply(lambda time: time.weekday())
        
        # create dummy variables from month (by seasons), hour (by part of the day), and weekday (weekend or not)
        def month_map(month):
            if month in [12,1,2]:
                return 'winter'
            elif month in [3,4,5]:
                return 'spring'
            elif month in [6,7,8]:
                return 'summer'
            else:
                return 'fall'

        def hour_map(hour):
            if hour in range(0,6):
                return 'night'
            elif hour in range(6,12):
                return 'morning'
            elif hour in range(12,18):
                return 'afternoon'
            else:
                return 'evening'

        def weekday_map(weekday):
            if weekday in range(0,5):
                return 'workday'
            else:
                return 'weekend'

        df['month'] = df['month'].apply(month_map)
        df['hour'] = df['hour'].apply(hour_map)
        df['weekday'] = df['weekday'].apply(weekday_map)
        
        season_columns = pd.DataFrame(columns = ['spring', 'summer', 'winter', 'fall'])
        season_columns[pd.get_dummies(df['month']).columns] = pd.get_dummies(df['month'])
        season_columns.fillna(0, inplace = True)
        season_columns.drop(['fall'],axis=1,inplace = True)
        
        daypart_columns = pd.DataFrame(columns = ['night','morning','afternoon','evening'])
        daypart_columns[pd.get_dummies(df['hour']).columns] = pd.get_dummies(df['hour'])
        daypart_columns.fillna(0, inplace = True)
        daypart_columns.drop(['afternoon'],axis=1,inplace = True)
                                      
        weekend_columns = pd.DataFrame(columns = ['workday','weekend'])
        weekend_columns[pd.get_dummies(df['weekday']).columns] = pd.get_dummies(df['weekday'])
        weekend_columns.fillna(0, inplace = True)
        weekend_columns.drop(['weekend'],axis=1,inplace = True)
                
        # concatenate column values
        df = pd.concat([df,season_columns,daypart_columns,weekend_columns], axis = 1)
        
        # drop time, month, hour, weekday columns
        df = df.drop(['time','month','hour','weekday'], axis = 1)
        
        df = df[['temperature', 'humidity', 'pressure', 'windSpeed', 'visibility', 'east_wind', 'south_wind', 'west_wind',
                 'spring', 'summer', 'winter', 'evening', 'morning', 'night', 'workday']]
        
        # create a variable to call the preprocessed data
        self.data = df.copy()
        
    
    # predict the PM2 and the pollution level and
    # add columns with these values at the end of the new data
    def predicted_outputs(self):
        """
        Returns a dataframe with predicted outputs (PM2.5) and the respective pollution level. 
        """
        # divide data on pollution levels
        def pol_levels(x):
            if x <= 12:
                return 'healthy'
            elif x > 12 and x <=35.4:
                return 'moderate'
            elif x > 35.4 and x <=55.4:
                return 'unhealthy for sensitive groups'
            elif x > 55.4 and x <=150.4:
                return 'unhealthy'
            else:
                return 'hazardous' 
                
        if (self.data is not None):
            self.data['PM2'] = self.reg.predict(self.data)
            self.data['Pollution Level'] = self.data['PM2'].apply(pol_levels)
            return self.data


# In[ ]:




