
# Created by Mark Dearman (a-iO5)

import requests
import tftu_settings
from tftu_db_utils import add_item_to_backpack, add_item_to_item_list

import json
import time

items_get_url = f"https://api.steampowered.com/IEconItems_{tftu_settings.TF2_APP_ID}/GetSchemaItems/v0001/?key={tftu_settings.STEAM_API_KEY}&language=eng"
backpack_get_url = f"https://api.steampowered.com/IEconItems_{tftu_settings.TF2_APP_ID}/GetPlayerItems/v0001/?SteamID={tftu_settings.PROFILE_ID}&key={tftu_settings.STEAM_API_KEY}"

def update_item_table():
    params = {"start": 0}
    retry_count = 5
    delay = 2  # Delay in seconds between requests

    while True:
        try:
            response = requests.get(items_get_url, params=params)
            data = response.json()

            for item in data["result"]["items"]:
                add_item_to_item_list(item.get('defindex'),
                                    item.get('name'),
                                    item.get('item_class'),
                                    item.get('item_type_name'),
                                    item.get('item_name'),
                                    item.get('item_description'),
                                    item.get('proper_name'),
                                    item.get('item_slot'),
                                    item.get('model_player'),
                                    item.get('item_quality'),
                                    item.get('image_inventory'),
                                    item.get('min_ilevel'),
                                    item.get('max_ilevel'),
                                    item.get('image_url'),
                                    item.get('image_url_large'),
                                    item.get('drop_type'),
                                    item.get('craft_class'),
                                    item.get('craft_material_type'),
                                    json.dumps(item.get('capabilities', [])),
                                    json.dumps(item.get('used_by_classes', [])),
                                    json.dumps(item.get('attributes', []))
                                    )
                print(f"Added item: {item.get('name')}, The defindex of this is {item.get('defindex')}.")
            
            if "next" in data["result"]:
                params['start'] = data["result"]["next"]
                print(f"New page, Starting from defindex: {data['result']['next']}.")
            else:
                break
        except requests.exceptions.RequestException as e:
            if retry_count > 0:
                retry_count -= 1
                time.sleep(delay)
                print(f"Request failed, retrying... ({retry_count} retries left)")
            else:
                print("Max retries reached. Exiting.")
                break

def refresh_backpack():
    delay = 2  # Delay in seconds between requests
    retry_count = 5

    while True:
        try:
            response = requests.get(f'https://api.steampowered.com/IEconItems_{tftu_settings.TF2_APP_ID}/GetPlayerItems/v0001/?SteamID={tftu_settings.PROFILE_ID}&key={tftu_settings.STEAM_API_KEY}')
            data = response.json()

            if response.status_code != 200:
                raise Exception(f"Invalid status code : {response.status_code}")

            for item in data["result"]["items"]:
                add_item_to_backpack(item.get('id'),
                                    item.get('original_id'),
                                    item.get('defindex'),
                                    item.get('level'),
                                    item.get('quality'),
                                    item.get('inventory'),
                                    item.get('quantity'),
                                    item.get('origin'),
                                    item.get('flag_cannot_trade'),
                                    item.get('attributes', []))
                
            break
            
        except Exception as e:
            if retry_count > 0:
                retry_count -= 1
                time.sleep(delay)
                print(f"Request failed, retrying... ({retry_count} retries left) || ERROR: {e}")
            else:
                print("Max retries reached. Exiting.")
                break
    


