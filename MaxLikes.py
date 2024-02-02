import codecs
import pandas as pd
import argparse
import sys


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


def dictio(namefile):
    df = pd.read_csv(namefile, sep=';')
    names = {}
    for ind in df.index:
        if names.get(df['username'][ind]) == None:
            names[df['username'][ind]] = [0, 0]
    return names


def maxlike(df, names):
    for ind in df.index:
        sup = names.get(df['username'][ind])
        if sup != None:
            if sup[0] < df['like_count'][ind]:
                names[df['username'][ind]][0] = df['like_count'][ind]
                names[df['username'][ind]][1] = ind
    return names


def escrita(df, resultado, outputfile):
    with codecs.open(outputfile + '_MaxLikes.csv', 'w', encoding='utf8') as arquivo:
        arquivo.write('"Name";"Number of likes";"text"\n')
        for key, values in resultado.items():
            sup = df['text'][values[1]]
            arquivo.write(f'{str(key)};{str(values[0])};"{str(sup)}"\n')
        arquivo.close()


def main():
    result = read_options()
    if not result.get('success'):
        print('missing data')
        sys.exit(0)
    df = pd.read_csv(result.get('input'))
    outputfile = result.get('output')
    namefile = result.get('names')
    folder = pasta(namefile)
    folder = [namefile]
    for namefile in folder:
        nome = namefile[24:-12]
        nome = 'Anti'
        print(nome)
        names = dictio(namefile)
        resultado = maxlike(df, names)
        escrita(df, resultado, outputfile + '/' + nome)



if __name__ == '__main__':
    main()
