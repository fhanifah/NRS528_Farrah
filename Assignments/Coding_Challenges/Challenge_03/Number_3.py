# 3. Working with CSV

# Question:
# Using the Atmospheric Carbon Dioxide Dry Air Mole Fractions from quasi-continuous daily measurements at Mauna Loa, Hawaii dataset, obtained from here (https://github.com/datasets/co2-ppm-daily/tree/master/data).

# Using Python (csv) calculate the following:
# 1. Annual average for each year in the dataset.
# 2. Minimum, maximum and average for the entire dataset.
# 3. Seasonal average if Spring (March, April, May), Summer (June, July, August), Autumn (September, October, November) and Winter (December, January, February).
# 4. Calculate the anomaly for each value in the dataset relative to the mean for the entire time series.

# Answer:
import csv

# 1. Annual average for each year in the dataset.
with open('co2-ppm-daily.csv') as co2:
    next(co2)
    year_list = []
    for row in csv.reader(co2):
        year = row[0].split('-')[0]
        if year not in year_list:
            year_list.append(year)

for y in year_list:
    with open('co2-ppm-daily.csv') as co2:
        next(co2)
        annual_sum = 0
        numdata = 0
        for row in csv.reader(co2):
            if row[0].split('-')[0] == y:
                annual_sum += float(row[1])
                numdata += 1
        annual_avg = annual_sum/numdata
        print('Annual average of atmosperic CO2 for year',y,': ',round(annual_avg,2))

# 2. Minimum, maximum and average for the entire dataset.
with open('co2-ppm-daily.csv') as co2:
    next(co2)
    sum_all = 0
    numdata = 0
    minVal, maxVal = [], []
    for row in csv.reader(co2):
        sum_all += float(row[1])
        numdata += 1
        minVal.append(float(row[1]))
        maxVal.append(float(row[1]))
    avg_all = sum_all/numdata   
    print('Total average of atmosperic CO2: ',round(avg_all,2))
    print('Minimum value of atmosperic CO2: ',round(min(minVal),2))
    print('Maximum value of atmosperic CO2: ',round(max(maxVal),2))
    
# 3. Seasonal average if Spring (March, April, May), Summer (June, July, August), Autumn (September, October, November) and Winter (December, January, February).
with open('co2-ppm-daily.csv') as co2:
    next(co2)
    spring_sum = 0
    summer_sum = 0
    autumn_sum = 0
    winter_sum = 0
    numdata_spring = 0
    numdata_summer = 0
    numdata_autumn = 0
    numdata_winter = 0
    for row in csv.reader(co2):
        if int(row[0].split('-')[1]) == 3 or int(row[0].split('-')[1]) == 4 or int(row[0].split('-')[1]) == 5:
            spring_sum += float(row[1])
            numdata_spring += 1
            spring_avg = spring_sum/numdata_spring
        elif int(row[0].split('-')[1]) == 6 or int(row[0].split('-')[1]) == 7 or int(row[0].split('-')[1]) == 8:
            summer_sum += float(row[1])
            numdata_summer += 1
            summer_avg = summer_sum/numdata_summer
        elif int(row[0].split('-')[1]) == 9 or int(row[0].split('-')[1]) == 10 or int(row[0].split('-')[1]) == 11:
            autumn_sum += float(row[1])
            numdata_autumn += 1
            autumn_avg = autumn_sum/numdata_autumn
        elif int(row[0].split('-')[1]) == 12 or int(row[0].split('-')[1]) == 1 or int(row[0].split('-')[1]) == 2:
            winter_sum += float(row[1])
            numdata_winter += 1
            winter_avg = winter_sum/numdata_winter
    print('Seasonal average of atmosperic CO2 for Spring (March, April, May): ',round(spring_avg,2))
    print('Seasonal average of atmosperic CO2 for Summer (June, July, August): ',round(summer_avg,2))
    print('Seasonal average of atmosperic CO2 for Autumn (September, October, November): ',round(autumn_avg,2))
    print('Seasonal average of atmosperic CO2 for Winter (December, January, February): ',round(winter_avg,2))

# 4. Calculate the anomaly for each value in the dataset relative to the mean for the entire time series.
with open('co2-ppm-daily.csv') as co2:
    next(co2)
    annual_sum = 0
    numdata = 0
    for row in csv.reader(co2):
        anomaly = float(row[1]) - avg_all
        print('Aanomaly of atmosperic CO2 for',row[0],'is',round(anomaly,2),'relative to total average')
