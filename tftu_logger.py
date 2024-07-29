
# Created by Mark Dearman (a-iO5)

import logging

# Just a fun little logging script because looking at the console all day can get quite mundane ;D ... Expecially if your job entails staring at it all day.

# Set up logging
logging.basicConfig(filename='app_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to log and display errors
def log_and_display_error(error_message, optional_message=None, additional_data=None):
    logging.error(error_message)
    print("-" * 40)
    print(f"❌ Error: {error_message}")
    if optional_message:
        print(f"ℹ️  Info: {optional_message}")
    if additional_data:
        print(f"🔍 Additional Data: {additional_data}")
    print("Please check the error log for more details.")
    print("-" * 40)

# Function to log and display warnings
def log_and_display_warning(warning_message, optional_message=None, additional_data=None):
    logging.warning(warning_message)
    print("-" * 40)
    print(f"⚠️  Warning: {warning_message}")
    if optional_message:
        print(f"ℹ️  Info: {optional_message}")
    if additional_data:
        print(f"🔍 Additional Data: {additional_data}")
    print("-" * 40)

# Function to log and display information
def log_and_display_info(info_message, optional_message=None, additional_data=None):
    logging.info(info_message)
    print("-" * 40)
    print(f"ℹ️  Info: {info_message}")
    if optional_message:
        print(f"ℹ️  Details: {optional_message}")
    if additional_data:
        print(f"🔍 Additional Data: {additional_data}")
    print("-" * 40)

# Function to log and display success messages
def log_and_display_success(success_message, optional_message=None, additional_data=None):
    logging.info(success_message)
    print("-" * 40)
    print(f"✅ Success: {success_message}")
    if optional_message:
        print(f"ℹ️  Info: {optional_message}")
    if additional_data:
        print(f"🔍 Additional Data: {additional_data}")
    print("-" * 40)