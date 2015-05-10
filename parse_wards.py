import json

import requests

WARD_TYPE = "District council ward"
CURRENT_GENERATION = 23

def get_wards():
    """
    Construct a dictionary of wards
    """
    with open("children.json") as f:
        children = json.loads(f.read())
    wards = {
        k:v for k,v in children.items() if v['type_name'] == WARD_TYPE and v['generation_high'] == CURRENT_GENERATION
    }
    return wards

def fetch_boundaries(wards):
    """
    Fetch the ward boundaries from the mapit site
    """
    for w in wards.values():
        url = "http://mapit.mysociety.org/area/{}.geojson".format(w['id'])
        response = requests.get(url)
        filename = "wards/{}.geojson".format(w['id'])
        with open(filename, 'w') as f:
            f.write(response.content)

if __name__ == "__main__":
    wards = get_wards()
    fetch_boundaries(wards)
