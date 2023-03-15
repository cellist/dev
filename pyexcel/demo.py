#!/usr/bin/env python3
#
# Simple insert-excel-into-sqlite demo
# using pandas and sqlalchemy
#
# Try:
# ./demo.py pyexcel.xlsx

from  sqlalchemy import create_engine
import pandas as pd
import sys

def print_table_meta(resultproxy):
    for rowproxy in resultproxy:
        for column, value in rowproxy.items():
            print(f'col: {column:10s} - val: {str(value):s}')
            
def excel_to_db(xlsx_name):
    spreadsheet = pd.read_excel(xlsx_name)
    engine = create_engine('sqlite://', echo=False)
    spreadsheet.to_sql('pyexcel',
                       con=engine,
                       if_exists='replace',
                       index_label='id')
    print_table_meta(engine.execute("PRAGMA table_info(pyexcel)"))
    print(engine.execute("SELECT * FROM pyexcel ORDER BY Wert,Name").fetchall())
    
if __name__ == '__main__':
    excel_to_db(sys.argv[-1])
