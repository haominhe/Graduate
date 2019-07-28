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


CREATE_PROCEEDING_IF_NOT_EXISTS = """
        CREATE TABLE IF NOT EXISTS proceeding_table (
            proceeding_id int PRIMARY KEY,
            proceeding_title text,
            author_id list<int>
        )
        """

INSERT_PROCEEDING = """
        INSERT INTO proceeding_table (proceeding_id, proceeding_title, author_id)
        VALUES (?, ?, ?)
        """


def readFile(path): return pd.read_csv(path, header='infer')

def populateTables(session):
    prepared = session.prepare(INSERT_PROCEEDING)

    dblp_dataset = readFile('proceed_table_2004_distinct.csv')
    dblp_proceeding_groups = dblp_dataset.groupby(['proceeding_id'])
    proceeding_title_collection = dblp_proceeding_groups['proceeding_title'].apply(list)
    author_ids_collection = dblp_proceeding_groups['author_id'].apply(list)        

    for key, _ in dblp_proceeding_groups:
        session.execute(prepared, (key, proceeding_title_collection[key][0], author_ids_collection[key]))

def printTables(session):
    future = session.execute_async("SELECT * FROM proceeding_table")
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

    #log.info("creating keyspace...")
    session.execute(CREATE_KEYSPACE)

    #log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)
    
    #log.info("creating table...")
    session.execute(CREATE_PROCEEDING_IF_NOT_EXISTS)

    populateTables(session)
    #printTables(session)


    allproceed = session.execute('select proceeding_id,proceeding_title,author_id from proceeding_table')
    proceedlist = []
    mostauthor = 0
    for each in allproceed:
        if(len(each.author_id) >= mostauthor):
            proceedlist = []
            proceedlist.append(each.proceeding_id)
            proceedlist.append(len(each.author_id))
            proceedlist.append(each.proceeding_title)
            mostauthor = len(each.author_id)
    
    print(proceedlist)



    #log.info("dropping keyspace...")
    #session.execute(DROP_KEYSPACE)

if __name__ == "__main__":
    main()