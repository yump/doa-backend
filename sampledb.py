import sqlite3

num_antennas = 4

def getdb(dbfile, antennaConfigName, numAntennas):
    """Get a sqlite database connection and table name for 
    a particular antenna configuration"""

    global dbcon

    dbcon = sqlite3.connect(dbfile)
    cur = dbcon.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS config("
            "config_name TEXT,"
            "config_id INTEGER"
            ")"
            )
    cur.execute("CREATE TABLE IF NOT EXISTS antenna("
            "config_id INTEGER,"
            "antenna_id INTEGER,"
            "x DOUBLE," 
            "y DOUBLE," 
            "z DOUBLE," 
            "jones_horiz DOUBLE," 
            "jones_vert DOUBLE"
            ")"
            )
    cur.execute("CREATE TABLE IF NOT EXISTS sample("
            "config_id INTEGER,"
            "session_id INTEGER,"
            "sample_id INTEGER,"
            "antenna_id INTEGER,"
            "time DOUBLE,"
            "phase TEXT"
            ")"
            )
    return dbcon

    
