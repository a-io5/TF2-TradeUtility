
# Created by Mark Dearman (a-iO5)

import tftu_db_utils
import tftu_backpack
import tftu_market

tftu_db_utils.generate_db()
tftu_backpack.update_item_table() # Grab a cuppa! this can take a minute or two, Make sure you wait until this has finished!!!
tftu_backpack.refresh_backpack()
tftu_market.skim_backpack_for_profit()

#This is just a test script, specifically used for setup. Above is a suggested order if you want to run just this script.