# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'music_lessons.db'

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
                        '4: All students who have a lesson on Monday, from earliest to latest\n'
                        '5: All students who have a lesson on Wednesday, from earliest to latest\n'
                        '6: All students who\'s learning the piano\n'
                        '7: All male students\n'
                        '8: Parents who owe the most money\n'
                        '9: Students sorted from oldest to youngest\n'
                        '10: All students born in 2008\n'
                        'EXIT: To exit the menu\n\n'
                        'Type option here: ')
    menu_choice = menu_choice.upper()