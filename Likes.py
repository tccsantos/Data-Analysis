import pandas as pd
import argparse
import sys
import codecs
import re

from argparse import RawTextHelpFormatter
from collections import Counter

def read_options():
    status = False

    parser = argparse.ArgumentParser(
        description="Basic Usage", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--input", help="CSV input File", required=True, default=""
    )

    argument = parser.parse_args()

    if argument.input:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input}


def analise(ind, df):
    print(df['username'][ind])
    print(df['text'][ind])
    print(df['like_count'][ind])


def likes(input):
    df = pd.read_csv(input)
    nomes = ['HildaDeSouzaMa1', 'xandevolp', 'josetomazfilho', 'getuliosantana', 'LeiaRachor', 'Doriko8', 'BetoFontes', 'tonytattoo', 'BR100PTRALHAS', 'Irlandaemel']
    for nome in nomes:
        most = 0
        big = -1
        for ind in df.index:
            if df['username'][ind] == nome:
                if int(df['like_count'][ind]) > most:
                    most = int(df['like_count'][ind])
                    big = ind
        analise(big, df)
    return

result = read_options()
if not result.get("success"):
    sys.exit(1)
likes(result.get("input"))