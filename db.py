import csv
import sqlite3

from sqlite3 import Error

class Database: 

    def __init__(self, db_name='address_book_database'):
        self.db_connection = sqlite3.connect(db_name)
        self.cursor = self.db_connection.cursor()
        self.current_table = ""
                
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.db_connection.close()

    def commit(self):
        return self.db_connection.commit()

    def table_exists(self, table_name):
        sql = f'''SELECT count(name) FROM sqlite_master WHERE type='table' and name={table_name} '''


        if self.cursor.fetchone() == None:
            return False

        return True

    def create_table(self, table_name="main_address_table"):
        sql = f''' CREATE TABLE IF NOT EXISTS {table_name}(
            id integer PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            username text NOT NULL,
            email text NOT NULL,
            smb_folder_path text NOT NULL
        ); '''
        
        if self.table_exists(table_name):
            print(f"{table_name} table already exists.")
            return
        
        try: 
            self.cursor.execute(sql)
            print(f"{table_name} created successfully.")
            self.current_table = table_name
        except Error as e:
            print(e)
    
    def user_exists(self, username):
        sql = f''' SELECT * FROM {self.current_table} WHERE username=?''' 

        self.cursor.execute(sql, (username,))
        row = self.cursor.fetchone()

        if row == None:
            return False

        return True

    def insert_user(self, user_info):
        sql = f'''INSERT INTO 'test_table' (name, username, email, smb_folder_path)
                  VALUES (?, ?, ?, ?)'''
        
        if self.user_exists(user_info[1]):
            print(f"User with the username '{user_info[1]}' already exists.")
            return

        try: 
            self.cursor.execute(sql, user_info)
            print(f"{user_info[0]} has been added successfully.")
        except Error as e:
            print(e)
        
        self.commit()

    def display_table(self): 
        print(f"Current table: {self.current_table}")
        sql = f''' SELECT * FROM {self.current_table} '''

        self.cursor.execute(sql)
        users = self.cursor.fetchall()

        if len(users) == 0:
            print(f"{self.current_table} is empty")
            return
        
        print(f'{"ID":^5} | {"NAME":^25} | {"USERNAME":^15} | {"EMAIL":^20} | {"PATH":^15}')
        for user in users:
            print(rf'{user[0]:^5} | {user[1]:^25} | {user[2]:^15} | {user[3]:^20} | {user[4]:^15}')