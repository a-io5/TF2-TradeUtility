
# Created by Mark Dearman (a-iO5)

import sqlite3
import json
import tftu_settings

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def commit(self):
        if self.connection:
            self.connection.commit()

    def execute(self, query, params=()):
        self.connect()
        self.cursor.execute(query, params)
        return self.cursor

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()
    
    def get_description(self):
        return self.cursor.description if self.cursor else None
    
db_manager = DatabaseManager(tftu_settings.DB_NAME)

def generate_db():
    # Create backpack table
    db_manager.execute('''
        CREATE TABLE IF NOT EXISTS backpack (
            id INTEGER PRIMARY KEY,
            original_id INTEGER,
            defindex INTEGER,
            level INTEGER,
            quality INTEGER,
            inventory INTEGER,
            quantity INTEGER,
            origin INTEGER,
            flag_cannot_trade BOOLEAN,
            attributes JSON,
            buy_receipt_id INTEGER,
            FOREIGN KEY (buy_receipt_id) REFERENCES buy_receipts (id)
        )
    ''')

    # Create buy_receipts table
    db_manager.execute('''
        CREATE TABLE IF NOT EXISTS buy_receipts (
            id SERIAL PRIMARY KEY,
            defindex INTEGER,
            quantity INTEGER,
            price_refined FLOAT,
            transaction_date TIMESTAMP,
            attributes JSON,
            FOREIGN KEY (defindex) REFERENCES backpack (defindex)
        )
    ''')

    # Create sell_receipts table
    db_manager.execute('''
        CREATE TABLE IF NOT EXISTS sell_receipts (
            id SERIAL PRIMARY KEY,
            defindex INTEGER,
            quantity INTEGER,
            price_refined FLOAT,
            transaction_date TIMESTAMP,
            attributes JSON,
            FOREIGN KEY (defindex) REFERENCES backpack (defindex)
        )
    ''')

    # Create items table
    db_manager.execute('''
        CREATE TABLE IF NOT EXISTS items (
            defindex INTEGER PRIMARY KEY,
            name TEXT,
            item_class TEXT,
            item_type_name TEXT,
            item_name TEXT,
            item_description TEXT,
            proper_name BOOLEAN,
            item_slot TEXT,
            model_player TEXT,
            item_quality INTEGER,
            image_inventory TEXT,
            min_ilevel INTEGER,
            max_ilevel INTEGER,
            image_url TEXT,
            image_url_large TEXT,
            drop_type TEXT,
            craft_class TEXT,
            craft_material_type TEXT,
            capabilities JSON,
            used_by_classes JSON,
            attributes JSON
        )
    ''')

    db_manager.close()

def add_item_to_backpack(id, original_id, defindex, level, quality, inventory, quantity, origin, flag_cannot_trade, attributes, buy_receipt_id=None):
    db_manager.execute('''
                   INSERT INTO backpack (id, original_id, defindex, level, quality, inventory, quantity, origin, flag_cannot_trade, attributes, buy_receipt_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                    original_id=excluded.original_id,
                    defindex=excluded.defindex,
                    level=excluded.level,
                    quality=excluded.quality,
                    inventory=excluded.inventory,
                    quantity=excluded.quantity,
                    origin=excluded.origin,
                    flag_cannot_trade=excluded.flag_cannot_trade,
                    attributes=excluded.attributes,
                    buy_receipt_id=excluded.buy_receipt_id
                   ''', (id, original_id, defindex, level, quality, inventory, quantity, origin, flag_cannot_trade, json.dumps(attributes), buy_receipt_id)
                   )
    db_manager.commit()
    db_manager.close()

def add_item_to_item_list(defindex, name, item_class, item_type_name, item_name, item_description, proper_name, item_slot, model_player, item_quality, image_inventory, min_ilevel, max_ilevel, image_url, image_url_large, drop_type, craft_class, craft_material_type, capabilities, used_by_classes, attributes):
    db_manager.execute('''
                   INSERT INTO items (defindex, name, item_class, item_type_name, item_name, item_description, proper_name, item_slot, model_player, item_quality, image_inventory, min_ilevel, max_ilevel, image_url, image_url_large, drop_type, craft_class, craft_material_type, capabilities, used_by_classes, attributes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(defindex) DO UPDATE SET
                    name=excluded.name,
                    item_class=excluded.item_class,
                    item_type_name=excluded.item_type_name,
                    item_name=excluded.item_name,
                    item_description=excluded.item_description,
                    proper_name=excluded.proper_name,
                    item_slot=excluded.item_slot,
                    model_player=excluded.model_player,
                    item_quality=excluded.item_quality,
                    image_inventory=excluded.image_inventory,
                    min_ilevel=excluded.min_ilevel,
                    max_ilevel=excluded.max_ilevel,
                    image_url=excluded.image_url,
                    image_url_large=excluded.image_url_large,
                    drop_type=excluded.drop_type,
                    craft_class=excluded.craft_class,
                    craft_material_type=excluded.craft_material_type,
                    capabilities=excluded.capabilities,
                    used_by_classes=excluded.used_by_classes,
                    attributes=excluded.attributes
                   ''', (
                       defindex,
                       name,
                       item_class,
                       item_type_name,
                       item_name,
                       item_description,
                       proper_name,
                       item_slot,
                       model_player,
                       item_quality,
                       image_inventory,
                       min_ilevel,
                       max_ilevel,
                       image_url,
                       image_url_large,
                       drop_type,
                       craft_class,
                       craft_material_type,
                       capabilities,
                       used_by_classes,
                       attributes
                   ))
    
    db_manager.commit()
    db_manager.close()

def get_all_backpack_items():
    query = 'SELECT * FROM backpack WHERE flag_cannot_trade IS NULL AND defindex NOT IN (5000, 5001, 5002)' # Remove "WHERE flag_cannot_trade IS NULL" if you want to retrieve all items even if they cant be traded and Remove NOT IN (5000, 5001, 5002) if you want to list metals
    cursor = db_manager.execute(query)
    columns = [desc[0] for desc in db_manager.get_description()]
    items = [dict(zip(columns, row)) for row in db_manager.fetchall()]
    return items

def get_backpack_item_by_defindex(defindex):
    query = 'SELECT * FROM backpack WHERE defindex = ?'
    cursor = db_manager.execute(query, (defindex,))
    columns = [desc[0] for desc in db_manager.get_description()]
    row = db_manager.fetchone()
    return dict(zip(columns, row)) if row else None

def get_item_by_defindex(defindex):
    query = 'SELECT * FROM items WHERE defindex = ?'
    cursor = db_manager.execute(query, (defindex,))
    columns = [desc[0] for desc in db_manager.get_description()]
    row = db_manager.fetchone()
    return dict(zip(columns, row)) if row else None

def check_db_exists():
    return