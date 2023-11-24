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
	argument = parser.parse_args()

	if argument.input:
		status = True

	if not status:
		print("Maybe you want to use -h for help")
		status = False 

	return {"success":status, "input":argument.input}

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

def escrita(output, data):
    with codecs.open(output[:-4] + 'hashtags.csv', 'w', encoding='utf8') as arquivo:
        for tup in data:
             arquivo.write(f'{str(tup[0])},{str(tup[1])}\n')
        arquivo.close()


result = readOptions()
inputfile	=	result.get("input")

arquivos = inputfile + '/*.csv'
#print(arquivo)
arquivos = sorted(glob(arquivos))
redex = re.compile('#')
for arquivo in arquivos:
    reps = analise(arquivo, redex)
    reps = contagem(reps)
    escrita(arquivo, reps)
