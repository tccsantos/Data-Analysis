import pandas as pd
import datetime as dt
import sys
import argparse
import codecs


from glob import glob
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


def pasta(pasta: str) -> list[str]:
    arquivo = pasta + '/*.csv'
    #print(arquivo)
    return sorted(glob(arquivo))


def read(input: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(input)
        return df.sort_values('username')
    except Exception as e:
        print(e)
        sys.exit(1)


def post_recente(df: pd.DataFrame, ref: dt.date) -> dict:
    wordlist = {}
    #helper = []
    #ajuda = []
    size = len(df.index)
    count = 0
    for ind in df.index:
        count += 1
        if not count%10000:
            p	=	(1.*count/size)*100	
            print("\t"+str(round(p,2))+" % finished")
        try:
            sup = df['created_at'][ind]
            dia = dt.date(int(sup[0:4]), int(sup[5:7]), int(sup[8:10]))
            delta = dia - ref
            delta = delta.days
            nome = df['username'][ind]
            sup = wordlist.get(nome)
            if sup:
                if delta < sup:
                    wordlist[nome] = delta
                # ajuda = [nome, delta]
                # wordlist.append(ajuda)
            else:
                wordlist[nome] = delta
        except Exception as e:
            print(e)
            pass

    return wordlist


def idade(df: pd.DataFrame, ref: dt.date) -> list[list[int, str]]:
    wordlist = []
    helper = {}
    size = len(df.index)
    count = 0
    for ind in df.index:
        count += 1
        if not count%10000:
            p	=	(1.*count/size)*100	
            print("\t"+str(round(p,2))+" % finished")
        try:
            nome = str(df['username'][ind])
            if not helper.get(nome):
                helper[nome] = True
                sup = df['user_created_at'][ind]
                dia = dt.date(int(sup[0:4]), int(sup[5:7]), int(sup[8:10]))
                delta = dia - ref
                delta = delta.days
                suporte = [delta, nome]
                wordlist.append(suporte)
        except Exception as e:
            print(e)
            pass
    return wordlist


def mix(post: dict, idade: list) -> list[list[int, str]]:
    definitivo = []
    if (size := len(post)) == len(idade):
        count = 0
        for a in range(size):
            count += 1
            if not count%10000:
                p	=	(1.*count/size)*100	
                print("\t"+str(round(p,2))+" % finished")
            apoio = []
            sup = post.get(idade[a][1])
            if not sup:
                print("Names does not match")
                sys.exit(1)
            phase = sup - idade[a][0]
            apoio.append(int(phase))
            apoio.append(idade[a][1])
            definitivo.append(apoio)
        definitivo.sort()
        return definitivo
    else:
        print("Error")
        print(len(post), len(idade))
        sys.exit(1)
    

def busca(df: pd.DataFrame, avalia: dict) -> list[tuple[str, int]]:
    suporte = []
    size = len(df.index)
    count = 0
    for ind in df.index:
        count += 1
        if not count%10000:
            p	=	(1.*count/size)*100	
            print("\t"+str(round(p,2))+" % finished")
        nome = df["username"][ind]
        if avalia.get(nome):
            suporte.append(nome)
    c = Counter(suporte)
    return c.most_common()


def junction(mix: dict, amount: list) -> list[tuple[int, int, str]]:
    suporte = []
    if len(mix) == len(amount):
        size = len(amount)
        count = 0
        for ind in range(len(amount)):
            count += 1
            if not count%10000:
                p	=	(1.*count/size)*100	
                print("\t"+str(round(p,2))+" % finished")
            nome = amount[ind][0]
            sup = mix.get(nome)
            if sup != None:
                ajuda = (amount[ind][1], sup, nome)
                suporte.append(ajuda)
            else:
                print('Name not Found')
                print(nome)
                sys.exit(1)
        return suporte
    else:
        print("Error")
        print(len(mix), len(amount))
        sys.exit(1)


def escrita(data: list[str], name: str) -> None:
    with codecs.open(name + "_bots.csv", 'w', encoding='utf-8') as arquivo:
        arquivo.write('"Name";"Posts";"Age"\n')
        for info in data:
            arquivo.write(f'"{str(info[2])}";"{str(info[0])}";"{str(info[1])}"\n')
        arquivo.close()


def main() -> None:
    result = read_options()
    if not result.get("success"):
        sys.exit(1)
    # folder = pasta(result.get("input"))
    # for input in folder:
    input = result.get("input")
    df = read(input)
    ref = dt.date(2010, 1, 1)
    print('Starting')
    wordlist = post_recente(df, ref)
    print("part 1 complete")
    wordlist2 = idade(df, ref)
    print('part 2 complete')
    bots = mix(wordlist, wordlist2)
    print('part 3 complete')
    avalia = {}
    processed = {}
    for ind in range(len(bots)):
        avalia[bots[ind][1]] = True
        processed[bots[ind][1]] = bots[ind][0]
    amount = busca(df, avalia)
    print('part 4 complete')
    conclusion = junction(processed, amount)
    print('start writing')
    conclusion.sort(reverse = True)
    escrita(conclusion, input[:-9])


if __name__ == '__main__':
    main()