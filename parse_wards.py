#!/usr/bin/env python3

import json

import requests

WARD_TYPE = "District council ward"
CURRENT_GENERATION = 23

def get_ward_info():
    """
    Construct a dictionary of wards
    """
    with open("children.json") as f:
        children = json.loads(f.read())
    ward_info = {
        k:v for k,v in children.items() if v['type_name'] == WARD_TYPE and v['generation_high'] == CURRENT_GENERATION
    }
    return ward_info

def fetch_boundaries(ward_info):
    """
    Fetch the ward boundaries from the mapit site
    """
    for ward in ward_info.values():
        print("Fetching ward {}".format(ward['name']))
        url = "http://mapit.mysociety.org/area/{}.geojson".format(ward['id'])
        response = requests.get(url)
        filename = "wards/{}.geojson".format(ward['id'])
        with open(filename, 'w') as f:
            f.write(response.content.decode('utf-8'))

def construct_borough_json(ward_info):
    """
    Creates a single json file with all the wards
    """
    collection = {
        "type": "FeatureCollection",
        "features": [
        ]
    }
    for ward_id, ward in ward_info.items():
        filename = "wards/{}.geojson".format(ward['id'])
        with open(filename, 'r') as f:
            polygon = json.loads(f.read())
            collection['features'].append(polygon)

    with open("wards/guildford.geojson", 'w') as f:
        f.write(json.dumps(collection))

if __name__ == "__main__":
    ward_info = get_ward_info()
    # fetch_boundaries(ward_info)
    construct_borough_json(ward_info)
