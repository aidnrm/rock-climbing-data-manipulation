import sqlite3
import pandas as pd
import os

class DBOperation:
    def __init__(self):
        #Create the connection to the database
        self.conn = sqlite3.connect('climbing.db')
        #Create the cursor object
        self.cursor = self.conn.cursor()
        
    def loadData(self):
        #Create tables and add data
        self.createTables()
        self.readCsvToTable('aggregate.csv', 'climb')
        self.readCsvToTable('byArea.csv', 'area')
        self.readCsvToTable('states.csv', 'state')

        #Commit changes to the database
        self.conn.commit()

    def createTables(self):
        self.cursor.execute('''
              CREATE TABLE IF NOT EXISTS climb
              (
                ST VARCHAR(255) PRIMARY KEY,
                Climbs INTEGER,
                Crags VARCHAR(255),
                Aid INTEGER,
                Alpine INTEGER,
                Boulder INTEGER,
                Ice INTEGER,
                Mixed INTEGER,
                Sport INTEGER,
                Toprope INTEGER,
                Trad INTEGER
              );
              ''')
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS area
                (
                    Numb INTEGER,
                    Crags VARCHAR(255),
                    Climbs INTEGER,
                    ST VARCHAR(255),
                    CONSTRAINT fk_ST
                        FOREIGN KEY (ST)
                        REFERENCES climb(ST)
                );
                ''')
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS state
                (
                    ST VARCHAR(255),
                    num INTEGER,
                    type VARCHAR(255),
                    CONSTRAINT fk_num
                        FOREIGN KEY (num)
                        REFERENCES area(Numb)
                );
                ''')

    def readCsvToTable(self, filename, tablename):
        #Read the csv file as a pandas dataframe
        path = os.path.join('backend', filename)
        dataFrame = pd.read_csv(path)
        #This call takes the dataframe created above and loads it into the correct table
        dataFrame.to_sql(tablename, self.conn, if_exists='replace', index=False)
    

