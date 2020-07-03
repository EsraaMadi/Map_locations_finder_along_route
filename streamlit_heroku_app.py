import folium
from folium.plugins import BeautifyIcon
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import pickle
import json
from colour import Color
import os
from IPython.display import display
#----------------------------------------------------------------------------#

### Define some paramters ###

# load saudi regions (En / AR)
with open('help_files/sa_regions.pkl', 'rb') as f:
    sa_regions_dict = pickle.load(f)


#  TomTom API key Setting
api_key = os.environ.get('tomtomapikey')

# places category 
# load saudi regions (En / AR)
with open('help_files/categories.pkl', 'rb') as f:
    places_cat_dict = pickle.load(f)
places_cat_en = list(places_cat_dict.name.values)
places_cat_ar  = list(places_cat_dict.name_ar.values)


# app languages
languages_lst = ["En", "العربية"]

# app text dict
app_text_dict = {
    'app_title':{ 0 : "Grab your :coffee: on your way :car: ",
                  1 : ':car: خذ قهوتك :coffee: بطريقك'},
    'sub_app_title':{ 0 : "Your Live Location/Area :world_map:",
                      1 : ': :world_map: مكانك الحين'},
    'home_loc_title' : { 0 : "Your Current Location:",
                         1 : ':مكانك'},
    'home_lat_title' : { 0 : "Is this your latitude?",
                         1 : 'خط العرض؟'},
    'home_lon_title' : { 0 : "Is this your longitude?",
                         1 : 'خط الطول؟'},
    'home_show_title' : { 0 : 'Show your location on the map?',
                          1 : 'ويني على الخريطة؟'},
    'home_map_title' : { 0 : 'Your location',
                         1 : '! انت'},
    'dest_cat_title' : { 0 : "You need All ... in your way:",
                         1 : 'تحتاج كل ال.... الي بطريقك'},
    'dest_cat' : { 0 : places_cat_en ,
                   1 : places_cat_ar },
    'dest_loc_title' : { 0 : "Where are you going?",
                         1 : 'وين رايح طال عمرك؟'},
    'dest_options_lst' : { 0 : ["Using Location (Latitude/Longitude)", "Using Area Name"],
                           1 : ["استخدام موقع محدد (خط الطول/خط العرض)", "استخدام اسم الحي"]},
    'dest_regions' : { 0 : [reg[0] for id, reg in sa_regions_dict.items()],
                       1 : [reg[1] for id, reg in sa_regions_dict.items()]},
    'dest_area_title' : { 0 : 'Area/Street Name',
                          1 : 'اسم الحي/الشارع'},
    'dest_lat_title' : { 0 : "Latitude?",
                         1 : 'خط العرض؟'},
    'dest_lon_title' : { 0 : "Longitude?",
                         1 : 'خط الطول؟'},
    'dest_show_title' : { 0 : 'Show your destination on the map?',
                          1 : 'وين رايح على الخريطة؟'},
    'dest_map_title' : { 0 : "your destination",
                         1 : '! وجهتك '},
    'route_show_title' : { 0 : "Show your Route on the map?",
                           1 : '! ورني طريقي على الخريطة'},
    'yala_title' : { 0 : 'yala!',
                     1 : '! يلا'},
    'trip_time_title' : { 0 : 'Needed Time to arraive your destination is ',
                          1 : '  لتصل لوجهتك تحتاج ل'},
    'minute_title' : { 0 : '  minutes',
                       1 : ' دقائق  '},
    'hour_title' : { 0 : '  hours',
                     1 : ' ساعات  '},
    'trip_dist_title' : { 0 : 'Estimated Distance is ',
                          1 : '   المسافة المقدرة  '},
    'km_title' : { 0 : ' Km',
                          1 : ' كم   '},
    'arrival_time_title' : { 0 : 'Estimated Arraival time is ',
                             1 : ' وقت الوصول المتوقع'},
    'derout_time_title' : { 0 : 'Max Detour Time (minutes):',
                            1 : 'اقصى وقت انعطاف (بالدقائق)'}
          
}



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
    folium.LatLngPopup().add_to(TomTom_map)
    
    return TomTom_map

def add_marker_map(tomtom_map, marker_latitude, marker_longitude, marker_title='point', marker_color='green', is_home=True):
    """
    A function to add a point marker at any TomTom map
    """
    if is_home:
        icon_ = 'glyphicon glyphicon-chevron-up'
    else:
        icon_ = 'glyphicon glyphicon-chevron-down'
        
    folium.Marker(location=( marker_latitude, marker_longitude),
                  popup=marker_title, 
                  icon=folium.Icon(color=marker_color, icon=icon_)
             ).add_to(tomtom_map)
    
    return tomtom_map

@st.cache(hash_funcs={st.DeltaGenerator.DeltaGenerator: lambda _: None})
def get_my_location(weights_warning, progress_bar):
    """
    A function to get my latitude, longitude, region code and city name
    """
    
    api_key_loc = os.environ.get('ipstackkey')
    
    # step 1: get my ip 
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']

    # increase progress bar 
    progress_bar.progress(0.5)
    weights_warning.warning("Downloading %s......" % 'Map of your Area')
    
    # step 2: get my loc
    geo_request = requests.get(f"http://api.ipstack.com/{my_ip}?access_key={api_key_loc}")
    geo_data = geo_request.json()
    
    return [float(geo_data['latitude']), float(geo_data['longitude'])], geo_data['region_code'], geo_data['city']

#@st.cache(suppress_st_warning=True, hash_funcs={folium.Map: hash})
def draw_route(points):
    """Function to draw a route between two points using folium"""
    
#     # get center of our map based on obtained route
#     ave_lat = sum(float(p[0]) for p in points)/len(points)
#     ave_long = sum(float(p[1]) for p in points)/len(points)
    
    lat_avg, long_avg, zoom_avg = get_map_center_zoom(float(points[0][0]), float(points[0][1]), float(points[-1][0]), float(points[-1][1]))
    
    # initlize a map 
    TomTom_map = init_map(api_key, latitude=lat_avg, longitude=long_avg, zoom=zoom_avg)

    #add a markers for home and destination points
    TomTom_map = add_marker_map(TomTom_map, points[0][0], points[0][1], marker_title='Your location', marker_color='blue', is_home=True)
    TomTom_map = add_marker_map(TomTom_map, points[-1][0], points[-1][1], marker_title='Your destination point', marker_color='red', is_home=False)


    # add lines 
    folium.PolyLine(points, color="green", weight=2.5, opacity=1).add_to(TomTom_map)

    return TomTom_map

@st.cache(suppress_st_warning=True, hash_funcs={folium.Map: hash})
def find_short_route(home_latitude, home_longitude, dest_latitude, dest_longitude):
    """Function to find the shortest route between 2 points"""
    
    # Make the Request
    r = requests.get(f"https://api.tomtom.com/routing/1/calculateRoute/{home_latitude},{home_longitude}:{dest_latitude},{dest_longitude}/xml?avoid=unpavedRoads&key={api_key}")
    
    # check response status to make sure it went through
    if r.status_code == 200:
        
        # Turn the XML data into a human readable format
        soup = BeautifulSoup(r.content, "lxml")
        
        # get Estimated travel time
        time_tot_sec = float(soup.find('summary').find('traveltimeinseconds').text)
        time_h = int(time_tot_sec / (60*60))
        time_m = int((time_tot_sec % (60*60)) /60)

        # get distance
        distance = float(soup.find('summary').find('lengthinmeters').text)/1000
        
        # get EAT
        eta = soup.find('summary').find('arrivaltime').text.split('T')
        eta_date = eta[0]
        eta_time = eta[1].split('+')[0]

        # Find all the tags that contain a point in our route
        points = soup.find_all('point')
        
        # clean points list 
        points = [tuple([float(point['latitude']), float(point['longitude'])]) for point in points ]
        
        #drow map
        tomtom_map = draw_route(points)
        
        return time_h, time_m, distance, eta_date, eta_time, tomtom_map, points
    else:
        st.error('This is an error') # i need to handel this

@st.cache(suppress_st_warning=True)
def get_map_center_zoom(home_latitude, home_longitude, dest_latitude, dest_longitude):
    """Function to get center of folium map and zoom used"""
    # get center of our map based on home and destination points
    ave_lat = (home_latitude + dest_latitude) / 2
    ave_long = (home_longitude + dest_longitude) /2
    
    # calculate map zoom
    zoom = 14 #defuelt zoom
    latitude_diff = abs(home_latitude - dest_latitude)
    longitude_diff = abs(home_longitude - dest_longitude)
    
    if latitude_diff > longitude_diff:
        while latitude_diff > 0:
            zoom = zoom -1
            latitude_diff = latitude_diff - 0.1
    else:
        while longitude_diff > 0:
            zoom = zoom -1
            longitude_diff = longitude_diff - 0.1
    return ave_lat, ave_long, zoom


def SearchCity(city, country):
    """ Function use Geocoding feature in Search API to get lat/lon of the center of a city or area"""
    
    url = f'https://api.tomtom.com/search/2/search/{city},{country}.json?limit=1&idxSet=Geo&key={api_key}'
    result = requests.get(url).json()
    
    GeoID = result['results'][0]['dataSources']['geometry']['id']
    position = result['results'][0]['position']
    
    return GeoID,position

@st.cache()
def getPolygon(city, country, zoomLevel):
    """ Function to get polygon of a given GeoID"""
    
    # get GeoID for region
    GeoID, position = SearchCity(city, country)
    
    url = f'https://api.tomtom.com/search/2/additionalData.json?geometries={GeoID}&geometriesZoom={zoomLevel}&key={api_key}'
    result = requests.get(url).json()
    
    GeoJson = result['additionalData'][0]['geometryData']
    
    return GeoJson, position['lat'], position['lon']

#@st.cache()
def get_cafes_around_point(dest_latitude, dest_longitude, search_limit, search_radius, category):
    """Function to retrieve cafes around given point"""

    # Gather all paramters in dict
    params_ = {'countrySet' : 'SA',
               'lat' : dest_latitude,
               'lon' : dest_longitude,
               'limit' : search_limit,
               'radius' : search_radius,
               'key' : api_key
              }
    # create a request 
    url = (f'https://api.tomtom.com/search/2/categorySearch/{category}.json')
    r = requests.get(url, params=params_)
    
    # check response status to make sure it went through
    if r.status_code == 200:
        result = r.json()
    return result 

def get_route_points(points, num_points):
    """Function returns distributed selected number of points along route (array of points)"""
    
    # calculate step between each 2 points
    step = len(points)// (num_points + 2) # num_points +1 for start point +1 for end points
    
    # return points
    return [{'lat':points[step * i][0], 'lon':points[step * i][1]} for i in range(1,num_points+1)]

def get_cafes_along_route(api_points, detour_time, res_limit, place_category, lang_ind, place_brand=None):
    """Function to retrieve cafes spread over given route"""
    
    if lang_ind:
        ind = places_cat_ar.index(place_category)
        place_category = places_cat_en[ind]
        
    places_cat_id = places_cat_dict[places_cat_dict['name']== place_category]['id']
    # Gather all paramters in dict
    params_ = {'maxDetourTime' : detour_time,
               'detourOffset' : json.dumps(True),
               'limit' : res_limit,
               'categorySet' : places_cat_id,
               'key': api_key
              } 
    # add place brand if it's provided
    if place_brand:
        params_['brandSet'] = place_brand
            
    # create a request
    headers = {'Content-type': 'application/json'}
    response = requests.post(f'https://api.tomtom.com/search/2/searchAlongRoute/{place_category}.json',
                             json=api_points,
                             headers=headers,
                             params=params_)
    
    # check response status to make sure it went through
    if response.status_code == 200:
        res = json.loads(response.text) 
    return res 

def convert_sec_to_h_m(sec, hours=True ):
    """Function to convert sec to corresponding hours and minates or minates"""
    if hours:
        time_h = int(sec / (60*60))
        time_m = int((sec % (60*60)) /60)
    else:
        time_h = 0
        time_m = int(sec / 60)
    return time_h, time_m  

def draw_along_search_map(res, points, max_res_limit):
    """Function to draw returned result of along_search service on map"""
    
    # draw home, destination, shortest route between them
    tomtom_map = draw_route(points)

    # create heat colors scale for markers to show Priority of the place
    # we chose here blue gradients
    colors = list(Color("#000080").range_to(Color("#d5e5ff"),max_res_limit))

    # for each returened place
    for ind, poi in enumerate(res['results']):

        # calculate detour time for this place in minutes 
        detour_h, detour_min = convert_sec_to_h_m(poi['detourTime'], False)

        #print(poi['detourTime'])
        # create marker on the place has own size and color
        icon_ = BeautifyIcon(icon_shape='marker',
                             number=ind+1,
                             spin=True,
                             text_color='gray',
                             icon_size=(40-ind, 40-ind),
                             border_color =str(colors[ind]),
                             background_color=str(colors[ind]),
                             inner_icon_style="font-size:12px;padding-top:-5px;"
                            )

        # add a marker for each lat, lon
        folium.Marker(location=tuple(poi['position'].values()),
                      popup=folium.Popup(f"<b>{poi['poi']['name']}</b> <br>{poi.get('address').get('streetName','')}, {poi['address']['municipalitySubdivision']}", max_width=100) , 
                      icon=icon_,
                      tooltip=f"<b>{poi['poi']['name']}</b> <br> ({detour_min} mins)"
                 ).add_to(tomtom_map)
    return tomtom_map

#----------------------------------------------------------------------------#

### Define main function ###
def main():
    
    # select language
    lang_radio = st.sidebar.radio(label="", options=languages_lst)
    lang_ind = languages_lst.index(lang_radio)

    
    # Progress bar for loading map
    weights_warning, progress_bar = None, None
        

    # add some titles
    st.header(app_text_dict['app_title'][lang_ind])
    st.subheader(app_text_dict['sub_app_title'][lang_ind])

    # add progress bar for loading map
    weights_warning = st.warning("Detecting %s..." % 'your location')
    progress_bar = st.progress(0)
    progress_bar.progress(.1)

    # get your location and update progress bar
    my_location, my_region_code, my_region = get_my_location(weights_warning, progress_bar)

    # initialize a map and update progress bar
    map_ = init_map(latitude=my_location[0], longitude=my_location[1], layer = "hybrid")
    progress_bar.progress(.8)
    map_box = st.markdown(map_._repr_html_(), unsafe_allow_html=True)

    # remove progress bar
    weights_warning.empty()
    progress_bar.empty()

    ## sidebar ##
    # show current latitude and longitude 
    st.sidebar.title(app_text_dict['home_loc_title'][lang_ind])
    lat_home = st.sidebar.number_input(label=app_text_dict['home_lat_title'][lang_ind], value=my_location[0], format='%f')
    long_home = st.sidebar.number_input(label=app_text_dict['home_lon_title'][lang_ind], value=my_location[1], format='%f')
    
    # show the current location on the map 
    if st.sidebar.checkbox(app_text_dict['home_show_title'][lang_ind]):
        map_box.empty()
        map_ = add_marker_map(map_, lat_home, long_home, app_text_dict['home_map_title'][lang_ind], 'green', is_home=True)
        map_box = st.markdown(map_._repr_html_(), unsafe_allow_html=True)

    st.sidebar.title(app_text_dict['dest_cat_title'][lang_ind])
    place = st.sidebar.selectbox('', app_text_dict['dest_cat'][lang_ind])
    #brand = st.sidebar.text_input('Any specific brand (optional)?')
    # destination section
    st.sidebar.title(app_text_dict['dest_loc_title'][lang_ind])
    
    if lang_ind == 0 : # for english lang only 
        dest_radio = st.sidebar.radio(label="", options=app_text_dict['dest_options_lst'][lang_ind])


     
    # use destination latitude and longitude
    if lang_ind == 1 or dest_radio == app_text_dict['dest_options_lst'][lang_ind][0]:
        lat_dest = st.sidebar.number_input(label=app_text_dict['dest_lat_title'][lang_ind], format='%f')
        long_dest = st.sidebar.number_input(label=app_text_dict['dest_lon_title'][lang_ind], format='%f')

        # show destination location on the map
        if st.sidebar.checkbox(app_text_dict['dest_show_title'][lang_ind]):
            map_box.empty()
            lat_avg, long_avg, zoom_avg = get_map_center_zoom(lat_home, long_home, lat_dest, long_dest)
            map_ = init_map(latitude=lat_avg, longitude=long_avg, zoom=zoom_avg, layer = "hybrid")
            map_ = add_marker_map(map_, lat_home, long_home, app_text_dict['home_map_title'][lang_ind], 'green', is_home=True)
            map_ = add_marker_map(map_, lat_dest, long_dest, app_text_dict['dest_map_title'][lang_ind], 'red', is_home=False)
            map_box = st.markdown(map_._repr_html_(), unsafe_allow_html=True)

        # show route between current and destination point on the map
        st.sidebar.title(app_text_dict['route_show_title'][lang_ind])
        if st.sidebar.checkbox(app_text_dict['yala_title'][lang_ind]):
            # maximum detour time limit (sec)
            max_detour_time = (st.sidebar.slider(app_text_dict['derout_time_title'][lang_ind], min_value=0, max_value=60, value=3)) * 60
            map_box.empty()
            # while waiting route calculation 
            with st.spinner('Finding the best Route....'):
                time_h, time_m, distance, eta_date, eta_time, map_, points= find_short_route(lat_home, long_home, lat_dest, long_dest)
                map_box = st.markdown(map_._repr_html_(), unsafe_allow_html=True)

            # show some celebration :D
            st.sidebar.balloons()

            # show route information  
            # needed time
            if time_h > 0 :
                st.sidebar.success(app_text_dict['trip_time_title'][lang_ind] + str(time_h) + \
                                   app_text_dict['hour_title'][lang_ind] + str(time_m) + \
                                   app_text_dict['minute_title'][lang_ind])
            else:
                st.sidebar.success(app_text_dict['trip_time_title'][lang_ind] + str(time_m) + \
                                   app_text_dict['minute_title'][lang_ind])
            # needed distance
            st.sidebar.info(app_text_dict['trip_dist_title'][lang_ind] + str(distance) + app_text_dict['km_title'][lang_ind])
            # etimated arrival time 
            st.sidebar.info(app_text_dict['arrival_time_title'][lang_ind])
            st.sidebar.markdown(f'<p style="color:red;text-align:center">{eta_time}  &#128339<p>', unsafe_allow_html=True)
            
            # route points points[0][0], points[0][1],
            route_dict={"points": [{"lat": points[0][0], "lon": points[0][1]}] #start point
                        + get_route_points(points, 4) # 4 middle points
                        + [{"lat": points[-1][0],"lon": points[-1][1]}] # end point
                       }
            api_points = {"route":route_dict}
            # place category 
            category = 'cafe'
            # maximum number of responses that will be returned.
            max_res_limit = 20
            # return calculation of the distance between the start of the route and the starting point of the detour to a POI.
            detour_offset = True
            
            res = get_cafes_along_route(api_points, max_detour_time, max_res_limit, place, lang_ind )
            
            map_box.empty()
            map_ = draw_along_search_map(res, points, max_res_limit)
            map_box = st.markdown(map_._repr_html_(), unsafe_allow_html=True)
            
            
   
        
    # use area name as destination
    elif dest_radio == app_text_dict['dest_options_lst'][lang_ind][1]:

        # show list of KSA cities with your city as default choise
        my_city_info = sa_regions_dict.get(my_region_code, 0)
        if my_city_info: 
            resion_index = app_text_dict['dest_regions'][lang_ind].index(my_city_info[lang_ind])
        else:
            resion_index = 0
        my_city = st.sidebar.selectbox('', app_text_dict['dest_regions'][lang_ind], resion_index)

        # enter area name or street name
        area_name = st.sidebar.text_input(app_text_dict['dest_area_title'][lang_ind])

        if area_name:
            # get lon and lat of the area
            Polygon, lat_area, lon_area = getPolygon(area_name, my_city, 22)

            # maximum number of responses (POI) that will be returned (1-100)
            search_limit = 100 

            # The results will be constrained to the defined area (radius) in meters.
            search_radius = 500

            # request all palaces in this area matches the selected category
            result = get_cafes_around_point(lat_area, lon_area, search_limit, search_radius, place)

            #draw map
            map_box.empty()
            lat_avg, long_avg, zoom_avg = get_map_center_zoom(lat_home, long_home, lat_area, lon_area)
            map_ = init_map(latitude=lat_avg, longitude=long_avg, zoom=zoom_avg-1, layer = "hybrid")
            map_ = add_marker_map(map_, lat_home, long_home, "your Location", 'green', is_home=True)
            # add polygons to a map
            folium.GeoJson(Polygon).add_to(map_)
            # Add POIs one by one to the map
            for poi in result['results']:
                folium.Marker(location=tuple(poi['position'].values()),
                              popup=str(poi['poi']['name']), 
                              icon=folium.Icon(color='green', icon='glyphicon-star')
                              #icon=icon
                         ).add_to(map_)
            map_box = st.markdown(map_._repr_html_(), unsafe_allow_html=True)

#----------------------------------------------------------------------------#

### run main function ###
if __name__ == "__main__":
    main()
