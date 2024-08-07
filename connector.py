import duckdb
def set_connection():
    credentials='my.db'
    return duckdb.connect(credentials)