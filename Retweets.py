import pandas as pd
import csv
import re
import argparse
import sys

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


def contagem(input, output):
    df = pd.read_csv(input)
    limpagem = re.compile("\W")
    rta = re.compile('RT @')
    for ind in df.index:
        with open(output + '_rt.csv', 'a', newline='') as arquivo:
            writer = csv.writer(arquivo)
            try:
                if rta.search(str(df['text'][ind])):
                    array = rta.split(str(df['text'][ind]))
                    for i in range(1, len(array)):
                        word_token = array[i].split()
                        word_token = limpagem.sub("", word_token[0])
                        writer.writerow((df["username"][ind],word_token))
            except Exception as e:
                print(e)
                break

#Somente CSV por enquanto
result = read_options()
if not result.get("success"):
    sys.exit(1)
contagem(result.get("input"), result.get("output"))
