from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import math
import os
import json
import logging
from datetime import datetime
from bson import json_util
from tools.loader import MongoLoader as Database
from tools.aemet.meteorology import get_precipitation_and_temperature

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz

logging.basicConfig(level=logging.DEBUG)

load_dotenv('../env')

# NLTK setup for Spanish
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))
stemmer = SnowballStemmer('spanish')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_FLASK_KEY')
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = Database()

all_events = db.get_data()

def preprocess(text):
    # Tokenization and stemming
    words = word_tokenize(text)
    return [stemmer.stem(w) for w in words if w not in stop_words]

def search_events(all_events, search):
    processed_search = preprocess(search.lower())
    filtered_events = []

    for event in all_events:
        event_title = preprocess(event['title'].lower())
        for word in processed_search:
            if any(fuzz.ratio(word, title_word) > 80 for title_word in event_title):
                filtered_events.append(event)
                break

    return filtered_events

def get_events_from_questionary(user_latitude, user_longitude, user_response):
    best_events = []

    for event in all_events:
        ponderation = 0.0
        for category, response in user_response.items():
            if category != 'close':
                sub_category_value = event['subcategories'].get(category, 0.0) 
                sub_category_value = float(sub_category_value) * float(response)
                ponderation += sub_category_value
            if category == 'price':
                price = event['price'].replace('€', '')
                try:
                    price = float(price)
                except ValueError:
                    price = 0
                if price > 0:
                    # Make price 0 == 1, and price >= 100 == 0
                    price_pon = (100 - price) / 100 * float(response)
                    if price_pon > 1:
                        price_pon = 1
                    if price_pon < 0:
                        price_pon = 0
                    ponderation += price_pon


        # Save in order of best to worst in best event. Only save the best 15
        if len(best_events) < 15:
            best_events.append((event, ponderation))
            best_events.sort(key=lambda x: x[1], reverse=True)
        else:
            if ponderation > best_events[-1][1]:
                best_events[-1] = (event, ponderation)
                best_events.sort(key=lambda x: x[1], reverse=True)

    # Special cases:

    # Calculate distance to home, and ponderate it with 'close' response
    user_location = (user_latitude, user_longitude)
    new_best_events = []
    for event, score in best_events:
        event_location = (float(event['coordinates']['latitude']),
                          float(event['coordinates']['longitude']))

        # Haversine formula to calculate the distance between two points on the Earth
        lat1, lon1 = user_location
        lat2, lon2 = event_location

        lat1, lon1 = float(lat1), float(lon1)
        lat2, lon2 = float(lat2), float(lon2)

        lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Radius of earth in kilometers. Use 3956 for miles
        radius = 6371.0

        # Distance in kilometers
        distance = radius * c

        # Ponderate distance with 'close' response
        if distance < 10:
            ponderation = 1 - distance / 10
        else:
            ponderation = 0

        new_best_events.append(
            (event, score + float(user_response['close']) * ponderation))

    best_events = new_best_events

    # Calculate weather, and ponderate it with 'outdoors' response
    new_best_events = []
    for event, score in best_events:
        event_lat, event_long = float(event['coordinates']['latitude']), float(event['coordinates']['longitude'])
        prec, temp = get_precipitation_and_temperature(event_lat, event_long)

        # Ponderate temperature with 'outdoors' response
        if temp > 25:
            ponderation = 1 - (temp - 25) / 10
        else:
            ponderation = 0

        if prec > 0:
            ponderation = 0
        else:
            ponderation = ponderation * 0.5

        new_best_events.append(
            (event, score + float(user_response['outdoors']) * ponderation))

    best_events = new_best_events

    for best_event in best_events:
        logging.debug(best_event[0]['title'], best_event[1])
    
    ordered_events = [event for event, score in sorted(
        best_events, key=lambda x: x[1], reverse=True)]
    return ordered_events


def haversine(lat1, lon1, lat2, lon2):
    # Earth radius in kilometers
    R = 6371.0

    # coordinates in radians
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))

    # differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance

def get_events_by_category(events, category):
    filtered_events =  [event for event in events if event['categories'] == category]
    return filtered_events

def get_event_by_title(events, name):
    for event in events:
        if event['title'] == name:
            return event
    return None

def get_event_by_id(events, id):
    for event in events:
        if event['id'] == id:
            return event
    return None

def find_nearest_events(events, top_n=4):
    if 'latitude' in session and 'longitude' in session:
        user_lat = session['latitude']
        user_lon = session['longitude']

        # Calculate distance of each event from the user
        distances = []
        for e in events:
            event_coordinates = e['coordinates']
            event_lat, event_lon = event_coordinates['latitude'], event_coordinates['longitude']
            distance = haversine(user_lat, user_lon, event_lat, event_lon)
            distances.append((distance, e))

        # Sort events by distance
        distances.sort(key=lambda x: x[0])

        # Return the top N events
        return [event for _, event in distances[:top_n]]

    else:
        return []

@app.route('/')
def index():
    first_five_events = all_events[:4]

    return render_template('index.html', 
                           google_maps_api_key=os.getenv('MAPS_API_KEY'),
                           popular_events=first_five_events)
    

@app.route('/get_nearest_events', methods=['POST'])
def get_nearest_events():
    user_location = request.json
    session['latitude'] = user_location['latitude']
    session['longitude'] = user_location['longitude']
    nearest_events = find_nearest_events(all_events, top_n=4)
    # Format the events as needed
    nearest_events_json = json.loads(json_util.dumps(nearest_events))
    return jsonify(nearest_events_json)  


@app.route('/search', methods=['GET'])
def search():
    search = request.args.get('query', '')
    query = {
        'search': search
    }
    return render_template('list_page.html', query=query)

@app.route('/list_page')
def list_page():
    # Cuestionario
    energic = request.args.get('energic', '')
    if energic:
        exciting = request.args.get('exciting')
        calm = request.args.get('calm')
        outdoors = request.args.get('outdoors')
        with_children = request.args.get('with_children')
        funny = request.args.get('funny')
        close = request.args.get('close')
        price = request.args.get('price')

        query = {
            'energic': energic,
            'exciting': exciting,
            'calm': calm,
            'outdoors': outdoors,
            'with_children': with_children,
            'funny': funny,
            'close': close,
            'price': price
        }
        logging.debug(f'213123Query params: {query}')

        return render_template('list_page.html', query=query)

    category = request.args.get('category', 'all')
    if category:
        query = {
            'category': category
        }
        return render_template('list_page.html', query=query)
    

@app.route('/map_content', methods=['GET', 'POST'])
def map_content():
    return render_template('map_content.html')

@app.route('/list_content', methods=['GET', 'POST'])
def list_content():
    events = request.json
    for event in events:
        if '_id' in event:
            event['_id'] = str(event['_id'])
    if events is None:
        print('No JSON data provided')
        return jsonify({'error': 'No JSON data provided'}), 400
    
    return render_template('list_content.html', events=events)


@app.route('/event_detail_page/<event_title>')
def event_detail_page(event_title):

    event = get_event_by_title(all_events, event_title)

    return render_template('event_detail.html', event=event)


@app.route('/get_events')
def get_events():
    logging.debug('Received a request on /get_events')
    query_params = request.args.to_dict()
    logging.debug(f'Query params: {query_params}')

    energic = query_params.get('energic', '')
    if energic:
        user_response = {
            'energic': energic,
            'exciting': query_params.get('exciting'),
            'calm': query_params.get('calm'),
            'outdoors': query_params.get('outdoors'),
            'with_children': query_params.get('with_children'),
            'funny': query_params.get('funny'),
            'close': query_params.get('close'),
            'price': query_params.get('price')
        }
        events = get_events_from_questionary(session.get('latitude', 40.2456), session.get('longitude', 3.4227), user_response)
        events_json = json.loads(json_util.dumps(events))
        return jsonify(events_json)

    category = query_params.get('category', 'all')
    search = query_params.get('search', '')


    if category != 'all':
        logging.debug(f'Filtering by category: {category}')
        events = get_events_by_category(all_events, category)
    else:
        logging.debug('No category filter')
        events = all_events

    if search != '':
        events = search_events(events, search)
    else:
        events = events

    # Convert MongoDB objects to JSON
    events_json = json.loads(json_util.dumps(events))
    return jsonify(events_json)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)