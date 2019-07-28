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

CREATE_AUTH_PUBLICATIONS_IF_NOT_EXISTS = """
        CREATE TABLE IF NOT EXISTS auth_publications (
            auth_id int PRIMARY KEY,
            auth_name text,
            publ_ids list<int>
        )
        """

INSERT_AUTH_PUBLICATIONS = """
        INSERT INTO auth_publications (auth_id, auth_name, publ_ids)
        VALUES (?, ?, ?)
        """


def readFile(path): return pd.read_csv(path, header='infer')

def populateTables(session):
    prepared = session.prepare(INSERT_AUTH_PUBLICATIONS)

    dblp_dataset = readFile('author_table.csv')
    dblp_authors_groups = dblp_dataset.groupby(['author_id'])
    publ_ids_collection = dblp_authors_groups['publication_id'].apply(list)    
    #print(publ_ids_collection)
    author_name_collection = dblp_authors_groups['author_name'].apply(list)
    #print(author_name_collection)

    for key, _ in dblp_authors_groups:
        session.execute(prepared, (key, author_name_collection[key][0],publ_ids_collection[key]))

def printTables(session):
    future = session.execute_async("SELECT * FROM auth_publications")
    log.info("key\tcol1\tcol2")
    log.info("---\t----\t----")

    try:
        rows = future.result()
    except Exception:
        log.exception("Error reading rows:")
        return

    for row in rows:
        # log.info('\t'.join(str(row)))
        print(row)
        print("\n")


def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    log.info("creating keyspace...")
    session.execute(CREATE_KEYSPACE)

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)
    
    log.info("creating table...")
    session.execute(CREATE_AUTH_PUBLICATIONS_IF_NOT_EXISTS)

    populateTables(session)
    printTables(session)
    
    #log.info("dropping keyspace...")
    #session.execute(DROP_KEYSPACE)

if __name__ == "__main__":
    main()