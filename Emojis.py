import emoji
import pandas as pd
import codecs
import argparse
import sys


from collections import Counter
from glob import glob
from csv import reader
from argparse import RawTextHelpFormatter



def pasta(pasta):
    arquivo = pasta + '/*.csv'
    #print(arquivo)
    return sorted(glob(arquivo))


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
        "-m", "--mode", help="True for reader, False for pandas", required=True, default=""
    )

    argument = parser.parse_args()

    if argument.input and argument.output and argument.mode:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input, "output": argument.output, "mode": argument.mode}


def contagem(lista):
    c = Counter(lista)
    return c.most_common()


def analise(file):
    count = []
    #i = 0
    for text in file:
        text = str(text)
        # i += 1
        # if i < 5833 and i > 5829:
        #     print(text)
        #     print(emoji.emoji_count(text))
        #     print(emoji.emoji_list(text))
        if emoji.emoji_count(text):
            emo = emoji.emoji_list(text)
            for emojis in emo:
                count.append(emojis.get('emoji'))
    return contagem(count)


def escrita(result, outputfile):
    with codecs.open(outputfile + '_emoji.csv', 'w', encoding='utf8') as arquivo:
        arquivo.write('"Emoji";"Count"\n')
        for termo in result:
            arquivo.write(f'"{termo[0]}";"{str(termo[1])}"\n')
        arquivo.close()
    return


def read(mode, file):
    if mode:
        with open(file, 'r', encoding='utf8') as arquivo:
            aba = reader(arquivo)
            return list(aba)
    else:
        df = pd.read_csv(file)
        return list(df['text'])


def main():
    result = read_options()
    if not result.get('success'):
        print('missing data')
        sys.exit(0)
    folder = pasta(result.get('input'))
    mode = result.get('mode')
    #folder = ['./Dados/Anti-Grande.csv']
    path = result.get('output')
    for file in folder:
        name = file[16:-9]
        print(name)
        raw = read(mode, file)
        resultado = analise(raw)
        print(path + '/' + name)
        escrita(resultado, path + '/' + name)


if __name__ == '__main__':
    main()
