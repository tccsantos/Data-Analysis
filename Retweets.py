import pandas as pd
import csv
import codecs
import re
import argparse
import sys
from collections import Counter

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

def contagem(lista):
    c = Counter(lista)
    return c.most_common()

def analise(input):
    df = pd.read_csv(input)
    limpagem = re.compile(r"[\W]")
    rta = re.compile('RT @')
    resultado = []
    for ind in df.index:
        try:
            if rta.search(str(df['text'][ind])):
                array = rta.split(str(df['text'][ind]))
                names = []
                for i in range(1, len(array)):
                    word_token = array[i].split()
                    word_token = limpagem.sub("", word_token[0])
                    word_token = word_token.lower()
                    if array[i - 1] != '':
                        if not limpagem.search(str(array[i - 1][-1])):
                            continue
                    names.append(word_token)
                    if i == 1: resultado.append((str(df["username"][ind]).lower(), names[0]))
                    else: resultado.append((names[i - 2], names[i - 1]))
        except Exception as e:
            print(e)
            print(ind)
            continue
    return resultado

def contnoh(lista):
    #set()
    apoio1 = []
    apoio2 = []
    for ind in range(len(lista)):
        apoio1.append(lista[ind][0][0])
        apoio2.append(lista[ind][0][1])
    apoio = apoio1 + apoio2
    c = Counter(apoio)
    sup = c.most_common()
    final = []
    for i in range(len(sup)):
        final.append(sup[i][0])
    return final

def escrita(output, aresta):
    noh = contnoh(aresta)
    with codecs.open(output + "_retweets.gml", 'w', encoding='utf-8') as arquivo:
        arquivo.write("graph\n[\n")
        for ind in range(len(noh)):
            node = noh[ind]
            arquivo.write(f'\tnode\n\t[\n\t\tid {str(node)}\n\t\tlabel "{str(node)}"\n\t]\n')
        for i in range(len(aresta)):
            source = aresta[i][0][0]
            target = aresta[i][0][1]
            weight = aresta[i][1]
            label = f'aresta {str(source)} para {str(target)}'
            arquivo.write(f'\tedge\n\t[\n\t\tsource {str(source)}\n\t\ttarget {str(target)}\n\t\tlabel "{str(label)}"\n\t\tweight {str(weight)}\n\t]\n')
        arquivo.write("]")

#Somente CSV por enquanto
result = read_options()
if not result.get("success"):
    sys.exit(1)
resultado = analise(result.get("input"))
processo = contagem(resultado)
escrita(result.get("output"), processo)
