import constants
import csv
import sqlite3

from sqlite3 import Error

class Database: 

    def __init__(self, db_name=constants.DEFAULT_DATABASE):
        self.db_connection = sqlite3.connect(db_name)
        self.cursor = self.db_connection.cursor()
        self.current_table = constants.DEFAULT_TABLE

        self.create_table(constants.DEFAULT_TABLE)    

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.db_connection.close()

    def commit(self):
        return self.db_connection.commit()

    def user_exists(self, username, show_info=False):
        sql = f''' SELECT * FROM {self.current_table} WHERE username = ? ''' 

        try: 
            self.cursor.execute(sql, (username,))
            row = self.cursor.fetchone()
        except Error as e:
            print(e)
            return 

        if row == None:
            return False

        if show_info:
            print(f'{"ID":^5} | {"NAME":^25} | {"USERNAME":^15} | {"EMAIL":^20} | {"SMB_PATH":^15}')
            print(rf'{row[0]:^5} | {row[1]:^25} | {row[2]:^15} | {row[3]:^20} | {row[4]:^15}')
        
        return True

    def insert_user(self, user_info):
        sql = f''' INSERT INTO '{self.current_table}' (name, username, email, smb_path)
                   VALUES (?, ?, ?, ?)'''
        
        if self.user_exists(user_info[1]):
            print(f"User with the username '{user_info[1]}' already exists.")
            return

        try: 
            self.cursor.execute(sql, user_info)
            print(f"{user_info[0]} has been added successfully.")
            self.commit()
        except Error as e:
            print(e)
            return 
    
    def get_all_users(self):
        sql = f''' SELECT * FROM '{self.current_table}' '''

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Error as e:
            print(e)
            return

    def delete_user(self, username):
        sql = f''' DELETE FROM {self.current_table} 
                  WHERE username = ? '''
        
        try: 
            self.cursor.execute(sql, (username,))
            self.commit()
        except Error as e:
            print(e)
            return

    def table_exists(self, table_name):
        sql = f''' SELECT count(name) FROM sqlite_master 
                  WHERE type='table' and name='{table_name}' '''
                
        self.cursor.execute(sql)
        
        if self.cursor.fetchone()[0]:
            return True

        return False

    def create_table(self, table_name):
        sql = f''' CREATE TABLE IF NOT EXISTS {table_name}(
                   id integer PRIMARY KEY AUTOINCREMENT,
                   name text NOT NULL,
                   username text NOT NULL,
                   email text NOT NULL,
                   smb_path text NOT NULL
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
    
    def drop_table(self, table_name):
        sql = f''' DROP TABLE {table_name} '''

        if table_name == constants.DEFAULT_TABLE or table_name == 'sqlite_sequence':
            print("You cannot delete this table.")
            return
        
        try: 
            self.cursor.execute(sql) 
            self.commit()
        except Error as e:
            print(e)
        
    def switch_table(self, table_name=constants.DEFAULT_TABLE):
        sql = f''' SELECT name FROM sqlite_master 
                   WHERE type = 'table' and name != 'sqlite_sequence' 
                   ORDER BY name '''

        try: 
            self.cursor.execute(sql)
            tables = self.cursor.fetchall()

            if (table_name,) in tables:
                self.current_table = table_name

            return True
        except Error as e:
            print(e)
            return False

    def display_table(self): 
        sql = f''' SELECT * FROM {self.current_table} '''

        try: 
            self.cursor.execute(sql)
            users = self.cursor.fetchall()
        except Error as e:
            print(e)
            return 

        if len(users) == 0:
            print(f"'{self.current_table}' is empty")
            return
        
        print(f'{"ID":^5} | {"NAME":^25} | {"USERNAME":^15} | {"EMAIL":^20} | {"SMB_PATH":^15}')
        for user in users:
            print(rf'{user[0]:^5} | {user[1]:^25} | {user[2]:^15} | {user[3]:^20} | {user[4]:^15}')
        
        print()

    def load_csv(self, filename):
        try: 
            with open(filename) as users_file: 
                reader = csv.DictReader(users_file)

                for row in reader:
                    self.insert_user((row['NAME'], row['USERNAME'], row['EMAIL'], row['SMB_PATH']))

        except FileNotFoundError:    
            print(rf'{filename} not found')
        except KeyError:
            print("File must be a CSV, Check csv column headers.")
            print("Headers should be NAME,USERNAME,EMAIL,SMB_PATH")
