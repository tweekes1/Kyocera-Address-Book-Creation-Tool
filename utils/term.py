import os, sys

curr_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(curr_path, "utils"))

import helper
import constants

from cmd import Cmd
from db import Database

class Terminal(Cmd):

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.prompt = self.db.current_table + '> '

    def do_display_table(self, args):
        self.db.display_table()     

    def help_display_table(self):
        print("="*50)
        print("Displays the entries in the current table")
        print("USAGE: display_table\n")

    def do_add(self, args):
        user_info = args.split('|')

        if len(user_info) == self.db.num_of_columns - 1:
            self.db.insert_user(user_info)

        print("="*50)
        print(f"User not added, {len(user_info)} args given {self.db.num_of_columns - 1} needed.")
        print(f"Params need to be separated by '|' \n")    

    def help_add(self):
        print("="*50)
        print("Adds user into current table.")
        print("USAGE: add 'NAME' | 'USERNAME' | 'EMAIL' | 'SMB_PATH'\n")

    def do_find(self, args):
        username = args.split(' ')[0]

        if self.db.user_exists(username, True):
            return
        
        print(f"'{username}' does not exist.")

    def help_find(self):
        print("="*50)
        print("Searches current table for the specified user and displays entry if found.")
        print("USAGE: find USERNAME\n")

    def do_switch(self, args):
        table_name = args.split(' ')[0]

        if self.db.switch_table(table_name): 
            self.prompt = self.db.current_table + "> "
        
    def help_switch(self):
        print("="*50)
        print("Switches the current table to the one specified, if it exists in the database.")
        print("USAGE: switch TABLE_NAME\n")

    def do_load(self, args):
        filename = args.split(' ')[0]

        self.db.load_csv(filename)

    def help_load(self):
        print("="*50)
        print("Loads users from specified csv file into the current table.")
        print("USAGE: load CSV_FILE\n")

    def do_exit(self, args):
        print("Bye!")
        return True
    
    def help_exit(self):
        print("="*50)
        print("Exits the application...")
        print("USAGE: exit\n")
    
    def emptyline(self):
        return