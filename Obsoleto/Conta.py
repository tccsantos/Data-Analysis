import datetime as dt
import argparse
import sys
import pandas as pd

from argparse import RawTextHelpFormatter


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


result = read_options()
if not result.get("success"):
    sys.exit(1)
inputfile = result.get("input")
df = pd.read_csv(inputfile)
ref = dt.date(2000, 1, 1)
wordlist = []
helper = None
for ind in df.index:
    try:
        nome = df['username'][ind]
        if nome != helper:
            helper = nome
            suporte = []
            sup = df['user_created_at'][ind]
            dia = dt.date(int(sup[0:4]), int(sup[5:7]), int(sup[8:10]))
            delta = dia - ref
            delta = delta.days
            suporte.append(delta)
            suporte.append(nome)
            wordlist.append(suporte)
    except Exception as e:
        print(e)
        pass
print('Contas mais recentes:')
wordlist.sort(reverse=True)
print(wordlist[:10])
