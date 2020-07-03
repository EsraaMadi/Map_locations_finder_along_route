import folium
from folium.plugins import BeautifyIcon
import streamlit as st
import requests
import pandas as pd
import os
#----------------------------------------------------------------------------#

### Define some paramters ###




#  TomTom API key Setting
api_key = os.environ.get('tomtomapikey')


#----------------------------------------------------------------------------#

### Define some help functions ###
#@st.cache(suppress_st_warning=True, hash_funcs={folium.Map: lambda _: None})
def init_map(api_key=api_key, latitude=0, longitude=0, zoom=14, layer = "basic", style = "main"):
    """
    A function to initialize a clean TomTom map
    """
    
    maps_url = "http://{s}.api.tomtom.com/map/1/tile/"+layer+"/"+style+"/{z}/{x}/{y}.png?tileSize=512&key="
    TomTom_map = folium.Map(
        location = [latitude, longitude],  # on what coordinates [lat, lon] initialise the map
        zoom_start = zoom,
        tiles = str(maps_url + api_key),
        attr = 'TomTom')
    
    # add get latitude and longitude feature to our map
    #folium.LatLngPopup().add_to(TomTom_map)
    
    return TomTom_map

#----------------------------------------------------------------------------#

### Define main function ###
def main():
   

    # initialize a map and update progress bar
    map_ = init_map(latitude=39.043701171875, longitude=-77.47419738769531, layer = "hybrid")
    st.markdown(map_._repr_html_(), unsafe_allow_html=True)


#----------------------------------------------------------------------------#

### run main function ###
if __name__ == "__main__":
    main()
