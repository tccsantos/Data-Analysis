import pandas as pd
import argparse
import sys
import codecs
#import re


from argparse import RawTextHelpFormatter
#from collections import Counter



def read_options():
    status = False

    parser = argparse.ArgumentParser(
        description="Basic Usage", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--input", help="CSV input File", required=True, default=""
    )

    parser.add_argument(
        "-o", "--output", help="CSV output File", required=True, default=""
    )

    argument = parser.parse_args()

    if argument.input and argument.output:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input, "output": argument.output}


def dicts(df):
    nomes = {}
    for ind in df.index:
        sup = nomes.get(df['username'][ind])
        if sup == None:
            nomes[df['username'][ind]] = 0
    return nomes


def ret(df):
    nomes = dicts(df)
    resultado = dicts(df)
    for ind in df.index:
        if nomes.get(df['username'][ind]) < df['retweet_count'][ind]:
            resultado[df['username'][ind]] = ind
            nomes[df['username'][ind]] = df['retweet_count'][ind]
    return resultado, nomes


def escrita(outputfile, result, nomes, df):
    with codecs.open(outputfile, 'w', encoding= 'utf8') as arquivo:
        arquivo.write('"username";"retweet_count";"text"\n')
        for key, values in result.items():
            sup = nomes.get(key)
            apoio = df['text'][values]
            arquivo.write(f'{str(key)};{str(sup)};"{str(apoio)}"\n')
        arquivo.close()


def main():
    result = read_options()
    if not result.get("success"):
        sys.exit(1)
    df = pd.read_csv(result.get("input"), sep=';')
    resultado, nomes = ret(df)
    escrita(result.get("output"), resultado, nomes, df)



if __name__ == '__main__':
    main()
