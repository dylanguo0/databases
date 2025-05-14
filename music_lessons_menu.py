# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'music_lessons.db'

# This is the SQL to connect to all the tables in the database
TABLES = (" student_info "
            "LEFT JOIN genders ON student_info.gender_id = genders.gender_id "
            "LEFT JOIN instruments ON student_info.instrument_id = instruments.instrument_id "
            "LEFT JOIN schools ON student_info.school_id = schools.school_id "
            "LEFT JOIN days ON student_info.day_id = days.day_id ")

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

def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
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

menu_choice = ''
print('Welcome to the music lessons database')
while menu_choice != 'EXIT':
    menu_choice = input('\nType the number for the information you want:\n'
                        '1: All music lessons\n'
                        '2: All students sorted in alphabetical order by surname then first name\n'
                        '3: All music lessons in order from earliest to latest\n'
                        '4: Find all students who have a lesson on a certain day, ordered from earliest time to latest time\n'
                        '5: All students who\'s learning the piano\n'
                        '6: All male students\n'
                        '7: Parents who owe the most money\n'
                        '8: Students sorted from oldest to youngest\n'
                        '9: All students born in 2008\n'
                        'EXIT: To exit the menu\n\n'
                        'Type option here: ')
    print('')
    menu_choice = menu_choice.upper()
    if menu_choice == '1':
        print_query('all_data')
    elif menu_choice == '2':
        print_query('alphabetical_names')
    elif menu_choice == '3':
        print_query('earliest_to_latest')
    elif menu_choice == '4':
        day = input('Which day to you want to see: ').title()
        print_parameter_query("first_name, school_code, parent_first_name, parent_phone, instrument, lesson_time", "day = ? ORDER BY lesson_time", day)
    elif menu_choice == '5':
        print_query('piano')
    elif menu_choice == '6':
        print_query('male')
    elif menu_choice == '7':
        print_query('most_owed')
    elif menu_choice == '8':
        print_query('oldest_to_youngest')
    elif menu_choice == '9':
        print_query('2008s')