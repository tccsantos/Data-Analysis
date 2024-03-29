import codecs
import pandas as pd
import argparse
import sys


from argparse import RawTextHelpFormatter
from glob import glob


def read_options() -> dict:
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


def pasta(pasta: str) -> list[str]:
    arquivo = pasta + '/*.csv'
    #print(arquivo)
    return sorted(glob(arquivo))


def dictio(namefile: str) -> dict:
    df = pd.read_csv(namefile, sep=';')
    names = {}
    for ind in df.index:
        if names.get(df['username'][ind]) == None:
            names[df['username'][ind]] = 0
    return names


def likes(df: pd.DataFrame, names: dict) -> dict:
    for ind in df.index:
        if names.get(df['username'][ind]) != None:
            names[df['username'][ind]] += df['like_count'][ind]
    return names


def escrita(resultado: dict, outputfile: str) -> None:
    with codecs.open(outputfile + '_likes.csv', 'w', encoding='utf8') as arquivo:
        arquivo.write('"Name";"Number of likes"\n')
        for key, values in resultado.items():
            arquivo.write(f'{str(key)};{str(values)}\n')
        arquivo.close()


def main() -> None:
    result = read_options()
    if not result.get('success'):
        print('missing data')
        sys.exit(0)
    df = pd.read_csv(result.get('input'), sep=';')
    outputfile = result.get('output')
    namefile = result.get('names')
    folder = pasta(namefile)
    folder = [namefile]
    for namefile in folder:
        nome = namefile[24:-12]
        nome = 'cib'
        print(nome)
        names = dictio(namefile)
        resultado = likes(df, names)
        escrita(resultado, outputfile + '/' + nome)



if __name__ == '__main__':
    main()
