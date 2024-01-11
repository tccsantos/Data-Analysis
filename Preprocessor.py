import pandas as pd
import codecs
from csv import reader
import argparse
import re
import itertools
from glob import glob

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
    cita = re.compile("@")
    link = re.compile("http")
    resultado = []
    resultadoh = []
    i = 0
    data.sort()
    data = list(data for data,_ in itertools.groupby(data))
    for rows in data:
        i += 1
        if i%100000 == 0:
            print(i)
        rows = str(rows)
        rows = rows[2:-2]
        if len(rows) < 5:
            continue
        rt = redex.search(rows)
        ht = hashtag.search(rows)
        ct = cita.search(rows)
        lk = link.search(rows)
        # if suporte == None and apoio == None:
        #     if len(rows) > 5:
        #         resultado.append(rows)
        #     continue
        amostra = rows
        if rt:
            sup = rt.span()
            amostra =  rows[:sup[0]]
            if len(amostra) < 5:
                 continue
        if ht:
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
            if len(amostra) < 5:
                 continue
        if ct:
            while True:
                apoio = cita.search(amostra)
                if apoio == None:
                    break
                sup = apoio.span()
                ap = amostra[sup[0]:]
                ap = ap.split()
                amostra = amostra[0:sup[0]] + amostra[sup[0] + len(ap[0]):]
            if len(amostra) < 5:
                 continue
        if lk:
            while True:
                apoio = link.search(amostra)
                if apoio == None:
                    break
                sup = apoio.span()
                ap = amostra[sup[0]:]
                ap = ap.split()
                amostra = amostra[0:sup[0]] + amostra[sup[0] + len(ap[0]):]
            if len(amostra) < 5:
                 continue
        resultado.append(amostra)
    ap = re.compile('…')
    for i in range(len(resultado)):
        resultado[i] = ap.sub("", resultado[i])
    return [resultado, resultadoh]

def escrita(content, outputfile):
    data = content[0]
    for i in range(len(data)):
        data[i] = ' '.join(data[i].split())
    data.sort()
    data = list(data for data,_ in itertools.groupby(data))
    #print(data)
    
    with codecs.open(outputfile + 'processed.csv', 'w', encoding='utf8') as arquivo:
        for row in data:
            #print(row + '\n\n')
            for i in range(len(row)):
                if row[i] != ' ':
                    if len(row[i:]) > 5:
                        arquivo.write(f'"{str(row[i:])}"\n')
                    break
        arquivo.close()
    
    # with codecs.open(outputfile + 'hashtags.csv', 'w', encoding='utf8') as arquivo:
    #     for rows in content[1]:
    #         for row in rows:
    #             arquivo.write(f'{str(row)}\n')
    #     arquivo.close()
    

result = readOptions()
inputfile	=	result.get("input")
outputfile	=	result.get("output")

print('Start')

# arquivo = inputfile + '/*.csv'
# arquivo = sorted(glob(arquivo))
# i = 0
# #print(arquivo)
# for input in arquivo:
with open(inputfile, "r",encoding="utf-8") as read_obj:
        csv_reader = reader(read_obj, delimiter=';')
        #next(csv_reader, None)
        data = list(csv_reader)

print("Data read")

resultado = analise(data)

print('Writing')

escrita(resultado, outputfile)
