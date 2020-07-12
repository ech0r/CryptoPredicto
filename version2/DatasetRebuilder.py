from TrainingDatasetBuilder import getData
import numpy as np

dates = []
i = 0
with open("/crypto-predicto/olddata.csv") as f:
    for row in f:
        if i != 0:
            dates.append(row.split(',')[0])
        i+=1

for date in dates:
    print(date)
    getData(date)