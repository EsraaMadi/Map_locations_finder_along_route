# Get your place in your way using TomTom maps Api

<br>

## Overview

Finding closest cafe while your going to your interview will impact directly your interview outcome, since it make you reach your distination on time and have your body needed caffine to be full focus during interview

<br>

## Solution Structure:
1. Preprocess the data to be in a format that could be provided for analyzer or indexer.
2. [Hotel tone analyzer](https://github.com/EsraaMadi/Hotel-tone-analyzer/blob/master/code/Hotel%20Analyzer.ipynb):
    - Use IBM Watson python lib to get tones for each review of hotels in our Datasets.
    - For each hotel, calculate the normalized score for the detected tones, aggregate them all and get a final score.
    - Show the final tones scores as a bar chart.
3. [Hotel indexer](https://github.com/EsraaMadi/Hotel-tone-analyzer/blob/master/code/Hotel%20Indexer.ipynb):
    - Create one document for each hotel that contains all hotel data plus obtained tones from IBM API.
    - Use Elasticsearch to index all documents from the previous step.
4. Provide the above two services as [web service](https://github.com/EsraaMadi/Hotel-tone-analyzer/tree/master/code/flask-app) using flask.


---
<br>

- Google Maps was always the favorite for its geolocation services worldwide. although  their expansive database of geographical changes the fact the Google Maps API has for years been the go-to choice for developers.(copy past)

- While looking for alternatives to Google Maps API, I’ve got many options for geolocation data such as: TomTom, Mapfit, OpenLayers, HERE and Mapbox

- You can find quick comparison among them in this article [5 Powerful Alternatives to Google Maps API](https://nordicapis.com/5-powerful-alternatives-to-google-maps-api/)

- For this tutorial, we are going to use TomTom api
#### [TomTom api ](https://developer.tomtom.com/)
TomTom features:
- Pretty Maps.
- Good satellite navigation.
- Provide good functionality such as display maps, locations search, traffic density and route finding
- Price: Free for 2,500 requests daily, $0.42–$0.50 for each subsequent 1,000


**Tone Analyzer** is a service determines the emotional tone behind a series of words, used to gain an understanding of the attitudes, opinions and emotions expressed within an online mention.


Here we going to use one of common emotional or sentiment analysis APIs **IBM Tone Analyzer** to analysis text reviews of 1,000 hotels and get the total emotional tones for a hotel

#### [IBM Tone Analyzer](https://www.ibm.com/watson/services/tone-analyzer/)
is one of the cognitive services provided by IBM Cloud. It can help us predict the emotions, tones and communication style of the text written by users (passed as input to the service).

To have an insight on the service and tones, try this [web interface](https://tone-analyzer-demo.ng.bluemix.net/).

---
<br>

## Components / Services Types:
In this project, we are going to implement and provide two services:
1. Hotel tone analyzer:
    - Using this service, you can pass a hotel name and get the normalized tone analysis for all its reviews. We cover these tones: anger, fear, joy, and sadness (emotional tones). analytical, confident, and tentative (language tones).
2. Hotel indexer:
    - By hitting this service, you can index all hotels data using Elasticsearch
---
<br>



## Datasets
The dataset used in this project is taken from this [Kaggle dataset](https://www.kaggle.com/datafiniti/hotel-reviews#7282_1.csv)

This dataset is a list of about 1,000 hotels and 30,000 reviews. The dataset includes hotel location, name, rating, review data, title, username, and more.

For more information about dataset columns, you can check this [data dictionary](https://developer.datafiniti.co/docs/business-data-schema)

----
<br>

### Prerequisites
The requirements.txt file contains any Python dependencies. You can install them by running this command:

```
pip3 install -r requirements.txt
```

### Built With

- [IBM Watson python lib](https://pypi.org/project/ibm-watson/) - Library to understand emotions and communication style in text.
- [Elasticsearch](https://www.elastic.co/products/elasticsearch) - Open-source, RESTful, distributed search and analytics engine
- [Flask](https://flask-doc.readthedocs.io/en/latest/)  - Web framework, a third-party Python library used for developing web applications.
- [Plotly](https://pypi.org/project/plotly/) - Open-source visualization libraries for R, Python, and JavaScript.

### How Run The Services
1. Clone repo
2. Run command on prerequisites section
3. Run `export FLASK_APP=app.py`
4. Run `flask run`



### Services Demo

- **Hotel Tone Analyzer**

![Alt Text](code/flask-app/static/images/app-demo1.gif)

- **Hotel Indexer**

![Alt Text](code/flask-app/static/images/app-demo2.gif)
