# This program allows you to visualize in a map the IP route given by traceroute.py.

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import matplotlib.pyplot as plt
import geocoder

#Lectura de datos
ip_path = pd.read_csv('UPs.csv')

#calculo coordenadas 
lats = []
longs = []
city = []
for i in ip_path['IP']:
    a = geocoder.ip(i)
    lats.append(a.lat)
    longs.append(a.lng)
    city.append(a.city)
    
ip_path['city'] = city
ip_path['lat'] = lats
ip_path['longs'] = longs
    
#Limpieza de datos por si de alguna IP no puede sacar la ciudad
ip_path.dropna()

#plot
fig = plt.figure(figsize=(20,5))

#tipo de mapa
ax = plt.axes(projection=ccrs.PlateCarree())

# feature del mapa
ax.coastlines()
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.BORDERS)

#ax.stock_img() #si se quiere el planisferio tipo imagen completo (comentar los features)

#nommbre ciudad
for i in range(len(ip_path)):
    plt.text(ip_path['longs'][i], ip_path['lat'][i], ip_path['city'][i],
         horizontalalignment='right',
         transform=ccrs.Geodetic())
#dots ciudad
plt.plot(ip_path['longs'], ip_path['lat'],
         color='red', linewidth=1, marker='o',
         transform=ccrs.Geodetic(),
         )

plt.title('Route of packet to destiny')

plt.show()
