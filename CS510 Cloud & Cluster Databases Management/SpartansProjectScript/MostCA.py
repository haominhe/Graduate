# CS 510 Cloud and Cluster Data Management
# Fall 2018
# Team Spartans: 
# Punam Pal
# Haomin He
# Pallavi Gusain
# Yokesh Thirumoorthi

import logging

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

import pandas as pd
from cassandra.cluster import Cluster
pd.set_option('expand_frame_repr', True)

KEYSPACE = "dblp"

CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE

DROP_KEYSPACE = "DROP KEYSPACE " + KEYSPACE        

     
def printTables(session):
    auth = session.execute('select pub_id,auth_id,pub_type,title from publication_details')
    mostcoauthors =[]
    mostauthors = 0 
    for each in auth:
        if(len(each.auth_id ) >= mostauthors):
            mostcoauthors = []
            mostcoauthors.append(each.pub_id)
            mostcoauthors.append(len(each.auth_id))
            mostcoauthors.append(each.pub_type)
            mostcoauthors.append(each.title)
            mostauthors = len(each.auth_id)

    print(mostcoauthors)        
  
def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    log.info("creating keyspace...")
    session.execute(CREATE_KEYSPACE)

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)
    
   # log.info("creating table...")
   # session.execute(CREATE_PUBLICATIONS_IF_NOT_EXISTS)

   # populateTables(session)
    printTables(session)
    
    log.info("dropping keyspace...")
    #session.execute(DROP_KEYSPACE)

if __name__ == "__main__":
    main()