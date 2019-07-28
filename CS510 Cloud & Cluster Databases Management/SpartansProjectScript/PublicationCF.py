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

CREATE_PUBLICATIONS_IF_NOT_EXISTS = """
        CREATE TABLE IF NOT EXISTS publication_details (
            pub_id int PRIMARY KEY,
            auth_id list<int>,
            pub_type text,
            title text
        )
        """

INSERT_PUBLICATIONS = """
        INSERT INTO publication_details (pub_id, auth_id, pub_type, title )
        VALUES (?, ?, ?, ?)
        """

def readFile(path): return pd.read_csv(path, header='infer')

def populateTables(session):
    prepared = session.prepare(INSERT_PUBLICATIONS)

    dblp_dataset = readFile('publication_table.csv')
    dblp_publication_groups = dblp_dataset.groupby(['publication_id'])
    auth_ids_collection = dblp_publication_groups['author_id'].apply(list)    
    publication_type_collection = dblp_publication_groups['publication_type'].apply(list)
    title_collection = dblp_publication_groups['title'].apply(list)

    for key, _ in dblp_publication_groups:
        session.execute(prepared, (key, auth_ids_collection[key], publication_type_collection[key][0], title_collection[key][0]))
        # session.execute(prepared, (key, [], "hi", "hello"))

def printTables(session):
    future = session.execute_async("SELECT * FROM publication_details")
    log.info("key\tcol1\tcol2\tcol3")
    log.info("---\t----\t----\t----")

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
    session.execute(CREATE_PUBLICATIONS_IF_NOT_EXISTS)

    populateTables(session)
    printTables(session)
    
    log.info("dropping keyspace...")
    #session.execute(DROP_KEYSPACE)

if __name__ == "__main__":
    main()