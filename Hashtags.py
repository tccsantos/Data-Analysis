import codecs
from csv import reader
import argparse
import re
from glob import glob
from collections import Counter
import re

from argparse import RawTextHelpFormatter


def	readOptions():

    status = False

    parser = argparse.ArgumentParser(description = "Basic Usage",formatter_class=RawTextHelpFormatter)
    parser.add_argument("-i"	,	"--input"		, help = "CSV input File"		, required = True	, default = "")
    parser.add_argument("-o"	,	"--output"		, help = "CSV input File"		, required = True	, default = "")
    argument = parser.parse_args()

    if argument.input and argument.output:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False 

    return {"success":status, "input":argument.input, "output":argument.output}

def contagem(lista):
    c = Counter(lista)
    return c.most_common()

def analise(data, redex):
    with open(data, "r",encoding="utf-8") as read_obj:
        csv_reader = reader(read_obj, delimiter=';')
        #next(csv_reader, None)
        arquivo = list(csv_reader)
    resultado = []
    total = 0
    for row in arquivo:
        row = str(row)
        row = row[2:-2]
        while True:
            suporte = redex.search(row)
            if suporte == None:
                break
            suporte = suporte.span()
            suporte = row[suporte[0]:].split()
            resultado.append(suporte[0].lower())
            total += 1
            row = redex.sub('', row, 1)
    return resultado, total

def escrita(output, data, total):
    with codecs.open(output + 'hashtags.csv', 'w', encoding='utf8') as arquivo:
        arquivo.write(f'"Hashtag";"Score";"Proportion"\n')
        limpagem = re.compile(r"[\W]")
        for tup in data:
             if not limpagem.search(str(tup[0][1:])):
                arquivo.write(f'{str(tup[0])};{str(tup[1])};{str("{:.3f}%".format(tup[1]/total*100))}\n')
        arquivo.close()
        print('end')


result = readOptions()
inputfile	=	result.get("input")
outputfile = result.get("output")

arquivos = inputfile + '/*.csv'
#print(arquivo)
arquivos = sorted(glob(arquivos))
redex = re.compile('#')
for arquivo in arquivos:
    reps, total = analise(arquivo, redex)
    reps = contagem(reps)
    escrita(arquivo[:-9], reps, total)
