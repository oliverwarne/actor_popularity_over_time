from flask import Flask, request, jsonify, abort
import json
import requests
from common import actormap
import os

API_KEY = os.environ.get("OMDB_API_KEY")
if API_KEY is None or len(API_KEY) == 0:
    print("Failed to pull OMDB_API_KEY from environment. Make sure you set it")
    raise Exception("api_key not found")

# init actormap

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # not very efficient way to serve static files.
    return app.send_static_file('index.html')

@app.route('/actor', methods=['POST'])
def actor():
    content = request.get_json(force=True)
    if content is None:
        print("actor(): data is none")
        print(request)
        abort(500) # on fail, return code 500

    # check that actorname is in body
    if 'actorname' not in content:
        print("actor(): actorname not provided")
        abort(500)
    actorname = content['actorname']

    # search actormap for matching actorid
    actorid  = search_actor_map(actorname)
    if actorid is None:
        print("actor(): actorid not found")
        abort(500)

    # on match, query omdb with actorid
    resp = query_omdb(actorid)
    if resp is None:
        print("actor(): query resp is bad")
        abort(500)

    # on successful query, get popularity
    years, pop = get_popularity_from_response(resp)

    # return popularity
    return jsonify({'years': years, 'pop': pop})

def search_actor_map(actorname):
    """
    scan map (global variable?) to see if actor is in it.
    return actorid if found
    return None if actorname not in map
    """
    actorname = actorname.lower()
    return actormap[actorname] if actorname in actormap else None

def query_omdb(actorid):
    """
    send a query to omdb and return its response
    """
    base_url = "https://api.themoviedb.org/3/person/{0}/movie_credits?api_key={1}"
    query_url = base_url.format(actorid, API_KEY)

    resp = requests.get(query_url)
    if not resp.ok:
        print("query_omdb(): bad response")
        return None

    try:
        resp_data = resp.json()
    except:
        # can't pull out data
        print("query_omdb(): failed to turn data into json")
        return None

    if "cast" not in resp_data:
        print("query_omdb(): failed to pull cast out of data")
        return None

    return resp_data["cast"]

def get_popularity_from_response(resp):
    """
    Scan through the actor omdb query and return the 

    keys: list of years actor was active in
    values: the corresponding popularity of year
    """
    year_pop_map = {}

    for movie in resp:
        if 'release_date' not in movie or 'vote_count' not in movie:
            continue

        year_of_release = movie['release_date'][0:4]
        if len(year_of_release) != 4:
            continue
        vote_count = movie['vote_count']

        if year_of_release not in year_pop_map:
            year_pop_map[year_of_release] = 0

        year_pop_map[year_of_release] += vote_count

    # we now need to sort the dictionary, then turn into two lists
    sorted_tuple_list = sorted(year_pop_map.items())

    return zip(*sorted_tuple_list)

def populate_actor_map_in_cache():
    """
    parse actormap from pi.json to populate a dictionary of actors

    each line in pi.json is a seperate json object


    doesn't handle multiple actors with same name but different ids

    """
    print("\n\nPopulating actormap...\n")
    with open('pi.json') as person_file:
        for line in person_file:
            data = json.loads(line)

            name = data["name"] if "name" in data else None
            person_id = data["id"] if "id" in data else None

            if name is None or person_id is None:
                continue
            actormap[name.lower()] = person_id
    print("\nDone populating actormap")

def setup():
    populate_actor_map_in_cache()

setup()

