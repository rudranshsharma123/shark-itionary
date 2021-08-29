import psycopg2
import numpy
import functools
import operator

conn = psycopg2.connect(
    database='Sharks',
    user='rudransh',
    password='',
    sslmode='require',
    port=26257,
    host='free-tier.gcp-us-central1.cockroachlabs.cloud',
    options="--cluster=shiny-wolf-1947"
)

class cockroachDB():
    def __init__(self, conn):
        self.conn = conn
    
    def create_table(self):
        '''
        It creates the table we would be storing all our data on 
        '''
        
        print("CREATING TABLE>>>>>>>>")
        with self.conn.cursor() as cur:
             cur.execute(
            """CREATE TABLE IF NOT EXISTS Sharks.tested (post_id VARCHAR(255), 
            post_urls VARCHAR(255)
            );"""
        )
        conn.commit()
        print("TABLE IS CREATED>>>>>>")
        return True

    def add_values(self, values:list[list]):
        '''
        It is used to add the values which you pass into the database
        '''
        print(len(values), print(len(values[0])) )
        print(values)
        varlist = [[i[j] for i in values] for j in range(len(values[0]))]
        print(varlist) 
        print("ADDING YOUR VALUES INTO THE TABLE >>>>>>>")
     
        with self.conn.cursor() as cur:
            # varlist = list(values)
            for ind, value in enumerate(varlist):
                j = "'"
                query_string = "UPSERT INTO Memes.tested VALUES (%s);" %", ".join([ j + i + j for i in value]) #had to do this shenanigan because SQL would'nt take the normal python string?
                cur.execute(query_string)
            conn.commit()
        print("YOU VALUES ARE ADDED INTO THE TABLE>>>>>")
        return True
    
    def get_values(self, printing:bool):
        '''
        it is used to get all the values which is stored in the table
        '''
        
        print("GETTING THE VALUES FROM THE TABLE >>>>>>>")
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM Memes.tested")
            rows = cur.fetchall()
            db = []
            for row in rows:
                db.append([str(cell) for cell in row])
                if printing:
                    print([str(cell) for cell in row])
        print("FOUND THE VALUES IN THE TABLE >>>>>>")
        
        return db
    
            


