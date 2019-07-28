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

QUERY_AUTH_PUBLICATIONS_BY_NAME = """
            SELECT auth_id from auth_publications where auth_name=? ALLOW FILTERING
        """
QUERY_AUTH_PUBLICATIONS_BY_ID = """
            SELECT publ_ids from auth_publications where auth_id=?
        """
QUERY_PUBLICATION_AUTHORS_BY_ID = """
            SELECT auth_ids from publication_authors where pub_id=?
        """

def get_auth_id(auth_name, session):
    auth_publication_query = session.prepare(QUERY_AUTH_PUBLICATIONS_BY_NAME)
    result = session.execute(auth_publication_query, [auth_name])
    return result[0].auth_id

def get_pub_ids(auth_id, session):
    auth_publication_query = session.prepare(QUERY_AUTH_PUBLICATIONS_BY_ID)
    result = session.execute(auth_publication_query, [auth_id])
    return result[0].publ_ids

def get_auth_ids(pub_id, session):
    publication_auths_query = session.prepare(QUERY_PUBLICATION_AUTHORS_BY_ID)
    result = session.execute(publication_auths_query, [pub_id])
    return result[0].auth_ids

def get_coauthors(auth_id, session):
    coauthors = set(())
    publ_of_auth_id = get_pub_ids(auth_id, session)
    for pub_id in publ_of_auth_id:
        authors_of_pub_id = get_auth_ids(pub_id, session)
        coauthors.update(authors_of_pub_id)
    return coauthors    

def get_coauthors_for_authors_list(auth_ids, session):
    coauthors = set(())
    for auth_id in auth_ids:
        coauthors.update(get_coauthors(auth_id, session))
    return coauthors

def get_coauthors_upto_level_3(auth_id, session):
    level_1_coauthors = get_coauthors(auth_id, session)
    level_2_coauthors = get_coauthors_for_authors_list(level_1_coauthors, session) - level_1_coauthors
    level_3_coauthors = get_coauthors_for_authors_list(level_2_coauthors, session) - level_1_coauthors - level_2_coauthors           
    return [(1, level_1_coauthors), (2, level_2_coauthors), (3, level_3_coauthors)]

def get_co_auth_count(auth_name, session):
    auth_id = get_auth_id(auth_name, session)

    coauthor_levels = get_coauthors_upto_level_3(auth_id, session)

    for (level, coauthors) in coauthor_levels:
        print "Level %s Coauthor count : %s" % (level, str(len(coauthors)),)

def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)

    auth_michael_stonebraker = 'Michael Stonebraker'
    auth_David = 'David J. DeWitt'
    
    print("\n")
    print("co-authors count for " + auth_michael_stonebraker)
    get_co_auth_count(auth_michael_stonebraker, session)
    print("\n")
    print("co-authors count for " + auth_David)
    get_co_auth_count(auth_David, session)

if __name__ == "__main__":
    main()
