import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self, db_params):
        self.connection = psycopg2.connect(**db_params)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def execute_insert(self, query, values=None):
        self.cursor.execute(query, values)
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
