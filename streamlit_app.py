from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd

from io import StringIO
from io import BytesIO

Otput_Final = 'Whizard_compar\\2017-P Empire Distr\\output_Final_R06'


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Ramchand2009',
    page_icon=':shopping_bags:', # This is an emoji shortcode. Could be a URL too.
)


# -----------------------------------------------------------------------------
# Declare some useful functions.

def connect_db():
    '''Connects to the sqlite database.'''

    DB_FILENAME = Path(__file__).parent/'inventory.db'
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created


def initialize_data(conn):
    '''Initializes the inventory table with some data.'''
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            price REAL,
            units_sold INTEGER,
            units_left INTEGER,
            cost_price REAL,
            reorder_point INTEGER,
            description TEXT
        )
        '''
    )

    cursor.execute(
        '''
        INSERT INTO inventory
            (item_name, price, units_sold, units_left, cost_price, reorder_point, description)
        VALUES
            -- Beverages
            ('Bottled Water (500ml)', 1.50, 115, 15, 0.80, 16, 'Hydrating bottled water'),
            ('Soda (355ml)', 2.00, 93, 8, 1.20, 10, 'Carbonated soft drink'),
            ('Energy Drink (250ml)', 2.50, 12, 18, 1.50, 8, 'High-caffeine energy drink'),
            ('Coffee (hot, large)', 2.75, 11, 14, 1.80, 5, 'Freshly brewed hot coffee'),
            ('Juice (200ml)', 2.25, 11, 9, 1.30, 5, 'Fruit juice blend'),

            -- Snacks
            ('Potato Chips (small)', 2.00, 34, 16, 1.00, 10, 'Salted and crispy potato chips'),
            ('Candy Bar', 1.50, 6, 19, 0.80, 15, 'Chocolate and candy bar'),
            ('Granola Bar', 2.25, 3, 12, 1.30, 8, 'Healthy and nutritious granola bar'),
            ('Cookies (pack of 6)', 2.50, 8, 8, 1.50, 5, 'Soft and chewy cookies'),
            ('Fruit Snack Pack', 1.75, 5, 10, 1.00, 8, 'Assortment of dried fruits and nuts'),

            -- Personal Care
            ('Toothpaste', 3.50, 1, 9, 2.00, 5, 'Minty toothpaste for oral hygiene'),
            ('Hand Sanitizer (small)', 2.00, 2, 13, 1.20, 8, 'Small sanitizer bottle for on-the-go'),
            ('Pain Relievers (pack)', 5.00, 1, 5, 3.00, 3, 'Over-the-counter pain relief medication'),
            ('Bandages (box)', 3.00, 0, 10, 2.00, 5, 'Box of adhesive bandages for minor cuts'),
            ('Sunscreen (small)', 5.50, 6, 5, 3.50, 3, 'Small bottle of sunscreen for sun protection'),

            -- Household
            ('Batteries (AA, pack of 4)', 4.00, 1, 5, 2.50, 3, 'Pack of 4 AA batteries'),
            ('Light Bulbs (LED, 2-pack)', 6.00, 3, 3, 4.00, 2, 'Energy-efficient LED light bulbs'),
            ('Trash Bags (small, 10-pack)', 3.00, 5, 10, 2.00, 5, 'Small trash bags for everyday use'),
            ('Paper Towels (single roll)', 2.50, 3, 8, 1.50, 5, 'Single roll of paper towels'),
            ('Multi-Surface Cleaner', 4.50, 2, 5, 3.00, 3, 'All-purpose cleaning spray'),

            -- Others
            ('Lottery Tickets', 2.00, 17, 20, 1.50, 10, 'Assorted lottery tickets'),
            ('Newspaper', 1.50, 22, 20, 1.00, 5, 'Daily newspaper')
        '''
    )
    conn.commit()


def load_data(conn):
    '''Loads the inventory data from the database.'''
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM inventory')
        data = cursor.fetchall()
    except:
        return None

    df = pd.DataFrame(data,
        columns=[
            'id',
            'item_name',
            'price',
            'units_sold',
            'units_left',
            'cost_price',
            'reorder_point',
            'description',
        ])

    return df


def update_data(conn, df, changes):
    '''Updates the inventory data in the database.'''
    cursor = conn.cursor()

    if changes['edited_rows']:
        deltas = st.session_state.inventory_table['edited_rows']
        rows = []

        for i, delta in deltas.items():
            row_dict = df.iloc[i].to_dict()
            row_dict.update(delta)
            rows.append(row_dict)

        cursor.executemany(
            '''
            UPDATE inventory
            SET
                item_name = :item_name,
                price = :price,
                units_sold = :units_sold,
                units_left = :units_left,
                cost_price = :cost_price,
                reorder_point = :reorder_point,
                description = :description
            WHERE id = :id
            ''',
            rows,
        )

    if changes['added_rows']:
        cursor.executemany(
            '''
            INSERT INTO inventory
                (id, item_name, price, units_sold, units_left, cost_price, reorder_point, description)
            VALUES
                (:id, :item_name, :price, :units_sold, :units_left, :cost_price, :reorder_point, :description)
            ''',
            (defaultdict(lambda: None, row) for row in changes['added_rows']),
        )

    if changes['deleted_rows']:
        cursor.executemany(
            'DELETE FROM inventory WHERE id = :id',
            ({'id': int(df.loc[i, 'id'])} for i in changes['deleted_rows'])
        )

    conn.commit()


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.

# Set the title that appears at the top of the page.
'''
# :shopping_bags: Ramchand2009

**Welcome to Alice's Corner Store's intentory tracker!**
This page reads and writes directly from/to our inventory database.
'''

st.info('''
    Use the table below to add, remove, and edit items.
    And don't forget to commit your changes when you're done.
    ''')

# Connect to database and create table if needed
conn, db_was_just_created = connect_db()

# Initialize data.
if db_was_just_created:
    initialize_data(conn)
    st.toast('Database initialized with some sample data.')

# Load data from database
df = load_data(conn)


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------




Intput_File_old = st.file_uploader("Choose a Logix Data Dictionary Input Old File")
if Intput_File_old is not None:   
    Input_old = pd.read_excel(Intput_File_old,sheet_name="WHizard Data Dict",skiprows=5)
    
    #st.write(Assets_Input) 

Intput_File_new = st.file_uploader("Choose a Logix Data Dictionary Input New File")
if Intput_File_new is not None:
    Input_new = pd.read_excel(Intput_File_new,sheet_name="WHizard Data Dict",skiprows=5)


data_Final=Input_old.compare(Input_new,keep_shape=True, keep_equal=False)
data_Final.insert(0,'name_Old','')
data_Final["name_Old"]= Input_old["Conveyor/ Device Name"]
data_Final.insert(1,'name_New','')
data_Final["name_New"]= Input_new["Conveyor/ Device Name"]
#data_Final.to_excel(Otput_Final)
#test

#Assets_File.name = "Output_"+Assets_File.name
flnme =  Otput_Final
    #flnme = st.text_input('Enter Excel file name (e.g. email_data.xlsx)')
if flnme != "":
    if flnme.endswith(".xlsx") == False:  # add file extension if it is forgotten
        flnme = flnme + ".xlsx"
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        data_Final.to_excel(writer, sheet_name='Sheet1')
st.write("Output filename:", flnme)
st.download_button(label="Download Excel workbook", data=buffer.getvalue(), file_name=flnme, mime="application/vnd.ms-excel")