import pandas as pd
import codecs
import argparse
import datetime as dt
import re


from argparse import RawTextHelpFormatter
from csv import reader



def	readOptions():

	status = False

	parser = argparse.ArgumentParser(description = "Basic Usage",formatter_class=RawTextHelpFormatter)
	parser.add_argument("-i"	,	"--input"		, help = "CSV input File"		, required = True	, default = "")
	parser.add_argument("-o"	,	"--output"		, help = "Output file name"		, required = True	, default = "")
	parser.add_argument("-ii"	,	"--input2"	, help = "dataframe file name"	, required = True	, default = "")

	argument = parser.parse_args()

	if argument.output and argument.input2 and argument.input:
		status = True

	if not status:
		print("Maybe you want to use -h for help")
		status = False 

	return {"success":status, "output":argument.output, "time":argument.input, "score":argument.input2}

def read(timefile, scorefile):
    """
    Read the file that contains the lifespan of a link
    and the file which contains the score of the link
    Arguments:
        Their directories
    Returns:
        Their contents in dictionary format
    """
    with open(timefile, 'r', encoding="utf-8") as aba:
        csv_reader = reader(aba, delimiter=';')
        next(csv_reader, None) 
        timelist = list(csv_reader)
    
    time = {}
    for row in timelist:
        sup = str(row[0]).lower()
        time[sup] = [str(row[1]), str(row[2]), str(row[3])]
    
    
    with open(scorefile, 'r', encoding="utf-8") as sup:
        csv_reader = reader(sup, delimiter=';')
        next(csv_reader, None) 
        scorelist = list(csv_reader)
    
    score = {}
    for row in scorelist:
        sup = str(row[0]).lower()
        score[sup] = str(row[1])
    
    
    return time, score

def analise(time, score):
    """
    Mix their contents in a single list, containing
    their lifespan and score
    
    Arguments:
        Both Dictionaries
    Returns:
        A list of lists of all the content
    """
    resultado = []
    i = 0
    for key, values in time.items():
        apoio = score.get(key)
        if apoio:
            suporte = [key, values[0], values[1], values[2], apoio]
            resultado.append(suporte)
        else:
            print('erro')
            print(key)
            i += 1
            if i > 10000:
                break
    
    return resultado

def escrita(resultado, outputfile):
    """
    Write the content of the resulting list

    Arguments:
        The list with all the info
    """
    with codecs.open(outputfile + '_full.csv', 'w', encoding='utf8') as arquivo:
        arquivo.write('"link","first","duration","last","score"\n')
        for row in resultado:
            arquivo.write(f'"{str(row[0])}",{str(row[1])},{str(row[2])},{str(row[3])},{str(row[4])}\n')
        arquivo.close()
            
def main():
    result = readOptions()
    timefile	=	result.get("time")
    outputfile	=	result.get("output")
    scorefile = result.get("score")

    print('Reading')
    time, score = read(timefile, scorefile)
    print('Start')
    resultado = analise(time, score)
    print('Writing')
    escrita(resultado, outputfile)


if __name__ == "__main__":
    main()
