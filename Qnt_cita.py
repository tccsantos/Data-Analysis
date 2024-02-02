import pandas as pd
import re
import argparse
import sys
import codecs

from argparse import RawTextHelpFormatter
from glob import glob



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
    parser.add_argument(
        "-n", "--names", help="Bots names file", required=True, default=""
    )

    argument = parser.parse_args()

    if argument.input and argument.output and argument.names:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input, "output": argument.output, "names": argument.names}


def pasta(pasta):
    arquivo = pasta + '/*.csv'
    #print(arquivo)
    return sorted(glob(arquivo))


def cita(df, nomes):
    redex = re.compile('@')
    for ind in df.index:
        sup = str(df['mentions'][ind])
        tags = sup.split()
        for tag in tags:
            tag = redex.sub('', tag)
            sup = nomes.get(tag)
            if sup != None:
                nomes[tag] += 1
    return nomes


def dictio(file):
    df = pd.read_csv(file, sep=';')
    nomes = {}
    for ind in df.index:
        sup = df['username'][ind]
        if nomes.get(sup) == None:
            nomes[sup] = 0
    return nomes


def escrita(number, outputfile):
    with codecs.open(outputfile + '_citados.csv', 'w', encoding='utf8') as arquivo:
        arquivo.write('"Name";"Number of citations"\n')
        for key, values in number.items():
            arquivo.write(f'{str(key)};{str(values)}\n')
        arquivo.close()


def main():
    result = read_options()
    if not result.get('success'):
        print('Missing data')
        sys.exit(0)
    inputfile = result.get('input')
    df = pd.read_csv(inputfile)
    outputfile = result.get('output')
    folder = pasta(result.get('names'))
    for namefile in folder:
        nome = namefile[24:-12]
        print(nome)
        names = dictio(namefile)
        number = cita(df, names)
        escrita(number, outputfile + '/' + nome)



if __name__ == '__main__':
    main()
