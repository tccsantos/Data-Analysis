import argparse
import sys
import os

from argparse import RawTextHelpFormatter
from codecs import open as co
sys.path.insert(1, 'DataAnalysis')
from Library.helper import helper


def read_options() -> dict[str, bool|str|int]:
    status = False

    parser = argparse.ArgumentParser(
        description="Basic Usage", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--input", help="CSV input File", required=True, default=""
    )
    parser.add_argument(
        "-o", "--output", help="Output file path", required=True, default=""
    )
    parser.add_argument(
        "-d", "--divisions", help="Number of parts", required=True, default=""
    )

    argument = parser.parse_args()

    if argument.input and argument.output and argument.divisions:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input, "output": argument.output, "divisions": argument.divisions}


def reset_size(start: int, size: int, lenth: int) -> int:
    if start + 2*size > lenth:
        return lenth - start
    else:
        return size


def escrita(start: int, size: int, data: list[list[str]], name: str) -> None:
    with co(name + '.csv', 'w', encoding='utf8') as arquivo:
        arquivo.write(f'Type;Tweet_id;Label2;Text\n')
        for i in range(start, start+size):
            arquivo.write(f'None;{str(data[i][1])};None;"{str(data[i][3])}"\n')
    return


def main():
    result = read_options()

    if not result.get("success"):
        sys.exit(1)

    inputfile: str = result.get("input")
    path: str = result.get("output") + "_divisions"
    print(path)
    divisions: int = int(result.get("divisions"))
    
    os.makedirs(path, exist_ok = True)
    data: list[list[str]] = helper.leitor_csv(inputfile, ';')
    tam = len(data)
    size = round(tam/divisions)
    start = 0
    for i in range(divisions):
        name = path + '/' + str(i + 1) + '_piece'
        print(start, size)
        escrita(start, size, data, name)
        start += size
        size = reset_size(start, size, tam)
    




if __name__ == "__main__":
    main()
