import os, sys

curr_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(curr_path, "utils"))

import utils.helper as helper
from utils.db import Database
from cmd import Cmd

class Terminal(Cmd):

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.prompt = self.db.current_table + '> '

    def do_display_table(self, args):
        self.db.display_table()

    def do_find(self, args):
        username = args.split(' ')[0]

        if self.db.user_exists(username, True):
            return
        
        print(f"'{username}' does not exist.")

    def do_switch(self, args): 
        table_name = args.split(' ')[0]

        if self.db.switch_table(table_name): 
            self.prompt = self.db.current_table + "> "
        
    def do_load(self, args):
        filename = args.split(' ')[0]

        self.db.load_csv(filename)

    def do_exit(self, args):
        print("Bye!")
        return True

    
    def emptyline(self):
        return