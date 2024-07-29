
# Created by Mark Dearman (a-iO5)

import tftu_backpack
import tftu_db_utils
import tftu_settings
import tftu_logger
import time

from tftu_utils import ref_calculator

from datetime import datetime
import requests

bptf_listing_url = f"https://backpack.tf/api/classifieds/listings/snapshot?appid={tftu_settings.TF2_APP_ID}"

def check_backpack_for_trades():
    detailed_items = {}
    backpack_items = tftu_db_utils.get_all_backpack_items()
    
    for item in backpack_items:
        defindex = int(item["defindex"])
        item_name = tftu_db_utils.get_item_by_defindex(defindex)['item_name']
        
        if defindex in detailed_items:
            detailed_items[defindex]["count"] += 1
        else:
            detailed_items[defindex] = {
                "defindex": defindex,
                "item_name": item_name,
                "count": 1
            }
    
    # Convert the dictionary to a list
    detailed_items_list = list(detailed_items.values())
    
    #for data in detailed_items_list:
    #    print(data)
    
    return detailed_items_list

def check_item_transaction_price(defindex, intent):
    if intent not in ["buy", "sell"]:
        print("intent must be buy or sell")
        return

    transaction_listings = []  # Use a list to store multiple listings
    item = tftu_db_utils.get_item_by_defindex(defindex)

    def fetch_listings(item_name_key, retry_attempts=3, wait_time=5):
        params = {
            'appid': 440,
            'sku': item[item_name_key],
            'token': tftu_settings.BPTF_ACCESS_TOKEN
        }

        for attempt in range(retry_attempts):
            response = requests.get("https://backpack.tf/api/classifieds/listings/snapshot", params=params)
            data = response.json()

            if response.status_code == 429:  # If rate limited, wait and retry
                tftu_logger.log_and_display_info("Status code: 429", f"Rate limit hit. Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
                continue

            try:
                for listing in data['listings']:
                    if listing["intent"] == intent:
                        steamID = listing["steamid"]
                        details = listing["details"]
                        item_data = listing["item"]
                        timestamp = int(listing["timestamp"])
                        bump = int(listing["bump"])
                        price = listing["price"]
                        currencies = listing["currencies"]

                        transaction_listings.append({
                            "steamID": steamID,
                            "details": details,
                            "item": item_data,
                            "timestamp": datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                            "bump": datetime.fromtimestamp(bump).strftime('%Y-%m-%d %H:%M:%S'),
                            "price": price,
                            "currencies": currencies
                        })
                return True, None, None  # Indicate success
            except Exception as error:
                return False, error, data  # Indicate failure, return error and data

        return False, "Maximum retry attempts reached", data

    # Try fetching listings with 'item_name' first, then 'name' if it fails
    success, error, data = fetch_listings('item_name')
    if not success:
        success, error, data = fetch_listings('name')
        if not success:
            tftu_logger.log_and_display_warning(error, f"Error finding listings, It is possible there is none for {item.get('item_name') or item.get('name')}, {data}.")

    return transaction_listings

def find_item_profitable_deal(defindex):

    item_name = tftu_db_utils.get_item_by_defindex(defindex)['item_name']

    buy_listings = check_item_transaction_price(defindex, "buy")
    sell_listings = check_item_transaction_price(defindex, "sell")

    if buy_listings and sell_listings:
        highest_buy_price = max(listing["price"] for listing in buy_listings)
        lowest_sell_price = min(listing["price"] for listing in sell_listings)

        if highest_buy_price > lowest_sell_price:
            profit = round(highest_buy_price - lowest_sell_price, 2)
            if profit > tftu_settings.PROFIT_FALSE_POSITIVE_LIMIT:
                print("-" * 40)
                print(f"⚠️ Unusually high profit detected for {item_name}, skipping...")
                print("-" * 40)
                return

            profit_str = str(ref_calculator(profit))
            print("-" * 40)
            print(f"✨ Profitable Deal Found for {item_name} ✨")
            print(f"💰 Buy at: {ref_calculator(lowest_sell_price)}")
            print(f"💵 Sell at: {ref_calculator(highest_buy_price)}")
            print(f"📈 Profit: {profit_str}")
            print("-" * 40)
        else:
            print("-" * 40)
            print(f"❌ No Profitable Deals for {item_name}")
            print("-" * 40)

def skim_backpack_for_profit():
    backpack = tftu_db_utils.get_all_backpack_items()
    for item in backpack:
        find_item_profitable_deal(item["defindex"])