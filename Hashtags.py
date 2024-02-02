import codecs
import argparse
import re


from glob import glob
from csv import reader
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


def pasta(pasta):
    arquivo = pasta + '/*.csv'
    #print(arquivo)
    return sorted(glob(arquivo))


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
    with codecs.open(output + '_hashtags.csv', 'w', encoding='utf8') as arquivo:
        arquivo.write(f'"Hashtag";"Score";"Proportion"\n')
        limpagem = re.compile(r"[\W]")
        for tup in data:
             if not limpagem.search(str(tup[0][1:])):
                arquivo.write(f'{str(tup[0])};{str(tup[1])};{str("{:.3f}%".format(tup[1]/total*100))}\n')
        arquivo.close()
        print('end')


def main():
    result = readOptions()
    inputfile	=	result.get("input")
    outputfile = result.get("output")
    arquivos = pasta(inputfile)
    redex = re.compile('#')
    for arquivo in arquivos:
        reps, total = analise(arquivo, redex)
        reps = contagem(reps)
        print(arquivo[24:-12])
        escrita(outputfile + '/' + arquivo[24:-12], reps, total)



if __name__ == '__main__':
    main()
