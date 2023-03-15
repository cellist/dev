#!/usr/bin/env python3
#
# Minimal read-excel-through-pandas demo
# Try:
# ./demo.py pyexcel.xlsx

import pandas as pd
import sys

def dump_excel(xlsx_name):
    spreadsheet = pd.read_excel(xlsx_name)
    print(spreadsheet)
    
if __name__ == '__main__':
    dump_excel(sys.argv[-1])
