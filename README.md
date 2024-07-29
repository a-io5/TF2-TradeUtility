
# TF2-TradeUtility - Few tools dedicated to TF2 backpacks and backpack.tf

## Overview
This project was created as a fun side project in one night. It's not fully finished and is provided as-is. Feel free to use it however you like, but please credit me if you do.

## Disclaimer
I did this project just to see if I could. I don't plan to continue working on it for the foreseeable future, unless there's a huge demand. I'm available to answer questions and provide support, but I won't be actively updating it.

## Basic Functionality
The project interacts with the Steam API and Backpack.tf API to retrieve and manage Team Fortress 2 items and player backpacks.

### Main Features
- **Item Table**: Retrieves item schema from the Steam API and stores all items in a local database.
- **Basic Backpack Tools**: Retrieves the player's backpack data from the Steam API and stores within a local database.

## Usage
1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd TF2-TradeUtility
    ```

2. **Install dependencies** (if any):
    ```sh
    pip install -r requirements.txt
    ```

3. **Update Settings**:
    - Open `tftu_settings.py` and fill in your Steam API key, Steam64 ID, and Backpack.tf credentials.

4. **Run the demo script**:
    - Run this script initially, Although this is just a demo script to show basic functionaliy. run:
      ```sh
      python tftu_test_setup.py
      ```

## Credits
- Created by Mark Dearman (a-iO5)
- Github: https://github.com/a-io5
- Discord: io5
- Linkedin: https://shorturl.at/3aMNc

## License
Feel free to use this project however you want, but please credit me. And if you are going to use this in a bigger project, i personally would love to hear about it!
