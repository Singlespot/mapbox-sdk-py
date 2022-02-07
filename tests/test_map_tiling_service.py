import random
import string
from tkinter import Tk
import json
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import os
import sys
import tkinter
import requests
from mapbox.services.map_tiling_service import MTS

if __name__ == "__main__":
    path = "/home/benjamin/dev/pycharm_projects/editor_rating"
    os.chdir(path)
    conf = json.load(open('src/dev.conf.json'))
    os.environ['MAPBOX_ACCESS_TOKEN'] = conf['MAPBOX']
    # ----------------------------------------------------------------------------------------------
    # CREATE TILESET SOURCE
    UUID = '_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    NAME = 'MTS_INTEGRATION' + UUID
    mapbox_tiling_service = MTS()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[408, 422, 429, 502, 503, 504],
        method_whitelist=["POST"],
        raise_on_status=False
    )
    mapbox_tiling_service.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    file_path = '/home/benjamin/dev/pycharm_projects/editor_rating/Data Studies/Others/Etude_PMP_Conseil/MTS_Integration/VIA_CLI_TOOL/populated_places.geojson.ld'
    create_resp = mapbox_tiling_service.create_tileset_source("benjamindanso", NAME, file_path)
    print(create_resp.json())
    # ----------------------------------------------------------------------------------------------
    # CREATE TILESET
    tileset_id = 'benjamindanso.' + NAME
    recipe_file_path = '/home/benjamin/dev/pycharm_projects/editor_rating/Data Studies/Others/Etude_PMP_Conseil/MTS_Integration/VIA_API/recipe-for-api.json'
    recipe_file = open(recipe_file_path, "r")
    recipe_json = json.load(recipe_file)
    recipe_file.close()
    recipe_json["recipe"]["layers"]["layer"]["source"] = create_resp.json()["id"]
    recipe_json["name"] = NAME
    recipe_file = open(recipe_file_path, "w")
    json.dump(recipe_json, recipe_file)
    recipe_file.close()

    create_resp = mapbox_tiling_service.create_tileset(tileset_id, recipe_file_path)
    print(create_resp.json())
    # ----------------------------------------------------------------------------------------------
    # PUBLISH TILESET
    create_resp = mapbox_tiling_service.publish_tileset(tileset_id)
    print(create_resp.json())
