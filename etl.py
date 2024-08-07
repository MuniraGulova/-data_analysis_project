import pandas as pd
from connector import set_connection

def get_data(table_name):
    tbl_name = f'select * from {table_name}'
    with set_connection() as dc:
        return dc.query(tbl_name).to_df()

def read_query(query_name):
    with open(f'queries/{query_name}.sql', 'r') as f:
        return f.read()


def get_data_query(query_name):
    query = read_query(query_name)
    with set_connection() as dc:
        return dc.query(query).to_df()