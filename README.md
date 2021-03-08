# Krakow Air Pollution Project
This project is dedicated to the air pollution levels in Krakow, Poland. Polish cities rank high in various researches on air quality in Europe. According to the Swiss air monitoring platform IQAir, Krakow takes 29th place in Europe's most polluted cities 2019 [ranking](https://www.iqair.com/world-most-polluted-cities?continent=59af92ac3e70001c1bd78e52&country=&state=&page=1&perPage=50&cities=). **Using weather conditions, the model predicts the level of very fine particulate matter known as PM2.5, a pollutant posing the greatest health risk.**

* Scraped Krakow weather data from 2019 and 2020 and PM2.5 data
* Performed data preprocessing (coped with missing data, transformed categorical features, scaled the data, removed the outliers, engineered new features)
* Performed exploratory data analysis
* Created and evaluated models with sklearn's LinearRegression and RandomForests
* Created a python module on the model with the best performance

## Code and Resources Used
**Python Version:** 3.7  
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, sklearn, json, pickle  
**Historical Weather Data:** https://www.getambee.com/api-documentation.  
**PM2.5 Data:** https://powietrze.gios.gov.pl/pjp/current/station_details/archive/400.  
**WHO Air Quality Guidelines:** https://apps.who.int/iris/bitstream/handle/10665/69477/WHO_SDE_PHE_OEH_06.02_eng.pdf?sequence=1.  
**24-Hour PM2.5 Levels (μg/m3)** https://blissair.com/what-is-pm-2-5.htm

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
