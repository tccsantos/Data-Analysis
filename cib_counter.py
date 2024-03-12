import pandas as pd
import codecs
import argparse
import sys

from collections import Counter
from argparse import RawTextHelpFormatter



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


def contagem(suporte: list) -> list[tuple[any, int]]:
    c = Counter(suporte)
    return c.most_common()


def read(inputfile: str) -> pd.DataFrame:
    return pd.read_csv(inputfile)


def dictio(df: pd.DataFrame) -> dict:
    sup = {}
    for ind in df.index:
        if not sup.get(str(df['cib'][ind])):
            sup[str(df['cib'][ind])] = 0
    return sup


def analise(df: pd.DataFrame, cib: dict) -> dict:
    apoio = []
    for ind in df.index:
        apoio.append(df['cib'][ind])
    soma = contagem(apoio)
    for value in soma:
        cib[str(value[0])] = str(value[1])
    return cib


def escrita(df: pd.DataFrame, cib: dict) -> None:
    # df2 = pd.DataFrame(cib)
    df['cib_count'] = cib
    print(df.head())


if __name__ == '__main__':
    result = read_options()
    if not result.get("success"):
        sys.exit(1)
    df = read(result.get("input"))
    cib = dictio(df)
    cib = analise(df, cib)
    escrita(df, cib)
