import codecs
from csv import reader
import argparse
import re
from glob import glob
from collections import Counter

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
    for row in arquivo:
        row = str(row)
        row = row[2:-2]
        while True:
            suporte = redex.search(row)
            if suporte == None:
                break
            suporte = suporte.span()
            suporte = row[suporte[0]:].split()
            resultado.append(suporte[0])
            row = redex.sub('', row, 1)
    return resultado

def escrita(name, output, data):
    with codecs.open(name + '/' + output[-16:-4] + 'hashtags.csv', 'w', encoding='utf8') as arquivo:
        suporte = None
        arquivo.write(f'"Hashtag";"Score"\n')
        for tup in data:
             arquivo.write(f'{str(tup[0])};{str(tup[1])}\n')
             suporte = tup
        if suporte: print(suporte[0])
        arquivo.close()


result = readOptions()
inputfile	=	result.get("input")
outputfile = result.get("output")

arquivos = inputfile + '/*.csv'
#print(arquivo)
arquivos = sorted(glob(arquivos))
redex = re.compile('#')
for arquivo in arquivos:
    reps = analise(arquivo, redex)
    reps = contagem(reps)
    escrita(outputfile, arquivo, reps)
