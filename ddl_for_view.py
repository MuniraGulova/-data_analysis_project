from connector import set_connection
import pandas as pd

with open('queries/create_views.sql') as f:
    query=f.read()

with set_connection() as dc:
    dc.execute(query)