"""
Created on Mon Dec 28 08:00:16 2020
@author: rwiyadi
"""
import segyio
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

name = input('Seismic line name:')
filename = ['folder'] + name + '.segy'

# Open SEGY file
with segyio.open(filename, ignore_geometry=True) as f:
    # Get all header keys:
    header_keys = segyio.tracefield.keys
    # Initialize df with trace id as index and headers as columns
    trace_headers = pd.DataFrame(index=range(1, f.tracecount+1),
                                 columns=header_keys.keys())
    # Fill dataframe with all trace headers values
    for k, v in header_keys.items():
        trace_headers[k] = f.attributes(v)[:]
print(trace_headers.head())

line_coord = trace_headers[['CDP_X', 'CDP_Y']]
line_coord.insert(1, 'LINE_NAME', name)

#Writer from Dataframe Pandas to Excel file (unnecessary repositoryy)
writer = pd.ExcelWriter([folder_location])
sheet_names = ['Sheet1']
line_coord.to_excel(writer, 'Sheet1', index=True)
writer.save()

#Shpaefile Properties
ESRI_WKT_49 = 'PROJCS["WGS_1984_UTM_Zone_49S",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",111],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",10000000],UNIT["Meter",1]]'
ESRI_WKT_50 = 'PROJCS["WGS_1984_UTM_Zone_50S",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",117],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",10000000],UNIT["Meter",1]]'

#Shapefile generation
line_gdf_50 = gpd.GeoDataFrame(line_coord, crs = "EPSG:32750", geometry = gpd.points_from_xy(line_coord['CDP_X'], line_coord['CDP_Y']))
line_gdf_50 = line_gdf_50.groupby(['LINE_NAME'])['geometry'].apply(lambda x: LineString(x.tolist()))
line_gdf_50 = gpd.GeoDataFrame(line_gdf_50)
line_gdf_50.to_file(filename= name + '.shp', driver= 'ESRI Shapefile', crs_wkt= ESRI_WKT_50)
