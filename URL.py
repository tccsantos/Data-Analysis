import pandas as pd
import argparse
import sys
import codecs
import re

from argparse import RawTextHelpFormatter
#from collections import Counter

def escrita(outputfile, top):
    with codecs.open(outputfile + "_URL.csv", 'w', encoding='utf-8') as arquivo:
        for a in range(len(top)):
            suporte = top[a]
            arquivo.write(f'{str(suporte)}\n')
        arquivo.close()


def busca(inputfile):
    df = pd.read_csv(inputfile)
    redex = re.compile("http")
    urllist = []
    for ind in df.index:
        text = str(df["expanded_url"][ind])
        cit = True
        while cit:
            suporte = redex.search(text)
            if suporte == None:
                cit = False
                break
            sup = suporte.span()
            amostra =  text[sup[0]:]
            amostra = amostra.split()
            url = amostra[0].split( sep=',')
            urllist.append(url[0])
            text = redex.sub("", text, 1)
    return urllist


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


result = read_options()
if not result.get("success"):
    sys.exit(1)
outputfile = result.get("output")
inputfile = result.get("input")
urllist = busca(inputfile)
escrita(outputfile, urllist)
