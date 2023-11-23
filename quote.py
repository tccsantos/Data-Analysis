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
    print(df['quote_count'][ind])


def likes(input):
    df = pd.read_csv(input)
    nomes = ['HildaDeSouzaMa1', 'xandevolp', 'josetomazfilho', 'getuliosantana', 'LeiaRachor', 'Doriko8', 'BetoFontes', 'tonytattoo', 'BR100PTRALHAS', 'Irlandaemel']
    for nome in nomes:
        most = 0
        big = -1
        for ind in df.index:
            if df['username'][ind] == nome:
                if int(df['quote_count'][ind]) > most:
                    most = int(df['quote_count'][ind])
                    big = ind
        if big != -1:
            analise(big, df)
        else:
            print('sem postagens: ' +  nome)
    return

result = read_options()
if not result.get("success"):
    sys.exit(1)
likes(result.get("input"))