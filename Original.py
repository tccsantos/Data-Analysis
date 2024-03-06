import pandas as pd
import codecs
import sys
import argparse
import re


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


def analise(path: str) -> None:
    df = pd.read_csv(path, sep=';')
    redex = re.compile('RT')
    mask = []
    for ind in df.index:
            if redex.search(df['text'][ind]):
                mask.append(False)
            else: mask.append(True)
    df_cut = df.loc[mask]
    df_cut.to_csv(path[:-4] + '_original.csv',index=False, sep=';')




def main() -> None:
    result = read_options()
    if not result.get("success"):
        sys.exit(1)
    path = str(result.get("input"))
    analise(path)
    


if __name__ == '__main__':
    main()
