import pandas as pd
import codecs
from csv import reader
import argparse
import datetime as dt
import re
from tld import get_tld
import pickle

from argparse import RawTextHelpFormatter


def get_domain(url):
    """
    Extrat the domain of a URL
    Arguments:
        url: a string
    Returns:
        return the domain
    """
    try:
        res = get_tld(url, as_object=True)
        if res.subdomain and res.subdomain != "www":
            return {
                "sub": True,
                "subdomain": res.subdomain + "." + res.fld,
                "domain": res.fld,
            }
        return {"sub": False, "domain": res.fld}
    except Exception as error:
        print(error)

    return {}

def	readOptions():

	status = False

	parser = argparse.ArgumentParser(description = "Basic Usage",formatter_class=RawTextHelpFormatter)
	#parser.add_argument("-i"	,	"--input"		, help = "CSV input File"		, required = True	, default = "")
	parser.add_argument("-o"	,	"--output"		, help = "Output file name"		, required = True	, default = "")
	parser.add_argument("-d"	,	"--dataframe"	, help = "dataframe file name"	, required = True	, default = "")
	parser.add_argument("-p"	,	"--pickledict"	, help = "pickle dictonary file name"	, required = True	, default = "")

	argument = parser.parse_args()

	if argument.output and argument.dataframe and argument.pickledict:
		status = True

	if not status:
		print("Maybe you want to use -h for help")
		status = False 

	return {"success":status, "output":argument.output, "dataframe":argument.dataframe, "pickle":argument.pickledict}

def analise(link, resultado, df):
	ref = dt.date(2010, 1, 1)
	redex = re.compile("http")
	filtro = re.compile("…")
	df = pd.read_csv(df)
	print('df read')
	#busca os urls no dataframe
	for ind in df.index:
		if ind%500 == 0:
			print(ind)
		words = str(df['expanded_url'][ind])
		cit = True
		while cit:
			#laço infinito!!!!!!
			suporte = redex.search(words)
			if suporte == None:
				cit = False
				break
			sup = suporte.span()
			amostra =  words[sup[0]:]
			amostra = amostra.split()
			url = amostra[0].split(sep=',')[0]
			if filtro.search(url) != None:
				continue

			#Faz a analise da data do url
			sup = df['user_created_at'][ind]
			dia = dt.date(int(sup[0:4]), int(sup[5:7]), int(sup[8:10]))
			url = link.get(url)
			today = resultado.get(url)
			if today == None:
				continue
			if (today[0] - ref).days > (dia - ref).days:
				resultado[url][0] = dia
			if (today[1] - ref).days < (dia - ref).days:
				resultado[url][1] = dia
			words = redex.sub("", words, 1)
	return resultado

def escrita(resultado, outputfile, ref):
	with codecs.open(outputfile + '_urlstime.csv', 'w', encoding='utf8') as arquivo:
		arquivo.write('"link","first","duration","last"')
		for key, values in resultado.items():
			duration = (values[1] - values[0]).days
			arquivo.write(f'{str(key)},{str(values[0])},{str(duration)},{str(values[1])}\n')
		arquivo.close()
	
	print('First over')

	domains = {}
	for key, value in resultado.items():
		domain = get_domain(key).get("domain")
		domains[domain] = value
	resultado = None

	sup = {}
	for key, value in domains.items():
		new = sup.get(key)
		if new:
			sup[key] = value
		else:
			if (new[0] - ref).days > (value[0] - ref).days:
				sup[key][0] = value[0]
			if (new[1] - ref).days < (value[1] - ref).days:
				sup[key][1] = value[1]
	
	domains = None

	print('Second start')

	with codecs.open(outputfile + '_domainstime.csv', 'w', encoding='utf8') as arquivo:
		arquivo.write('"domain","first","duration","last"')
		for key, value in sup.items():
			duration = (value[1] - value[0]).days
			arquivo.write(f'{str(key)},{str(value[0])},{str(duration)},{str(value[1])}\n')
		arquivo.close()



result = readOptions()
#inputfile	=	result.get("input")
outputfile	=	result.get("output")
# with open(inputfile, 'r') as aba:
# 	csv_reader = reader(aba, delimiter=';')
# 	next(csv_reader, None) 
# 	data = list(csv_reader)
with open(result.get('pickle'), 'rb') as file:
	links = pickle.load(file)
resultado = {}
ref = dt.date(2010, 1, 1)
dia = dt.date(2022, 12, 31)
for key, values in links.items():
	resultado[values] = [dia, ref]

df = result.get("dataframe")
print('Start')
resultado = analise(links, resultado, df)
print("Writing")
escrita(resultado, outputfile, ref)
