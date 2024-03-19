
# %%
# import necessary libraries
import pandas as pd
import numpy as np
import math
import seaborn as sns
import datetime
import matplotlib.pylab as plt
import plotly.graph_objects as go
from pathlib import Path
from matplotlib import pyplot
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from matplotlib.ticker import NullFormatter
import matplotlib.ticker as ticker
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, DotProduct, RBF
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
#%matplotlib inline

# %%
from pymongo import MongoClient
import pymongo
# MongoDB Atlas connection string
# Replace '<your_connection_string>' with your actual connection string
connection_string = '<your_connection_string>'

try:
    # Connect to MongoDB Atlas
    client = MongoClient(connection_string)
# return a friendly error if a URI error is thrown 
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string (found the .env)?")

#print(client.list_database_names())



# %%
database_name = 'scrape'
db = client[database_name]
#print(db.list_collection_names())


# %%
collection_name = 'scraped_raw'
collection = db[collection_name]

# Fetch data from MongoDB and convert it to a DataFrame
cursor = collection.find()
data = list(cursor)
cars = pd.DataFrame(data)

# Convert DataFrame to CSV
csv_filename = 'output_data.csv'
cars.to_csv(csv_filename, index=False)

# Close the MongoDB connection
client.close()

print(f'Data has been successfully exported to {csv_filename}')



# %%
cars = pd.read_csv('output_data.csv')

# %%
#cars = pd.read_csv('data.csv')

# %%
cars.head()

# %%
cars.shape[0]

# %% [markdown]
# ## Data Cleaning

# %%
# drop unnecessary variables: id, url, region_url, VIN, image_url, description, lat, and long
cars = cars.drop(columns = ['_id', 'link'])

# %%
cars.head()

# %%
# look at the number of NA values by column
cars.isna().sum()

# %%
#cars = cars.drop(columns = ['images/23','images/22','images/21','images/20','images/19','images/18','images/17','images/16','images/15','images/14','images/13','images/12','images/11','images/10','images/9','images/8', 'images/7','images/6','images/5','images/4','images/3','images/2','images/1'])

# %%
cars = cars.drop(columns = ['scraper-version','scrape-date','images'])
cars.head()

# %%
cars.shape[0]

# %%
# drop NA values
cars = cars.dropna()

# %%
cars.shape[0]

# %%
cars.head()

# %%
# convert year and odometer to integer values
#cars['odometer'] = cars['odometer'].str.replace('K', '').str.replace(' miles', '').astype(int) * 1000
#cars['odometer'] = cars['odometer'].str.replace('K miles', '').str.replace(' miles · Dealership', '').astype(float).astype(int) * 1000
import re
cars['odometer'] = cars['odometer'].apply(lambda x: int(re.search(r'\d+', str(x)).group(0)) if re.search(r'\d+', str(x)) else None)
cars['year'] = cars['title'].str.extract(r'(\d{4})')
# Fill NaN values in the 'year' column with a placeholder (you can choose a value that makes sense)
cars['year'].fillna(-1, inplace=True)
cars = cars.astype({'year':'int', 'odometer':'int'})

# %%
# create an age variable to get a better understanding of how old a car is
cars['age'] = datetime.date.today().year - cars['year']

# %%
cars.head()

# %% [markdown]
# ## Data Exploration

# %%
sns.histplot(data = cars, x = 'age', binwidth = 5).set(title = 'Distribution of Car Ages')

# %%
cars[cars['year'] < 1990]

# %%
cars = cars[cars.year >= 2005]

# %%
cars.shape[0]

# %%
# looking again at the distribution of ages
sns.histplot(data = cars, x = 'age', binwidth = 1).set(title = 'Distribution of Car Ages')

# %%
cars.shape[0]

# %%
sns.histplot(data = cars, x = 'odometer').set(title = 'Distribution of Car Odometer')

# %%
cars[cars['odometer'] > 300]

# %%
cars = cars[cars.odometer <= 300]
# Clean up the 'price' column by replacing non-numeric values with NaN
cars['price'] = pd.to_numeric(cars['price'].replace('[\$,]', '', regex=True), errors='coerce')

# Fill NaN values in the 'price' column with a placeholder (you can choose a value that makes sense)
cars['price'].fillna(-1, inplace=True)

# Convert 'price' column to integers
cars['price'] = cars['price'].astype(int)


# %%
cars.shape[0]

# %%
sns.histplot(data = cars, x = 'odometer').set(title = 'Distribution of Car Odometer')

# %%
sns.scatterplot(data = cars, x = 'odometer', y = 'price').set(title = 'Correlation of Vehicle Odometer and List Price')

# %%
cars[cars['price'] > 100000]

# %%
cars = cars[cars.price <= 100000]

# %%
cars.shape[0]

# %%
# look at the odometer vs price now
sns.scatterplot(data = cars, x = 'odometer', y = 'price').set(title = 'Correlation of Vehicle Odometer and List Price')

# %%
sns.histplot(data = cars, x = 'price').set(title = 'Distribution of List Price')

# %%
cars[cars['price'] < 1000]

# %%
cars = cars[cars.price >= 1000]

# %%
sns.histplot(data = cars, x = 'price').set(title = 'Distribution of List Price')

# %%
cars.shape[0]

# %%
#Dictionary of car makes
kbb_make = {
    'acura',
    'alfa-romeo',
    'aston-martin',
    'audi',
    'bentley',
    'bmw',
    'buick',
    'cadillac',
    'chevrolet',
    'chrysler',
    'dodge',
    'ferrari',
    'fiat',
    'ford',
    'genesis',
    'gmc',
    'honda',
    'hyundai',
    'infiniti',
    'jaguar',
    'jeep',
    'kia',
    'lamborghini',
    'land rover',
    'lexus',
    'lincoln',
    'lucid',
    'maserati',
    'mazda',
    'mclaren',
    'mercedes-benz',
    'mini',
    'mitsubishi',
    'nissan',
    'polestar',
    'porsche',
    'ram',
    'rivian',
    'rolls-royce',
    'subaru',
    'tesla',
    'toyota',
    'volkswagen',
    'volvo',
}

# Dictionary to store car models for each make
kbb_models = {
    'acura': ['ILX', 'MDX', 'NSX','RDX','TLX'],
    'alfa-romeo': ['Giulia', 'Stelvio'],
    'aston-martin': ['DB11', 'DBS', 'DBX','Vantage'],
    'audi': ['A3', 'A4','A4 allroad','A5', 'A6','A6 allroad',
             'A7','A8','e-tron','e-tron GT','e-tron S',
             'e-tron S Sportback','e-tron Sportback','Q3',
             'Q4 e-tron','Q4 Sportback e-tron','Q5', 
             'Q5 Sportback','Q7','Q8','R8','RS 3','RS 5',
             'RS 6','RS 7', 'RS e-tron GT','RS Q8','S3',
             'S4','S5','S6','S7','S8','SQ5','SQ5 Sportback',
             'SQ7','SQ8','TT'],
    'bentley': ['Bentayga','Continental GT','Flying Spur'],
    'bmw': ['2 Series','3 Series','4 Series', '5 Series',
            '6 Series','7 Series','8 Series','i4','iX','M3',
            'M4','M5','M8','X1','X2','X3','X3 M','X4','X4 M','X5',
            'X5 M','X6','X6 M','X7','Z4'],
    'buick': ['Enclave','Encore','Encore GX','Envision'],
    'cadillac': ['CT4','CT5','Escalade','Escalade ESV','XT4','XT5','XT6'],
    'chevrolet': ['Blazer','Bolt EUV','Bolt EV','Camaro','Colorado Crew Cab',
                  'Colorado Extended Cab','Corvette','Equinox','Express 2500 Cargo',
                  'Express 2500 Passenger','Express 3500 Cargo','Express 3500 Passenger',
                  'Malibu','Silverado 1500 Crew Cab','Silverado 1500 Double Cab',
                  'Silverado 1500 Regular Cab','Silverado 1500 Limited Crew Cab',
                  'Silverado 1500 Limited Double Cab','Silverado 1500 Limited Regular Cab',
                  'Silverado 2500 HD Crew Cab','Silverado 2500 HD Double Cab',
                  'Silverado 2500 HD Regular Cab','Silverado 3500 HD Crew Cab',
                  'Silverado 3500 HD Double Cab','Silverado 3500 HD Regular Cab',
                  'Spark','Suburban','Tahoe','Trailblazer','Traverse','Trax',
                  'Avalanche','Cruze','Impala','Lumina','Malibu Maxx','Monte Carlo','SS','Uplander','Venture'],
    'chrysler': ['300','Pacifica','Pacifica Hybrid','Voyager'],
    'dodge': ['Charger', 'Challenger', 'Durango'],
    'ferrari': ['296 GTB','812 Competizione','812 Competizione A','812 GTS',
                'F8', 'Portofino', 'SF90', 'Roma'],
    'fiat': ['500X'],
    'ford': ['Bronco', 'Bronco Sport','E-Transit 350 Cargo Van','EcoSport', 'Edge', 
             'Escape','Escape Plug-in Hybrid', 'Expedition','Expedition MAX', 
             'Explorer', 'F150 Lightning', 'F150 Regular Cab','F150 Super Cab',
             'F150 SuperCrew Cab', 'F250 Super Duty Crew Cab','F250 Super Duty Regular Cab',
             'F250 Super Duty Super Cab', 'F350 Super Duty Crew Cab','F350 Super Duty Regular Cab',
             'F350 Super Duty Super Cab', 'F450 Super Duty Crew Cab','F450 Super Duty Regular Cab', 
             'Maverick', 'Mustang','Mustang MACH-E', 'Ranger SuperCab','Ranger SuperCrew', 
             'Transit 150 Cargo Van', 'Transit 150 Crew Van', 'Transit 150 Passenger Van',              
             'Transit 250 Cargo Van', 'Transit 250 Crew Van', 'Transit 350 HD Cargo Van', 'Transit 350 HD Crew Van',
             'Transit 350 Cargo Van', 'Transit 350 Crew Van', 'Transit 350 Passenger Van', 
             'Transit Connect Cargo Van', 'Transit Connect Passenger Wagon','C-Max Hybrid','C-Max Energi',
             'Fiesta','Flex','Focus','Fusion','Mustang Mach-E','Taurus','Thunderbird'],
    'genesis': ['G70', 'G80','G90', 'GV70','GV80'],
    'gmc': ['Acadia','Canyon Crew Cab','Canyon Extended Cab','HUMMER EV Pickup','Savana 2500 Cargo','Savana 2500 Passenger', 
            'Savana 3500 Cargo','Savana 3500 Passenger','Sierra 1500 Crew Cab', 'Sierra 1500 Double Cab','Sierra 1500 Regular Cab',
            'Sierra 1500 Limited Crew Cab', 'Sierra 1500 Limited Double Cab', 'Sierra 1500 Limited Regular Cab', 
            'Sierra 2500 HD Crew Cab','Sierra 2500 HD Double Cab','Sierra 2500 HD Regular Cab', 'Sierra 3500 HD Crew Cab',
            'Sierra 3500 HD Double Cab','Sierra 3500 HD Regular Cab', 'Yukon', 'Yukon XL', 'Terrain','C1500 Pickup','C2500 Pickup',
            'C3500 Pickup','Envoy','Envoy XL','Envoy XUV','Jimmy','R/V 3500 Series','S15 Jimmy','Safari','Savana 1500 Cargo',
            'Savana 1500 Passenger','Savana 2500 Cargo','Savana 2500 Passenger','Savana 3500 Cargo',
            'Savana 3500 Passenger','Sierra 1500 Classic Crew Cab','Sierra 1500 Classic Double Cab',
            'Sierra 1500 Classic Regular Cab','Sierra 1500 HD Classic Crew Cab','Sierra 1500 HD Classic Double Cab',
            'Sierra 1500 HD Classic Regular Cab','Sierra 2500 Classic Crew Cab','Sierra 2500 Classic Double Cab',
            'Sierra 2500 Classic Regular Cab','Sierra 3500 Classic Crew Cab','Sierra 3500 Classic Double Cab',
            'Sierra 3500 Classic Regular Cab','Sonoma','Suburban 1500','Suburban 2500','Syclone','Typhoon',
            'Vandura 1500','Vandura 2500','Vandura 3500','Yukon XL 1500','Yukon XL 2500'],
    'honda': ['Accord', 'Accord Hybrid', 'Civic', 'CR-V', 'CR-V Hybrid', 'HR-V', 'Insight', 'Odyssey', 'Passport', 'Pilot',
              'Fit','Element','Prelude','S2000','Crosstour','Ridgeline'],
    'hyundai': ['Accent', 'Elantra', 'Elantra N' , 'IONIQ5', 'Ioniq Hybrid','Ioniq Plug-in Hybrid','Kona', 'Kona Electric', 'Kona N',
                'Palisade', 'Santa Fe', 'Santa Fe Hybrid', 'Santa Fe Plug-in Hybrid','Sonata', 'Sonata Hybrid', 'Tucson', 'Tucson Hybrid', 
                'Tucson Plug-in Hybrid', 'Venue', 'Veloster', 'Santa Cruz','Azera','Equus','Genesis Coupe','Genesis G70','Genesis G80',
                'Genesis G90','Santa Fe Sport','Santa Fe XL','Veracruz'],
    'infiniti': ['Q50', 'Q60','QX50','QX55','QX60','QX80','EX35','EX37','FX35','FX37','FX45','FX50',
                'G25','G35','G37','I30','I35','JX35',
                'M35','M35h','M37','M45','M56','Q40',
                'Q45','QX4','QX56','QX60 Hybrid',
                'QX70',],
    'jaguar': ['XF', 'E-PACE','F-PACE','F-TYPE', 'I-PACE','S-Type','X-Type','XE','XE SV Project 8','XJ','XJR',
                'XJR-S','XJS','XK','XK-Series'],
    'jeep': ['Cherokee', 'Compass', 'Gladiator', 'Grand Cherokee', 'Grand Cherokee 4xe', 'Grand Cherokee L', 'Grand Wagoneer','Renegade', 
             'Wagoneer','Wrangler','Wrangler Unlimited', 'Wrangler Unlimited 4xe','CJ-5','CJ-7','CJ-8 Scrambler','Commander','Comanche','Dispatcher',
            'FC-150','FC-170','FC-170 DRW','Gladiator (JT)','Grand Cherokee SRT',
            'Grand Cherokee SRT8','Grand Cherokee Trackhawk','Grand Wagoneer (SJ)',
            'J-100','J-2500','J-2600','J-2700','J-2800','J-3500','J-3600',
            'J-3700','J-3800','J10','J20','Jeepster','Jeepster Commando','Liberty',
            'Patriot','Scrambler','Wagoneer (SJ)','Wagoneer (XJ)','Willys','Wrangler (JK)',
            'Wrangler (LJ)','Wrangler (TJ)','Wrangler (YJ)'],
    'kia': ['Cadenza', 'Forte', 'K5', 'K900', 'Niro', 'Rio', 'Seltos', 'Sorento', 'Soul', 'Sportage', 'Stinger', 
            'Telluride','Amanti','Borrego','Forte5','K900','Optima','Optima Hybrid','Rondo','Sedona',
            'Sephia','Sorento Sport','Soul EV','Spectra','Sportage Hybrid','Telluride Nightfall Edition'],
    'lamborghini': ['Aventador', 'Huracan', 'Urus','Gallardo','Centenario','Diablo','Gallardo Spyder','Huracan Evo','Huracan Evo Spyder',
            'Huracan Performante','Huracan Performante Spyder','Huracan Spyder',
            'Murcielago','Murcielago Roadster','Reventon','Urus Graphite Capsule'],
    'land rover': ['LR2','LR4','Defender', 'Discovery', 'Discovery Sport', 'Range Rover', 'Range Rover Evoque', 'Range Rover Sport', 'Range Rover Velar',
                   'Discovery Series II','Discovery Series II SD','Discovery Sport SD',
                    'Discovery Series II SE7','Discovery Series II XD','Freelander',
                    'Freelander SE','Freelander SE3','LR2 HSE','LR3','LR3 HSE','LR3 SE',
                    'LR4 HSE','LR4 HSE LUX','LR4 V8','LR4 V8 HSE LUX','Range Rover 4.0 SE',
                    'Range Rover 4.6 HSE','Range Rover HSE','Range Rover Velar R-Dynamic',
                    'Range Rover Velar S','Range Rover Velar SE','Range Rover Velar SVAutobiography Dynamic',
                    'Range Rover Westminster','Range Rover Westminster Edition','Range Rover 4.6 HSE',
                    'Range Rover Autobiography','Range Rover Autobiography Black','Range Rover Autobiography Black LWB',
                    'Range Rover Autobiography L','Range Rover Autobiography LWB',
                    'Range Rover HSE','Range Rover HSE LUX','Range Rover Long Wheelbase','Range Rover SE',
                    'Range Rover Sport','Range Rover Sport 5.0L V8 Supercharged','Range Rover Sport GT Limited Edition',
                    'Range Rover Sport HSE','Range Rover Sport HST','Range Rover Sport Limited Edition','Range Rover Sport SC',
                    'Range Rover Sport SE','Range Rover Sport Supercharged','Range Rover Sport SVR',
                    'Range Rover Velar','Range Rover Velar First Edition','Range Rover Velar P250 S','Range Rover Velar P250 SE',
                    'Range Rover Velar P250 R-Dynamic S','Range Rover Velar P250 R-Dynamic SE','Range Rover Velar P250 R-Dynamic HSE',
                    'Range Rover Velar P340 S','Range Rover Velar P340 SE','Range Rover Velar P340 R-Dynamic S',
                    'Range Rover Velar P340 R-Dynamic SE','Range Rover Velar P380 R-Dynamic HSE','Range Rover 4.0 SE',
                    'Range Rover Autobiography','Range Rover Autobiography Black',
                    'Range Rover Autobiography Black LWB','Range Rover Autobiography L',
                    'Range Rover Autobiography LWB','Range Rover HSE','Range Rover HSE LUX',
                    'Range Rover Long Wheelbase','Range Rover SE'],
    'lexus': ['ES', 'GS', 'GX', 'IS', 'LS', 'LX', 'NX', 'RC', 'RX', 'UX','CT','ES 250','ES 300','ES 300h','ES 330','ES 350','GS 200t','GS 300',
            'GS 350','GS 400','GS 430','GS 450h','GS 460','GS F','GX 460','GX 470','HS 250h','IS 200t','IS 250',
        'IS 300','IS 350','IS 350C','LC 500','LC 500h','LFA','LS 400',
        'LS 430','LS 460','LS 500','LS 500h','LS 600h','LX 450','LX 470',
        'LX 570','NX 200t','NX 300','NX 300h','RC 200t','RC 300','RC 350',
        'RC F','RX 300','RX 330','RX 350','RX 350L','RX 400h','RX 450h',
        'RX 450hL','SC 300','SC 400','SC 430','UX 200','UX 250h',
        'GS 300','GS 350','GS 450h','GS F','IS 200t','IS 300',
        'LC 500','LC 500h','LS 500','LS 500h','LX 570','NX 200t',
        'NX 300','RC 300','RC 350','RC F','RX 350','RX 450h',
        'ES 250','ES 300','ES 300h','ES 330','ES 350','GS 200t',
        'GS 300','GS 350','GS 400','GS 430','GS 450h','GS F','GX 460',
        'GX 470','HS 250h','IS 200t','IS 250','IS 300','IS 350',
        'IS 350C','LC 500','LC 500h','LFA','LS 400','LS 430',
        'LS 460','LS 500','LS 500h','LS 600h','LX 450','LX 470',
        'LX 570','NX 200t','NX 300','NX 300h','RC 200t','RC 300',
        'RC 350','RC F','RX 300','RX 330','RX 350','RX 350L',
        'RX 400h','RX 450h','RX 450hL','SC 300','SC 400','SC 430',
        'UX 200','UX 250h'],
    'lincoln': ['Aviator', 'Continental', 'Corsair', 'MKS','MKZ','MKT','MKX', 'Nautilus', 'Navigator', 'Navigator L','Blackwood','Capri','Continental Mark III','Continental Mark IV',
                'Continental Mark V','Continental Mark VI','Corsair','LS','Mark LT',
                'Mark VI','Mark VII','Mark VIII','MKS','MKT','MKX','MKZ',
                'Nautilus','Navigator','Navigator L','Town Car','Versailles',
                'Zephyr'],
    'lucid': ['Air','Air Dream Edition','Air Grand Touring','Air Pure','Air Touring'],
    'maserati': ['Ghibli', 'GranTurismo','Levante','MC20', 'Quattroporte','430','GranSport','GranTurismo MC','Levante GTS','Levante S',
                'Quattroporte GTS','Quattroporte S','Quattroporte Trofeo'],
    'mazda': ['CX-30', 'CX-5', 'CX-9', 'Mazda3', 'Mazda6', 'MX-5 Miata','323','626','929','B-Series Pickup','CX-3','CX-7','CX-9',
                'GLC','Mazda2','Mazda3 Sport','Mazda5','Mazda6 Sport',
                'MAZDASPEED MX-5','MAZDASPEED Protege','MAZDASPEED3',
                'MAZDASPEED6','Millenia','MPV','MX-3','MX-5 Miata RF','MX-6',
                'Navajo','Protege','Protege5','RX-7','RX-8','Tribute'],
                'mclaren': ['570S', '600LT', '720S', '765LT','GT',
                '570S Spider','600LT Spider','620R','675LT','675LT Spider',
                '720S Spider','765LT Spider','GT','GT Coupe','GT Spider',
                'MP4-12C','MP4-12C Spider','P1'],
    'mclaren': ['570S', '600LT', '720S', '765LT','GT'],
    'mercedes-benz': ['A-Class', 'C-Class', 'E-Class', 'G-Class', 'GLA', 'GLC', 'GLE', 'GLS', 'S-Class','190-Class','260-Class','300-Class','350-Class','380-Class','400-Class','420-Class',
                '450-Class','500-Class','560-Class','600-Class','AMG GT','B-Class','C-Class Coupe',
                'C-Class Wagon','CL-Class','CLA','CLA-Class','CLK-Class','CLS','CLS-Class',
                'E-Class Coupe','E-Class Wagon','G-Class','GL-Class','GLA-Class','GLB','GLB-Class',
                'GLC Coupe','GLC-Class','GLE Coupe','GLE-Class','GLK-Class','GLS-Class',
                'M-Class','Maybach S-Class','Metris','R-Class','S-Class Coupe',
                'S-Class Maybach','SL-Class','SLC-Class','SLK-Class','SLR McLaren','SLS AMG',
                'Sprinter'],
    'mini': ['Clubman', 'Convertible', 'Countryman', 'Hardtop','Cooper','Cooper Clubman','Cooper Countryman','Cooper Paceman',
        'Hardtop 2 Door','Hardtop 4 Door','John Cooper Works',
        'John Cooper Works Clubman','John Cooper Works Convertible',
        'John Cooper Works Countryman','John Cooper Works Hardtop',
        'John Cooper Works Hardtop 2 Door','John Cooper Works Hardtop 4 Door',
        'John Cooper Works Paceman'],
    'mitsubishi': ['Outlander', 'Eclipse Cross', 'Pajero','3000GT','Diamante','Eclipse','Eclipse Spyder','Endeavor','Expo',
                'Galant','Lancer','Mighty Max','Mirage','Montero','Montero Sport',
                'Outlander PHEV','Outlander Sport','Raider','Sigma','Van'],
    'nissan': ['370Z', 'Altima', 'Armada', 'Frontier', 'Kicks', 'LEAF', 'Maxima', 'Murano', 'NV Cargo', 'NV Passenger', 'NV200', 'Pathfinder', 'Rogue', 'Rogue Sport', 'Titan', 'Versa',
               '200SX','240SX','300ZX','350Z','370Z Coupe','370Z NISMO','370Z Roadster',
                'Altima Hybrid','Armada','Cube','Frontier King Cab','Frontier Crew Cab',
                'GT-R','Kicks','LEAF','Maxima','Murano','Murano CrossCabriolet','NV Cargo','NV Passenger','NV200',
                'Pathfinder','Quest','Rogue','Rogue Select','Rogue Sport',
                'Sentra','Titan King Cab','Titan Crew Cab','Titan XD',
                'Versa','Versa Note','Versa Sedan','Xterra','Altima','Armada',
                'Cube','Frontier','GT-R','JUKE','Kicks','LEAF','Maxima',
                'Murano','Murano CrossCabriolet','NV Cargo','NV Passenger',
                'NV200','Pathfinder','Quest','Rogue','Rogue Select','Rogue Sport',
                'Sentra','Titan'],
    'polestar': ['2', '1', '3'],
    'porsche': ['911', 'Cayenne', 'Macan', 'Panamera', 'Taycan','718 Cayman','911 Carrera','911 Carrera 4','911 Carrera 4 Cabriolet',
                '911 Carrera 4 GTS','911 Carrera 4S','911 Carrera 4S Cabriolet',
                '911 Carrera Cabriolet','911 Carrera GTS','911 Carrera S',
                '911 Carrera S Cabriolet','911 Targa','911 Targa 4',
                '911 Targa 4 GTS','911 Targa 4S','911 Turbo','911 Turbo Cabriolet',
                '911 Turbo S','911 Turbo S Cabriolet','918 Spyder','Boxster',
                'Carrera GT','Cayenne','Cayenne Coupe','Cayenne E-Hybrid','Cayenne GTS',
                'Cayenne S','Cayenne S E-Hybrid','Cayenne Turbo','Cayenne Turbo S E-Hybrid',
                'Cayman','Macan','Panamera','Panamera 4','Panamera 4 E-Hybrid',
                'Panamera 4 Executive','Panamera 4S','Panamera 4S E-Hybrid',
                'Panamera Executive','Panamera GTS','Panamera S','Panamera Turbo',
                'Panamera Turbo Executive','Panamera Turbo S E-Hybrid'],
    'ram': ['1500', '2500', '3500','1500 Classic','1500 Classic Crew Cab','1500 Classic Quad Cab',
        '1500 Classic Regular Cab','2500','3500','3500 Chassis Cab',
        '4500 Chassis Cab','5500 Chassis Cab','C/V','Dakota',
        'ProMaster Cargo Van','ProMaster Chassis Cab','ProMaster City Cargo',
        'ProMaster City Wagon','ProMaster Cutaway','ProMaster Window Van'],
    'rivian': ['R1T', 'R1S'],
    'rolls-royce': ['Cullinan', 'Dawn', 'Ghost', 'Phantom', 'Wraith','Cullinan Black Badge','Dawn','Dawn Black Badge','Ghost',
                'Ghost Black Badge','Phantom','Phantom Drophead Coupe',
                'Phantom Drophead Coupe Waterspeed Collection','Phantom Coupe',
                'Phantom Coupe Aviator Collection','Phantom Coupe Waterspeed Collection',
                'Phantom Coupe Tiger Edition','Wraith','Wraith Black Badge'],
    'subaru': ['Ascent', 'BRZ', 'Crosstrek', 'Forester', 'Impreza', 'Legacy', 'Outback', 'WRX',
               'Ascent','Baja','BRAT','BRZ','Crosstrek','Crosstrek Hybrid',
                'Forester','Impreza','Impreza Outback Sport','Impreza WRX',
                'Legacy','Outback','SVX','Tribeca','WRX','XT','XT6'],
    'tesla': ['Model 3', 'Model S', 'Model X', 'Model Y'],
    'toyota': ['4Runner', 'Avalon', 'C-HR', 'Camry', 'Corolla', 'Highlander', 'Land Cruiser', 'Prius', 'RAV4', 
               'Sequoia', 'Sienna', 'Tacoma', 'Tundra', 'Venza', 'Yaris', 'Corolla Hatchback',
                'Corolla Hybrid','Corolla iM','FJ Cruiser','GR86','Highlander',
                'Highlander Hybrid','Land Cruiser','Matrix','Mirai','MR2',
                'MR2 Spyder','Paseo','Previa','Prius','Prius c','Prius Plug-in',
                'Prius Prime','Prius Prime Advanced','Prius Prime Premium',
                'Prius v','RAV4','RAV4 Prime','Sequoia','Sienna',
                'Supra','T100','Tacoma','Tercel','Tundra','Venza',
                'Yaris','Yaris iA','4Runner','Avalon','Avalon Hybrid',
                'C-HR','Camry','Camry Hybrid','Camry Solara','Celica',
                'Corolla','Corolla Hatchback','Corolla Hybrid','Corolla iM',
                'FJ Cruiser','GR86','Highlander','Highlander Hybrid',
                'Land Cruiser','Matrix','Mirai','MR2','MR2 Spyder',
                'Paseo','Previa','Prius','Prius c','Prius Plug-in',
                'Prius Prime','Prius Prime Advanced','Prius Prime Premium',
                'Prius v','RAV4','RAV4 Prime','Sequoia','Sienna',
                'Supra','T100','Tacoma','Tercel','Tundra','Venza',
                'Yaris','Yaris iA'],
    'volkswagen': ['Arteon', 'Atlas', 'Golf', 'Jetta', 'Passat', 'Tiguan',
                   'Atlas','Atlas Cross Sport','Beetle','Cabrio',
                'CC','e-Golf','EuroVan','Fox','GLI','Golf','Golf Alltrack',
                'Golf GTI','Golf R','Golf SportWagen','ID.4','Jetta','Jetta GLI',
                'Karmann Ghia','Microbus','Passat','Quantum','R32','Rabbit',
                'Routan','Tiguan','Touareg','Touareg 2'],
    'volvo': ['S60', 'S90', 'V60', 'V90', 'XC40', 'XC60', 'XC90','240','740','760','780','850','940','960','C30',
                'C40 Recharge','C70','S40','S60 Cross Country','S60 Recharge',
                'S70','S80','S90 Recharge','V40','V50','V60','V60 Cross Country',
                'V60 Recharge','V70','V90','V90 Cross Country','V90 Recharge',
                'XC40','XC40 Recharge','XC60','XC60 Recharge','XC70',
                'XC90','XC90 Recharge'],
}

# %%

from difflib import get_close_matches

title = cars['title']

# Function to extract make from title
def extract_make(title):
    title_lower = title.lower()
    for make in kbb_make:
        if make in title_lower:
            return make
        elif (len(make) >= 4 and make[:4] in title_lower):
            return make
    return None

def extract_model_wreg(title, make):
    title_lower = title.lower()

    # Check if the make is in the kbb_models dictionary
    make_models = kbb_models.get(make, [])

    # Use regex to find patterns like "2021 RAM 3500" in the title
    match = re.search(r'\b\d{4}\s*[a-zA-Z0-9-]+\s*([a-zA-Z0-9-]+)\b', title)

    if match:
        # Extracted model is in the first capturing group
        model = match.group(1)

        if model is not None:
            # Handle models with dashes
            model = model.replace("-", "")

            # Compare with the kbb_models dictionary
            matched_model = get_close_matches(model, make_models, n=1)

            if matched_model:
                return matched_model[0]
            else:
                # If no direct match, try finding a close match using pieces of words
                title_words = re.findall(r'\b\w+\b', title)
                extracted_model_pieces = []

                for word in title_words:
                    # Check if the word is part of the make name, if yes, skip it
                    if make is not None and word.lower() in make.lower():
                        continue

                    extracted_model_pieces.append(word)
                    current_model_attempt = ' '.join(extracted_model_pieces)

                    # Check if the current attempt is a close match
                    matched_model = get_close_matches(current_model_attempt, make_models, n=1)
                    if matched_model:
                        return matched_model[0]

                # If still no match, return the original extracted model
                return model
        else:
            return None
    else:
        return None

# Apply the extraction functions
cars['manufacturer'] = cars['title'].apply(extract_make)
cars['model'] = cars.apply(lambda row: extract_model_wreg(row['title'], row['manufacturer']), axis=1)

# Print the DataFrame with 'manufacturer' and 'model'
result_df = cars[['manufacturer', 'model']]
print(result_df)

# Save the selected columns to CSV
result_df.to_csv('output.csv', index=False)

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(data=cars, x='manufacturer', y='price', estimator=np.median, ax=ax).set(title='Median List Price by Manufacturer')
plt.xticks(rotation=45)


# %%
cars.groupby(['manufacturer'])['price'].median().sort_values(ascending = False)

# %%
cars['manufacturer'].value_counts()

# %%
cars.shape[0]

# %%
# Drop rows where either 'manufacturer' or 'model' is empty
cars.dropna(subset=['manufacturer', 'model'], inplace=True)

# Print the DataFrame with 'manufacturer' and 'model'
result_df = cars[['manufacturer', 'model']]
print(result_df)

# Save the selected columns to CSV
#result_df.to_csv('outputff.csv', index=False)


# %%
cars.shape[0]

# %%
numeric_columns = ['price', 'year', 'odometer','age']
#cars.groupby(['title_status'])[numeric_columns].median()

# %% [markdown]
# ## Modeling

# %% [markdown]
# ### Segmentation

# %%
cars.head()

# %% [markdown]
# VEHICLE FREQUENCY MODEL

# %%
# Function to analyze frequency of vehicle models
def analyze_frequency(vehicle_data):
    model_frequency = vehicle_data['model'].value_counts()
    return model_frequency

# Function to assess risk associated with vehicles based on frequency
def assess_risk(model_frequency, threshold=6):
    # Define a threshold for significant frequency
    # Vehicles with frequency above this threshold are considered high risk
    high_risk_models = model_frequency[model_frequency > threshold].index.tolist()
    return high_risk_models

# Analyze frequency of vehicle models
model_frequency = analyze_frequency(cars)

# Assess risk associated with vehicles based on frequency
high_risk_models = assess_risk(model_frequency)

# Add a column to indicate if the model is high risk
cars['high_risk'] = cars['model'].apply(lambda x: x in high_risk_models)

# Print high-risk models
print("High-risk models based on significant frequency:")
print(high_risk_models)


# %%
import matplotlib.pyplot as plt

# Function to create better visuals for frequency analysis
def visualize_frequency(model_frequency, threshold=6):
    # Plotting frequency of vehicle models
    plt.figure(figsize=(12, 6))
    model_frequency.plot(kind='bar', color='skyblue')
    plt.title('Frequency of Vehicle Models')
    plt.xlabel('Vehicle Model')
    plt.ylabel('Frequency')

    # Adjust x-axis labels to cut short if too long
    x_labels = [label[:8] + '...' if len(label) > 11 else label for label in model_frequency.index]
    plt.xticks(range(len(x_labels)), x_labels, rotation=45, ha='right', fontsize=8)  # Rotate and adjust fontsize
    plt.axhline(y=threshold, color='red', linestyle='--', linewidth=2, label='Threshold')  # Add threshold line
    plt.legend()
    plt.tight_layout()
    plt.show()

# Visualize frequency of vehicle models
visualize_frequency(model_frequency, threshold=6)

# Function to create better visuals for risk assessment
def visualize_risk(high_risk_models):
    # Plotting high-risk models
    plt.figure(figsize=(10, 6))
    plt.bar(high_risk_models, model_frequency[high_risk_models], color='salmon')
    plt.title('High-Risk Vehicle Models')
    plt.xlabel('Vehicle Model')
    plt.ylabel('Frequency')

   # Adjust x-axis labels to cut short if too long
    x_labels = [label[:15] + '...' if len(label) > 18 else label for label in high_risk_models]
    plt.xticks(range(len(x_labels)), x_labels, rotation=45, ha='right', fontsize=8)  # Rotate and adjust fontsize
    plt.tight_layout()
    plt.show()

# Visualize high-risk vehicle models
visualize_risk(high_risk_models)


# %%
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Step 1: Define Target Variable
target_variable = 'high_risk'

# Step 2: Feature Selection
# Select relevant features
#features = ['age', 'odometer', 'manufacturer', 'model']  # Add more features as needed
# Assuming all columns except 'high_risk' are features
features = [col for col in cars.columns if col != target_variable]

# Make a copy of the DataFrame
cars_encoded = cars.copy()

# Example: Convert categorical variables to numerical using one-hot encoding
cars_encoded = pd.get_dummies(cars_encoded, columns=[col for col in cars_encoded.columns if col not in [target_variable]], drop_first=True)

# Step 5: Split Data
X = cars_encoded.drop(columns=[target_variable])
y = cars_encoded[target_variable]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Model Training
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 7: Model Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))


""" 

# Step 6: Model Training
# Update the RandomForestClassifier with hyperparameters and use cross-validation for evaluation
from sklearn.model_selection import cross_val_score

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
cv_scores = cross_val_score(model, X_train, y_train, cv=5)  # Perform 5-fold cross-validation
model.fit(X_train, y_train)

# Step 7: Model Evaluation
# Use cross-validated accuracy and classification report for evaluation
print("Cross-Validated Accuracy:", cv_scores.mean())
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

##########
# Step 6: Model Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))


"""

# %%


# %%
from sklearn.dummy import DummyClassifier

# Create and train the baseline model (predicts the most frequent class)
baseline_model = DummyClassifier(strategy='most_frequent')
baseline_model.fit(X_train, y_train)

# Evaluate the baseline model
baseline_accuracy = baseline_model.score(X_test, y_test)
print("Baseline Model Accuracy:", baseline_accuracy)

# Evaluate the RandomForestClassifier model
model_accuracy = model.score(X_test, y_test)
print("RandomForestClassifier Model Accuracy:", model_accuracy)

# Compare the performance of the models
if model_accuracy >= baseline_accuracy:
    print("RandomForestClassifier model outperforms the baseline model.")
else:
    print("RandomForestClassifier model does not outperform the baseline model.")


# %%
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Create a bar plot to visualize model accuracies
model_names = ['Baseline', 'RandomForestClassifier']
accuracies = [baseline_accuracy, model_accuracy]

plt.figure(figsize=(8, 6))
sns.barplot(x=model_names, y=accuracies, palette='viridis')
plt.title('Comparison of Model Accuracies')
plt.ylabel('Accuracy')
plt.ylim(0, 1)  # Set y-axis limit to 0-1 for accuracy scale
plt.show()

# Create a confusion matrix to compare predictions
baseline_pred = baseline_model.predict(X_test)
model_pred = model.predict(X_test)

# Create confusion matrices
baseline_cm = confusion_matrix(y_test, baseline_pred)
model_cm = confusion_matrix(y_test, model_pred)

# Plot confusion matrices
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.heatmap(baseline_cm, annot=True, cmap='YlGnBu', fmt='d', cbar=False)
plt.title('Baseline Model Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')

plt.subplot(1, 2, 2)
sns.heatmap(model_cm, annot=True, cmap='YlGnBu', fmt='d', cbar=False)
plt.title('RandomForestClassifier Model Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')

plt.tight_layout()
plt.show()


# %% [markdown]
# MARKET PRICE COMPARISION

# %%
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np
from difflib import get_close_matches
import matplotlib.pyplot as plt
import seaborn as sns

# Function to scrape current market price from Kelly Blue Book
def get_kbb_price(row):
    base_url = 'https://www.kbb.com/'
    
    # Check if vehicle_make and vehicle_model are not None or float
    if isinstance(row['manufacturer'], str) and isinstance(row['model'], str):
        # Replace spaces with dashes in the manufacturer and model for the URL
        make_url_part = row["manufacturer"].lower().replace(" ", "-")
        model_url_part = row["model"].lower().replace(" ", "-")
        
        search_url = f'{base_url}{make_url_part}/{model_url_part}/{row["year"]}/'
        #print(search_url)
        try:
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract relevant information (adjust based on the actual HTML structure)
            # Extract the price information from the HTML code
            #price_field = soup.find('div', {'class': 'nationalBaseDefaultPrice'})
            #kbb_price = price_field['content'] if price_field else None

            # Use regular expression to extract the price information
            pattern = re.compile(r'"nationalBaseDefaultPrice":(\d+),')
            match = pattern.search(response.text)
            
            kbb_price = match.group(1) if match else None

            return kbb_price

            #return kbb_price.text.strip() if kbb_price else None
        except Exception as e:
            print(f"Error: {e}")
            return None
    else:
        return None


# Use ThreadPoolExecutor to parallelize the scraping process
with ThreadPoolExecutor(max_workers=5) as executor:
    kbb_prices = list(executor.map(get_kbb_price, cars.to_dict(orient='records')))

# Add the kbb_prices to the DataFrame
cars['kbb_price'] = kbb_prices

# Drop rows where kbb_price is empty
cars = cars.dropna(subset=['kbb_price'])

# Compare the actual market price with the dataset using absolute difference
cars['price_difference'] = np.abs(cars['price'] - cars['kbb_price'].astype(float))

# Print the results
#print(cars[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference']])

# Flag rows with price difference greater than 10000 as fraudulent
cars['fraudulent'] = np.where(cars['price_difference'] > 10000, True, False)




# %%
# Visualize the comparison
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(data=cars, x='manufacturer', y='price_difference', estimator=np.median, ax=ax).set(title='Median Price Difference by Manufacturer')
plt.xticks(rotation=45)
plt.show()

# Visualize the average fraudulent status on a separate plot
avg_fraudulent_status = cars.groupby('manufacturer')['fraudulent'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(data=avg_fraudulent_status, x='manufacturer', y='fraudulent', color='red').set(title='Average Fraudulent Status by Manufacturer')
plt.xticks(rotation=45)
plt.show()

# %%
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Split the dataset into features (X) and target variable (y)
X = cars[['manufacturer', 'model', 'year', 'odometer']]
y = cars['fraudulent']

# Convert categorical variables to numerical using one-hot encoding
X_encoded = pd.get_dummies(X, drop_first=True)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train the Random Forest Classifier model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))


# %%
from sklearn.dummy import DummyClassifier

# Create and train the baseline model (predicts the most frequent class)
baseline_model = DummyClassifier(strategy='most_frequent')
baseline_model.fit(X_train, y_train)

# Evaluate the baseline model
baseline_accuracy = baseline_model.score(X_test, y_test)
print("Baseline Model Accuracy:", baseline_accuracy)

# Evaluate the RandomForestClassifier model
model_accuracy = model.score(X_test, y_test)
print("RandomForestClassifier Model Accuracy:", model_accuracy)

# Compare the performance of the models
if model_accuracy >= baseline_accuracy:
    print("RandomForestClassifier model outperforms the baseline model.")
else:
    print("RandomForestClassifier model does not outperform the baseline model.")


# %%
from sklearn.svm import SVC

# Initialize the SVM classifier
svm_model = SVC(kernel='rbf', random_state=42)  # You can experiment with different kernel types (e.g., 'rbf', 'linear', 'poly')

# Train the SVM model
svm_model.fit(X_train, y_train)

# Make predictions on the test set
svm_predictions = svm_model.predict(X_test)

# Evaluate the SVM model
svm_accuracy = accuracy_score(y_test, svm_predictions)
print("SVM Model Accuracy:", svm_accuracy)

# Print classification report
svm_classification_report = classification_report(y_test, svm_predictions)
print("Classification Report:")
print(svm_classification_report)


# %%
from sklearn.ensemble import GradientBoostingClassifier

# Initialize the Gradient Boosting Classifier
gb_model = GradientBoostingClassifier(random_state=42)

# Train the Gradient Boosting model
gb_model.fit(X_train, y_train)

# Make predictions on the test set
gb_predictions = gb_model.predict(X_test)

# Evaluate the Gradient Boosting model
gb_accuracy = accuracy_score(y_test, gb_predictions)
print("Gradient Boosting Model Accuracy:", gb_accuracy)

# Print classification report
gb_classification_report = classification_report(y_test, gb_predictions)
print("Classification Report:")
print(gb_classification_report)


# %%
# Define risk levels based on the magnitude of price difference
def categorize_risk(price_difference):
    if price_difference < 5000:
        return 'Low Risk'
    elif price_difference < 10000 and price_difference > 5001:
        return 'Moderate Risk'
    else:
        return 'High Risk'

# Apply the categorize_risk function to create a new column 'risk_level'
cars['risk_level'] = cars['price_difference'].apply(categorize_risk)

# View the DataFrame with the new 'risk_level' column
#print(cars[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference', 'risk_level']])

# Print the results
output_df = cars[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference', 'risk_level']]
print(output_df)

# Save the results to a CSV file
output_csv_filename = 'price_comparison_results.csv'
output_df.to_csv(output_csv_filename, index=False)
print(f'Results have been saved to {output_csv_filename}')

# %%
# Create a new column 'model_frequency' to represent the frequency of each model
cars['model_frequency'] = cars['model'].map(cars['model'].value_counts())

# Iterate through each row in the DataFrame
for index, row in cars.iterrows():
    manufacturer = row['manufacturer']
    model = row['model']
    frequency = row['model_frequency']

# Extract the first four letters of each model
cars['model_short'] = cars['model'].str[:4]

# Create a bar plot for the frequency of each scraped vehicle with wider bars
plt.figure(figsize=(18, 6))  # Increase the figure width
sns.barplot(data=cars, x='model_short', y='model_frequency').set(title='Frequency of Scraped Vehicles')
plt.xticks(rotation=90, ha='right')  # Rotate the labels for better visibility
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()




# %% [markdown]
# THEFT LIKELIHOOD

# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from fuzzywuzzy import fuzz
import Levenshtein


# Step 1: Load the datasets
car_df = cars
car_df['make_model'] = car_df['manufacturer'] + ' ' + car_df['model']

# Load the dataset containing the Top 10 Most Frequently Stolen Vehicles
top10theft = {
    "Rank": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Model": ["Chevrolet Full Size Pick-up", "Ford Full Size Pick-up", "Honda Civic", "Honda Accord", "Hyundai Sonata",
              "Hyundai Elantra", "Kia Optima", "Toyota Camry", "GMC Full Size Pick-up", "Honda CR-V"],
    "Thefts": [49.903, 48.175, 27.113, 27.089, 21.707, 19.602, 18.221, 17.094, 16.622, 13.832],
    "year": [2004, 2006, 2000, 1997, 2013, 2017, 2015, 2021, 2005, 2001]
}

top10theft = pd.DataFrame(top10theft)

# Function to calculate similarity between strings using fuzzywuzzy
def calculate_similarity(str1, str2):
    return fuzz.token_sort_ratio(str1, str2)

# Function to compare models and years and assign theft occurrences
def assign_theft_occurrences(row):
    for index, theft_row in top10theft.iterrows():
        # Check if model and year are similar
        similarity = calculate_similarity(row["make_model"], theft_row["Model"])
        if similarity >= 80 and abs(row["year"] - theft_row["year"]) <= 5:
            return theft_row["Thefts"]
    # If vehicle not in top 10 list, assign a reasonable number
    return 1000


# Apply the function to assign theft occurrences
car_df["theft_occurrences"] = car_df.apply(assign_theft_occurrences, axis=1)

# Step 2: Preprocess the data (if needed)
# Drop columns that are not needed for modeling
car_df = car_df.drop(columns=['source', 'title','location', 'kbb_price', 'price_difference', 'fraudulent', 'risk_level', 'model_frequency', 'model_short', 'high_risk'])
print(car_df)



# One-hot encode categorical variables if needed
car_df = pd.get_dummies(car_df, columns=['manufacturer', 'model'])

# Step 3: Split the data into features and target variable
X = car_df.drop(['theft_occurrences', 'make_model'], axis=1)
y = car_df['theft_occurrences']

# Print unique theft_occurrences values and their corresponding make_model and thefts
unique_theft_occurrences = car_df['theft_occurrences'].unique()
for theft_occurrence in unique_theft_occurrences:
    print(f"Theft Occurrence: {theft_occurrence}")
    print("Make Model and Thefts:")
    matched_make_models = car_df.loc[car_df['theft_occurrences'] == theft_occurrence, 'make_model'].unique()
    for make_model in matched_make_models:
        # Find the corresponding thefts value from top10theft
        top10_row = top10theft[top10theft['Model'].str.lower().str.startswith(make_model[:3])]
        if not top10_row.empty:
            thefts_value = top10_row.iloc[0]['Thefts']
            print(f"Make Model: {make_model}, Thefts: {thefts_value}")
    print()

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Impute missing values in y_train and y_test
imputer = SimpleImputer(strategy='mean')
y_train_imputed = imputer.fit_transform(y_train.values.reshape(-1, 1)).ravel()
y_test_imputed = imputer.transform(y_test.values.reshape(-1, 1)).ravel()

# Step 6: Train the machine learning model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train_imputed)

# Step 7: Make predictions
y_pred = model.predict(X_test)

# Step 8: Evaluate the model
mse = mean_squared_error(y_test_imputed, y_pred)
print("Mean Squared Error:", mse)

# Example of predicting theft rate for new data
# Assuming 'new_data_features' contains features of new vehicles
new_data_features = X_test.head(9)  # Use the first row of the test set as an example
new_data_theft_rate = model.predict(new_data_features)
print("Predicted theft rate for new data:", new_data_theft_rate)

# %%

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Gradient Boosting Regressor model
model = GradientBoostingRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)


# Visualize the feature importances
feature_importances = model.feature_importances_
sorted_indices = np.argsort(feature_importances)[::-1]
sorted_features = X.columns[sorted_indices]
sorted_importances = feature_importances[sorted_indices]

plt.figure(figsize=(10, 6))
sns.barplot(x=sorted_importances, y=sorted_features, orient='h')
plt.xlabel('Feature Importance')
plt.ylabel('Feature')
plt.title('Gradient Boosting Regressor - Feature Importances')
plt.show()


# %%

def get_theft_rate(make, model):
    # URL for the NHTSA theft rates website
    url = 'https://www.nhtsa.gov/road-safety/vehicle-theft-prevention/theft-rates'

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

         # Find the form_build_id input element
        form_build_id_element = soup.find('input', {'id': 'edit-submit-vehicle-theft-data--FvUDqy1mAxQ'})

        # Check if the element is found before accessing its attributes
        if form_build_id_element:
            build_id = form_build_id_element.get('value')
        else:
            print("Error: form_build_id not found on the page.")
            return None

        # Prepare the payload with make and model from the dataset
        payload = {
            'make_tid': make,
            'model_tid': model,
            'form_build_id': build_id,
            'form_id': 'vehicle_theft_data',
            'op': 'Submit',
        }

        # Extract the form action URL
        form_action = 'https://www.nhtsa.gov' + soup.find('form', {'id': 'views-exposed-form-vehicle-theft-data-page-1'})['action']

        # Send a POST request with the payload to get the theft rates
        response = requests.post(form_action, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the response
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the theft rates (modify this based on the actual structure of the page)
            theft_rate = soup.find('td', {'headers': 'view-field-theft-rate-table-column--jHg96wYo01s'}).get_text(strip=True)

            return theft_rate
        else:
            print(f"Error in POST request: {response.status_code}")
    else:
        print(f"Error in GET request: {response.status_code}")

    return None

# Iterate through each row in the DataFrame
for index, row in cars.iterrows():
    make = row['manufacturer']
    model = row['model']
    theft_rate = get_theft_rate(make, model)

    if theft_rate is not None:
        print(f"Theft rate for {make} {model}: {theft_rate}")
    else:
        print(f"Failed to retrieve theft rate for {make} {model}")




