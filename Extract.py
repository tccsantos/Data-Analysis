import pandas as pd
import argparse
import sys
#import codecs


from argparse import RawTextHelpFormatter
from glob import glob
from csv import reader



def read_options():
    status = False

    parser = argparse.ArgumentParser(
        description="Basic Usage", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--input", help="CSV input File", required=True, default=""
    )

    argument = parser.parse_args()

    if argument.input:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input}


def pasta(pasta: str) -> list[str]:
    arquivo = pasta + '/*.csv'
    #print(arquivo)
    return sorted(glob(arquivo))


def read(input: str) -> list[str]:
    with open(input, 'r', encoding='utf8') as arquivo:
        aba = reader(arquivo, delimiter=';')
        next(aba, None)
        file =  list(aba)

    suporte = []
    for i in range(len(file)):
        if int(file[i][1])/(int(file[i][2]) + 1) >= 100:
            suporte.append(str(file[i][0]))
        # suporte.append(str(file[i][1]))
    return suporte


# def extract_text(bots: list[str], df: pd.DataFrame, output: str) -> None:
#     with codecs.open(output + '_text.csv', 'w', encoding='utf8') as arquivo:
#         arquivo.write('"Name";"Text"\n')
#         for ind in df.index:
#             if df['username'][ind] in bots:
#                 name = df['username'][ind]
#                 text = df['text'][ind]
#                 arquivo.write(f'"{str(name)}";"{str(text)}"\n')
#         arquivo.close()


def main():
    result = read_options()
    if not result.get("success"):
        sys.exit(1)
    path = str(result.get("input"))
    folder = [path]
    df = pd.read_csv('./Dados/Anti-Grande.csv')
    for input in folder:
        bots: list[str] = read(input)
        nome = input[45:-4]
        print(nome)
        # print(len(bots))
        # extract_text(bots, df, path + '/' + nome)
        mask = []
        for ind in df.index:
            if df['username'][ind] in bots:
                mask.append(True)
            else: mask.append(False)
        df_cut = df.loc[mask]
        df_cut.to_csv('./Dados/Antiqnt_text.csv',index=False, sep=';')


if __name__ == '__main__':
    main()