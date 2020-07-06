# Find Favorite Places Along your Route using TomTom Maps

<br>

## Overview

Finding the closest cafe while you are going to an interview will directly impact the interview outcome. Doing so will make you reach your destination on time and be respectful of interviewers' time. In addition, getting the caffeine that you need it to have full focus during the interview.

---
<br>

## Solution Structure:

Google Maps was the favorite and almost the single geolocation services worldwide for a long time.
Especially for developers, Google Maps API has for years been the go-to choice, but their expansive database of geographical changes this fact and pushed them for looking for cheaper alternatives provide the same services.

For this app, I've found several viable alternatives to Google Maps API to get geolocation data, such as TomTom, Mapfit, OpenLayers, HERE and Mapbox

You can find quick comparison among them in this article [5 Powerful Alternatives to Google Maps API](https://nordicapis.com/5-powerful-alternatives-to-google-maps-api/)

**Here we are going to use [TomTom api ](https://developer.tomtom.com/)**


> TomTom API main features:
>  - Pretty Maps.
>  - Good satellite navigation.
>  - Provide good functionality such as display maps, locations search, traffic density and route finding
>  - Price:
>    1. Free for 2,500 requests daily.
>    2. $0.42–$0.50 for each subsequent 1,000

Using TomTom maps we will provide app's users a pretty map that shows his current location. By providing the desired place category ex: cafe, car wash, etc. and destination location, the app will show all possible options for the selected category along his way.

---
<br>

## App Components / Services Types:
In this project, we will implement and provide following services:
1. App languages:
  - Arabic
  - English

<p align="center">
  <img src="assets/lang.png" width="50%">
</p>
<br>


2. Main map shows current user's location and provides clicking feature on anywhere on map to get Longitude and Latitude.

![Map](assets/map.png)

<br>


3. Place category: You can choose the place category that you are looking for along your way.

> List of categories we cover in our app:
  >- Café
  >- Restaurant
  > - Fast Food
  > - Market
  > - Bakery
  > - Grocery Store
  > - Bank
  >- ATM
  >- Gas Station
  >- Hospital
  >- Car Wash		
  >- Post Office		
  >- Hotel	School
  >- Clothing Shop		
  >- Mosque


<p align="center">
  <img src="assets/category_ar.png" width="40%" style="border-width=2px;border-color=black; border-style:solid;">   <img src="assets/category_en.png" width="40%">
</p>

<br>


4. Find destination using Location (Latitude/Longitude): Using this service, you can find the shortest route to your destination by providing Location's latitude and longitude.


<p align="center">
  <img src="assets/lat_lon_ar.png" width="40%" style="border-width=2px;border-color=black; border-style:solid;">   <img src="assets/lat_lon_en.png" width="40%">
</p>
<br>



5. Find destination using Area Name: Using this service, you can find the shortest route to your destination by providing Area name.


<p align="center">
  <img src="assets/area.png" width="40%">
</p>
<br>



6. Max Detour time: After sepcfy both start and destination points, the app calculated the shortest route between them and highlight all possible places that belong to selected category with max detour time 3 minuits (this defualt value for detour time then you can change custmize to different value )


<p align="center">
  <img src="assets/detour_time_ar.png" width="40%" style="border-width=2px;border-color=black; border-style:solid;">   <img src="assets/detour_time_en.png" width="40%">
</p>
<br>



7. Result section:


<p align="center">
  <img src="assets/route_ar.png" width="40%" style="border-width=2px;border-color=black; border-style:solid;">   <img src="assets/route_en.png" width="40%">
</p>
<br>




By activating `yala` checkbox, the app will show the following information:

- Map section:
  - Home point (blue marker)
  - Destination point (red marker)
  - The shortest route between both points
  - (Rest of markers) that represent places belong to the selected category and these markers have the following features:
    - Each place marker has a number indicate the order of the place based on its detour time.
        - ex: the place with the shortest derout time will have number 1 then the second shortest place will have number 2 and so on.
    - Each place marker has a different color and size, they represent the place derout time
        - ex: the place with the shortest derout time will have the darkest color and bigger marker then the second shortest place be a little bit lighter and smaller and so on.
    - Each place has 2 popup windows:
        1. Popup window that showup when pressing on the marker to give you location's information (name, full address) .
        2. Popup window that showup when hovering over the marker to give you location's name and derout time.

![Alt Text](assets/res_map.png)

- Side section: The app will show some information about the calculated route to the destination:
  - The time you need to reach your destination.
  - Estimated distance.
  - Estimated arrival time


  <p align="center">
    <img src="assets/res_side_ar.png" width="40%" style="border-width=2px;border-color=black; border-style:solid;">   <img src="assets/res_side_en.png" width="40%">
  </p>
<br>


---

### Prerequisites
The requirements.txt file contains any Python dependencies. You can install them by running this command:

```
pip3 install -r requirements.txt
```

### Built With

- [TomTom API](https://developer.tomtom.com/) - Cross platform REST APIs and SDKs provide geographical data.
- [Streamlit](https://docs.streamlit.io/en/stable/#:~:text=Streamlit%20is%20an%20open%2Dsource,with%20streamlit%20run%20%5Bfilename%5D%20.) - Open-source Python library that makes it easy to build beautiful custom web-apps for machine learning and data science.
- [Folium](https://python-visualization.github.io/folium/) - Open-source library to visualize data that’s been manipulated in Python on an interactive leaflet map.


### How Run The Services
1. Run command on prerequisites section above.
2. Run streamlit script:
```
streamlit run https://github.com/EsraaMadi/Map_locations_finder_along_route/blob/master/streamlit_app.py
```




### Services Demo

- **Finding destination using Location (Latitude/Longitude):**

![Alt Text](code/flask-app/static/images/app-demo1.gif)

- **Finding destination using Area Name**

![Alt Text](code/flask-app/static/images/app-demo2.gif)
