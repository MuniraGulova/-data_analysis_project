from connector import set_connection
import pandas as pd

with open('queries/create_tbls.sql') as f:
    query=f.read()

with set_connection() as dc:
    dc.execute(query)
    tables = {
        'Products':'products',
        'Customers':'customers',
        'Orders':'orders',
        'Payment_info':'payment_info',
        'Returns':'returns',
        'Suppliers':'suppliers'
    }
    for table in tables.keys():
        df = pd.read_csv(f'source/{table}.csv')
        dc.query(f"""
            insert into {tables[table]}
            select *
            from df
        """)