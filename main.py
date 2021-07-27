# Library we need
import pandas as pd
import numpy as np
import requests
import urllib.parse

# Read the data
df = pd.read_excel('Lapangan Jakarta.xlsx')
df.head()

# Get the longlat data!
longitude = []
latitude = []
error = 0
for index, row in df.iterrows():
    # Get the address
    mark = row['alamat']
    village = row['kelurahan']
    district = row['kecamatan']
    regency = row['wilayah']
    address = str(mark) + ', ' + str(village) + ', ' + str(district) + ', ' + str(regency)
    try:
        #We will search the longlat data from Nominatim Open Street Map
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        response = requests.get(url).json()
        longitude.append(response[0]["lon"])
        latitude.append(response[0]["lat"])
    except:
        # If you can't find the longlat data, it should be zero (0) for missing value
        longitude.append(0)
        latitude.append(0)
        error = error+1
print('Banyak error: '+str(error))

# Get longlat data part 2 from Gelanggang column!
longitude2 = []
latitude2 = []
error = 0
for index, row in df.iterrows():
    mark = row['gelanggang']
    village = row['kelurahan']
    district = row['kecamatan']
    regency = row['wilayah']
    address = str(mark) + ', ' + str(village) + ', ' + str(district) + ', ' + str(regency)
    try:
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        response = requests.get(url).json()
        longitude2.append(response[0]["lon"])
        latitude2.append(response[0]["lat"])
    except:
        # If you can't find the longlat data, it should be zero (0) for missing value
        longitude2.append(0)
        latitude2.append(0)
        error = error+1
print('Banyak error 2: '+str(error))

# Get the copy of original dataframe (so you can't lose the original file, if u still need it!)
df2 = df.copy()

# Put the results into new columns
df2['lon'] = longitude
df2['lat'] = latitude
df2['lon2'] = longitude2
df2['lat2'] = latitude2

# Imputation missing longlat (we initialize as 0 before)
new_lon = []
new_lat = []
for index, row in df2.iterrows():
    if row['lon'] == 0:
        new_lon.append(row['lon2'])
        new_lat.append(row['lat2'])
    else:
        new_lon.append(row['lon'])
        new_lat.append(row['lat'])
df2['new_lon']=new_lon
df2['new_lat']=new_lat

# Drop unused column
df2.drop(['lon','lat','lon2','lat2'], axis=1, inplace=True)

# Save the result to csv
df2.to_csv('Data with LongLat.csv', index=False)
