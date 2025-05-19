# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate
from easygui import *

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

while True:
    msg = "What information do you want?"
    title = "Welcome to the music lessons database"
    choices = ["All music lessons", 
                "All students sorted in alphabetical order by surname then first name", 
                "All music lessons in order from earliest to latest", 
                "Find all students who have a lesson on a certain day, ordered from earliest time to latest time", 
                "Find all students learning a certain instrument", 
                "Find all students of a certain gender",
                "Parents who owe the most money", 
                "Students sorted from oldest to youngest", 
                "All students born in 2008",
                "All students who are siblings"]
    choice = choicebox(msg, title, choices)
    print('')
    if choice == 'All music lessons':
        print_query('all_data')
    elif choice == 'All students sorted in alphabetical order by surname then first name':
        print_query('alphabetical_names')
    elif choice == 'All music lessons in order from earliest to latest':
        print_query('earliest_to_latest')
    elif choice == 'Find all students who have a lesson on a certain day, ordered from earliest time to latest time':
        msg = "Which day do you want to see?"
        title = "Pick a day"
        choices = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day = buttonbox(msg, title, choices)
        print_parameter_query("first_name, school_code, parent_first_name, parent_phone, instrument, lesson_time", "day = ? ORDER BY lesson_time", day)
    elif choice == 'Find all students learning a certain instrument':
        msg = "Which instrument do you want to see?"
        title = "Pick an instrument"
        choices = ["Piano", "Guitar", "Drums"]
        instrument = buttonbox(msg, title, choices)
        print_parameter_query("first_name, school_code, parent_first_name, parent_phone, day, lesson_time", "instrument = ? ORDER BY student_info.day_id, lesson_time", instrument)
    elif choice == 'Find all students of a certain gender':
        msg = "Which gender do you want to see?"
        title = "Pick a gender"
        choices = ["Male", "Female", "Not specified"]
        gender = buttonbox(msg, title, choices)
        print_parameter_query("surname, first_name, school_code, instrument, parent_first_name, parent_phone, day, lesson_time", "gender = ? ORDER BY student_info.day_id, lesson_time", gender)
    elif choice == 'Parents who owe the most money':
        print_query('most_owed')
    elif choice == 'Students sorted from oldest to youngest':
        print_query('oldest_to_youngest')
    elif choice == 'All students born in 2008':
        print_query('2008s')
    elif choice == 'All students who are siblings':
        print_query('siblings')
    else:
        break