# Krakow Air Pollution Project
This project is dedicated to the air pollution levels in Krakow, Poland. Polish cities rank high in various researches on air quality in Europe. According to the Swiss air monitoring platform IQAir, Krakow takes 29th place in Europe's most polluted cities 2019 [ranking](https://www.iqair.com/world-most-polluted-cities?continent=59af92ac3e70001c1bd78e52&country=&state=&page=1&perPage=50&cities=). **Using weather conditions, the model predicts the level of very fine particulate matter known as PM2.5, a pollutant posing the greatest health risk.**

* Scraped Krakow weather data from 2019 and 2020 and PM2.5 data
* Performed data preprocessing  (coped with missing data, transformed categorical features, scaled the data, removed the outliers, engineered new features, checked for multicollinearity)
* Performed exploratory data analysis
* Created and evaluated models with sklearn's LinearRegression and RandomForest  
* Created a python module on the model with the best performance

## Code and Resources Used
**Python Version:** 3.7  
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, sklearn, requests, json, pickle  
**Historical Weather Data:** https://www.getambee.com/api-documentation.  
**PM2.5 Data:** https://powietrze.gios.gov.pl/pjp/current/station_details/archive/400.  
**WHO Air Quality Guidelines:** https://apps.who.int/iris/bitstream/handle/10665/69477/WHO_SDE_PHE_OEH_06.02_eng.pdf?sequence=1.  
**24-Hour PM2.5 Levels (μg/m3):** https://blissair.com/what-is-pm-2-5.htm

## Web Scraping
Using getambee.com's API, I scraped the hourly weather data for Krakow from 2019 and 2020. With each job, I received the following data:
* time
* temperature
* apparent temperature
* dew point
* humidity
* pressure
* wind speed
* wind gust
* wind bearing
* cloud cover
* visibility
* ozone

I downloaded the air pollution levels from the Polish Environmental Protection Inspection's web page.

## Data Preprocessing
After scraping the data, I needed to clean it up to be usable for the model. I made the following changes and created the following features:
* converted epoch to human-readable date (e.g. 1546383600 -> 2019-01-01 23:00:00)
* substituted missing *ozone* values in 2019 with values from 2020 after having checked that they are reasonably close for other dates
* turned *windBearing* into dummy variables, as it indicated the wind direction (north, east, south, and west)
* merged the weather data with the air pollution data
* removed *PM2.5* outliers from the dataset
* dropped rows with unknown values (*pressure*, *windGust*)
* created features *month*, *hour*, and *weekday* from *time* feature,then based on those features created dummy variables for seasons, parts of the day, and workdays/weekends

## EDA
![alt text](https://github.com/yeegorski/krakow_air_pollution/blob/main/PM2.png "Pollution levels 2019-2020, PM2.5")

**Pollution levels 2019-2020, PM2.5**   
Horizontal lines indicate upper bounds of the air pollution levels used for calculating air quality index:
* green - healthy
* yellow - moderate
* orange - unhealthy for sensitive groups
* red - unhealthy
* purple - hazardous

![alt text](https://github.com/yeegorski/krakow_air_pollution/blob/main/temperature.png "Temperature levels 2019-2020, degrees Celsius")

**Temperature levels 2019-2020, degrees Celsius, with gradient showing the PM2.5 levels**


![alt text](https://github.com/yeegorski/krakow_air_pollution/blob/main/corr_matrix.png "Heatmap of the feature correlation matrix")

**Heatmap of the feature correlation matrix**  
Some features show high correlation -- I will remove those for the linear model to avoid multicollinearity.

## Model Building

I split the data into train and test sets with a test size of 20%.

I tried linear regression and random forest models and evaluated them using .score() method, which shows the model accuracy.

**Multiple Linear Regression** – baseline for the model.  
**Random Forest** – given data's sparsity, I thought that this would be the right choice.

## Model Performance

The Random Forest model outperformed the Linear Regression on the test set.

**Random Forest:** accuracy score = 0.6976  
**Linear Regression:** accuracy score = 0.4305

## Model Deployment

In this step, I saved ("pickled") the model and wrote a python module. It can be called along with a list of weather data and date and return an estimated air pollution level (PM2.5).
Data needed for the model:
* temperature	
* humidity
*	pressure	
*	windSpeed	
*	visibility	
*	windBearing	
*	date and time  
I stick to this set of features, as they are easily accessible in any weather application. A random forest model with ozone levels produced a little higher accuracy, but I opted for the model's usability and dropped the feature.


## Some Insights from the Data
* More polluted air comes in winter, as many Polish homes are still heated with coal and wood. 
* The air quality in Krakow tends to get worse when the wind is blowing from the west. That is where the Silesia region is located - the Polish coal mining hub.
* The most smog is usually coming in the morning hours (from midnight till 6 am), following the day's coldest hours.
* Pressure might alleviate the smog burden or reinforce it depending on where the wind is blowing from. Low pressure and the west wind might cause more air pollution than high pressure and the wind from the same direction. 
