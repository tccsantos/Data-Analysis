import pandas as pd
import codecs
from csv import reader
import argparse
import re

from argparse import RawTextHelpFormatter


def	readOptions():

	status = False

	parser = argparse.ArgumentParser(description = "Basic Usage",formatter_class=RawTextHelpFormatter)
	parser.add_argument("-i"	,	"--input"		, help = "CSV input File"		, required = True	, default = "")
	parser.add_argument("-o"	,	"--output"		, help = "Output file name"		, required = True	, default = "")
	argument = parser.parse_args()

	if argument.output and argument.input:
		status = True

	if not status:
		print("Maybe you want to use -h for help")
		status = False 

	return {"success":status, "output":argument.output, "input":argument.input}

def analise(data):
    redex = re.compile("RT")
    hashtag = re.compile("#")
    resultado = []
    resultadoh = []
    i = 0
    for rows in data:
        i += 1
        if i%100000 == 0:
            print(i)
        rows = str(rows)
        rows = rows[2:-2]
        suporte = redex.search(rows)
        apoio = hashtag.search(rows)
        if suporte == None and apoio == None:
            if len(rows) > 5:
                resultado.append(rows)
            continue
        amostra = rows
        if suporte:
            sup = suporte.span()
            amostra =  rows[:sup[0]]
            if len(amostra) < 5:
                 continue
        if apoio:
            hashs = []
            while True:
                apoio = hashtag.search(amostra)
                if apoio == None:
                    break
                sup = apoio.span()
                ap = amostra[sup[0]:]
                ap = ap.split()
                amostra = amostra[0:sup[0]] + amostra[sup[0] + len(ap[0]):]
                hashs.append(ap[0])
            resultadoh.append(hashs)

        resultado.append(amostra)
    return [resultado, resultadoh]

def escrita(data, outputfile):
    with codecs.open(outputfile + 'processed.csv', 'w', encoding='utf8') as arquivo:
        for row in data[0]:
            arquivo.write(f'{str(row)}\n')
        arquivo.close()
    
    with codecs.open(outputfile + 'hashtags.csv', 'w', encoding='utf8') as arquivo:
        for rows in data[1]:
            for row in rows:
                arquivo.write(f'{str(row)}\n')
        arquivo.close()
    

result = readOptions()
inputfile	=	result.get("input")
outputfile	=	result.get("output")

print('Start')

with open(inputfile, "r",encoding="utf-8") as read_obj:
        csv_reader = reader(read_obj, delimiter=';')
        #next(csv_reader, None)
        data = list(csv_reader)

print("Data read")

resultado = analise(data)

print('Writing')

escrita(resultado, outputfile)
