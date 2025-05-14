# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'fast_cars2.db'

# This is the SQL to connect to all the tables in the database
TABLES = (" fast_cars "
           "LEFT JOIN makes ON fast_cars.make_id = makes.make_id "
           "LEFT JOIN aspirations ON fast_cars.aspiration_id = aspirations.aspiration_id "
           "LEFT JOIN cylinders ON fast_cars.cylinder_id = cylinders.cylinder_id ")

def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
    print('')
    # Set up the connection to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    # Get the results from the view
    sql = "SELECT * FROM '" + view_name + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    # Get the field names to use as headings
    field_names = "SELECT name from pragma_table_info('" + view_name + "') AS tblInfo"
    cursor.execute(field_names)
    headings = list(sum(cursor.fetchall(),()))
    # Print the results in a table with the headings
    print(tabulate(results,headings))
    db.close()

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    print('')
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    db.close()

menu_choice = ''
print('Welcome to the Cars database\n')
while menu_choice != 'EXIT':
    menu_choice = input('Type the number for the information you want:\n'
                        '1: All cars\n'
                        '2: 10 fastest cars\n'
                        '3: 5 most expensive cars\n'
                        '4: Cheap fast cars with engine capacity less than 4 litres\n'
                        '5: All English cars\n'
                        '6: Fast cars which aren\'t electric\n'
                        '7: Cars with high horsepower and torque\n'
                        '8: All of the makes and model sorted by the make then model\n'
                        '9: All naturally aspirated cars\n'
                        '10: Find all cars of a certain make\n'
                        'EXIT: To exit the menu\n\n'
                        'Type option here: ')
    menu_choice = menu_choice.upper()
    if menu_choice == '1':
        print_query('all_data')
    elif menu_choice == '2':
        print_query('10_fastest')
    elif menu_choice == '3':
        print_query('5_expensive')
    elif menu_choice == '4':
        print_query('cheap_fast')
    elif menu_choice == '5':
        print_query('english_cars')
    elif menu_choice == '6':
        print_query('fast_non_electric')
    elif menu_choice == '7':
        print_query('high_horsepower_and_torque')
    elif menu_choice == '8':
        print_query('make_and_model')
    elif menu_choice == '9':
        print_query('naturally_aspirated')
    elif menu_choice == '10':
        make = input('Which make cars do you want to see?: ')
        print_parameter_query("model, top_speed", "make = ? ORDER BY top_speed DESC",make)
    print('')