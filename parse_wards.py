#!/usr/bin/env python3

import json

import requests

CURRENT_GENERATION = 25

GUILDFORD_BOROUGH_COUNCIL = {
    'id': 2452,
    'type': 'DIS',
    'ward_type': 'DIW',
    'name': 'Guildford Borough Council',
}

SURREY_COUNTY_COUNCIL = {
    'id': 2242,
    'type': 'CTY',
    'ward_type': 'CED',
    'name': 'Surrey County Council'
}

def get_ward_info(council):
    """
    Construct a dictionary of wards
    """
    url = "https://mapit.mysociety.org/area/{}/children".format(council['id'])
    response = requests.get(url)
    
    with open("{}/children.json".format(council['name']), 'wb') as f:
        f.write(response.content)
    
    children = response.json()
    ward_info = {
        k:v for k,v in children.items() if v['type'] == council['ward_type'] and v['generation_high'] == CURRENT_GENERATION
    }
    return ward_info

def fetch_boundaries(council, ward_info):
    """
    Fetch the ward boundaries from the mapit site
    """
    for ward in ward_info.values():
        print("Fetching ward {}".format(ward['name']))
        url = "https://mapit.mysociety.org/area/{}.geojson".format(ward['id'])
        response = requests.get(url)
        filename = "{}/wards/{}.geojson".format(council['name'], ward['id'])
        with open(filename, 'wb') as f:
            f.write(response.content)

def construct_borough_json(council, ward_info):
    """
    Creates a single json file with all the wards
    """
    collection = {
        "type": "FeatureCollection",
        "features": [
        ]
    }
    for ward_id, ward in ward_info.items():
        filename = "{}/wards/{}.geojson".format(council['name'], ward['id'])
        with open(filename, 'r') as f:
            polygon = json.loads(f.read())
            polygon['properties'] = {'name': ward['name']}
            collection['features'].append(polygon)

    with open("{}/{}.geojson".format(council['name'], council['name']), 'w') as f:
        f.write(json.dumps(collection))

if __name__ == "__main__":
    council = SURREY_COUNTY_COUNCIL
    ward_info = get_ward_info(council)
    # fetch_boundaries(council, ward_info)
    construct_borough_json(council, ward_info)
