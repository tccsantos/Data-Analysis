import pandas as pd
import argparse
import sys
import codecs
import re
#import emoji

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
    parser.add_argument(
        "-t", "--type", help="Output file type (CSV or GML)", required=True, default=""
    )
    parser.add_argument(
        "-o", "--output", help="Output file name", required=True, default=""
    )

    argument = parser.parse_args()

    if argument.input and argument.output and argument.type:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input, "type": argument.type, "output": argument.output}


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


def escrita(aresta, output, file):
    if file:
        with codecs.open(output + "_citacoes.csv", 'w', encoding='utf-8') as arquivo:
            arquivo.write('"source","target","weight"\n')
            for a in range(len(aresta)):
                user = aresta[a][0][0]
                citado = aresta[a][0][1]
                peso = aresta[a][1]
                arquivo.write(f'{str(user)},{str(citado)},{int(peso)}\n')
    else:
        noh = contnoh(oficial)
        with codecs.open(output + "_citacoes.gml", 'w', encoding='utf-8') as arquivo:
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


def procura(comp, redex, user, tokens):
    suporte = comp.search(tokens)
    tup = redex.sub("", str(suporte.group()))
    return (user, tup)


def contagem(lista):
    c = Counter(lista)
    return c.most_common()


def analise(input):
    df = pd.read_csv(input, lineterminator='\n')
    principal = []
    comp = re.compile("@\\w+")
    limpagem = re.compile(r"[?!@#]")
    ret = re.compile(r"RT @")
    for ind in df.index:
        try:
            word_tokens = ret.sub("", str(df['text'][ind]))
            user = df['username'][ind]
            cit = True
            while cit:
                if not comp.search(word_tokens):
                    cit = False
                    break
                principal.append(procura(comp, limpagem, user, word_tokens))
                word_tokens = comp.sub("", word_tokens, 1)
        except Exception as e:
            print(e)
            pass
    return principal



result = read_options()
if not result.get("success"):
    sys.exit(1)
secundario = analise(result.get("input"))
principal = contagem(secundario)
oficial = []
for ind in range(len(principal)):
    if principal[ind][1] > 5:
        oficial.append(principal[ind])
file = result.get("type").lower()
if file == "gml":
    escrita(oficial, result.get("output"), 0)
else:
    escrita(oficial, result.get("output"), 1)
