import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "caps.db"

    sql_create_wlan_table = """CREATE TABLE wlan (
	wlan_id                 INTEGER        PRIMARY KEY,
    wlan_radio_channel      INTEGER,
    wlan_radio_signal_dbm   INTEGER,
    wlan_ta                 TEXT,
    wlan_da                 TEXT, 
    wlan_ra                 TEXT, 
    wlan_bssid              TEXT,
    wlan_ta_resolved        TEXT,
    wlan_da_resolved        TEXT,
    wlan_ra_resolved        TEXT,
    wlan_bssid_resolved     TEXT,
    frame_time              TEXT,
    frame_time_epoch        TEXT
    );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        print("Creating WLAN table.")
        create_table(conn, sql_create_wlan_table)
        
    else:
        print("Error! cannot create the database connection.")

    sql_create_mac_table = """CREATE TABLE mac (
    mac_id TEXT UNIQUE PRIMARY KEY,
    first_seen TEXT,
    mac_resolved TEXT
    );"""

    # create tables
    if conn is not None:
        # create projects table
        print("Creating MAC table.")
        create_table(conn, sql_create_mac_table)
        
    else:
        print("Error! cannot create the database connection.")        

    sql_create_talkingto_table = """CREATE TABLE talkingto (
    mac_sender TEXT PRIMARY KEY,
    mac_receiver TEXT,
    mac_sender_resolved TEXT,
    mac_receiver_resolved TEXT,
    wlan_radio_channel TEXT,
    wlan_radio_signal_dbm TEXT,
    first_talked TEXT,
    UNIQUE(mac_sender, mac_receiver)
    );"""

    # create tables
    if conn is not None:
        # create projects table
        print("Creating TalkingTo table.")
        create_table(conn, sql_create_talkingto_table)
        
    else:
        print("Error! cannot create the database connection.")        

if __name__ == '__main__':
    main()