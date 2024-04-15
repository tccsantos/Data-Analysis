import pandas as pd
import argparse
import sys
import io
import re

from argparse import RawTextHelpFormatter


def read_options():
    status = False

    parser = argparse.ArgumentParser(
        description="Basic Usage", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--input", help="CSV input File", required=True, default=""
    )
    parser.add_argument(
        "-o", "--output", help="Output file name", required=True, default=""
    )

    argument = parser.parse_args()

    if argument.input and argument.output:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input, "output": argument.output}


def escrita(output, lista):
    with io.open(output + "_adaptado.csv", 'w', encoding='utf8') as arquivo:
        arquivo.write('username,text,created_at\n')
        for ind in range(len(lista)): 
            arquivo.write(str(lista[ind][0]) + ",")
            arquivo.write(str(lista[ind][1]) + " " + str(lista[ind][2]) + ",")
            arquivo.write(str(lista[3]) + "\n")


def slice(input):
    df = pd.read_csv(input)
    lista = []
    redex = re.compile(r"[\n,\t,\r]")
    for ind in df.index:
        suporte = []
        user = str(df["User Name"][ind])
        user = redex.sub(" ", user)
        suporte.append(user)
        text = str(df["Description"][ind])
        text = redex.sub(" ", text)
        suporte.append(text)
        image = str(df["Image Text"][ind])
        image = redex.sub(" ", image)
        suporte.append(str(image))
        suporte.append(str(df["Post Created Date"][ind]))
        lista.append(suporte)
    return lista
    


result = read_options()
if not result.get("success"):
    sys.exit(1)
lista = slice(result.get("input"))
escrita(result.get("output"), lista)
