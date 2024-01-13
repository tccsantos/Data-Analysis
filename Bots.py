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


def pasta(pasta):
    arquivo = pasta + '/*.csv'
    #print(arquivo)
    return sorted(glob(arquivo))


def read(input):
    try:
        df = pd.read_csv(input)
        return df.sort_values('username')
    except Exception as e:
        print(e)
        sys.exit(1)


def post_recente(df, ref):
    wordlist = []
    helper = []
    ajuda = []
    for ind in df.index:
        try:
            sup = df['created_at'][ind]
            dia = dt.date(int(sup[0:4]), int(sup[5:7]), int(sup[8:10]))
            delta = dia - ref
            delta = delta.days
            nome = df['username'][ind]
            if nome not in helper:
                ajuda = [nome, delta]
                wordlist.append(ajuda)
                helper.append(nome)
            else:
                for i in range(len(wordlist)):
                    if wordlist[i][0] == nome:
                        if delta < wordlist[i][1]:
                            wordlist[i][1] = delta
                        break
        except Exception as e:
            print(e)
            pass

    return wordlist


def idade(df, ref):
    wordlist = []
    helper = []
    for ind in df.index:
        try:
            nome = df['username'][ind]
            if nome not in helper:
                helper.append(nome)
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


def mix(post, idade):
    definitivo = []
    if len(post) == len(idade):
        for a in range(len(post)):
            apoio = []
            if post[a][0] != idade[a][1]:
                print("Names does not match")
                sys.exit(1)
            phase = post[a][1] - idade[a][0]
            apoio.append(phase)
            apoio.append(post[a][0])
            definitivo.append(apoio)
        definitivo.sort()
        return definitivo
    else:
        print("Error")
        print(len(post), len(idade))
        sys.exit(1)
    

def busca(df, avalia):
    suporte = []
    for ind in df.index:
        nome = df["username"][ind]
        if nome in avalia:
            suporte.append(nome)
    c = Counter(suporte)
    return c.most_common()


def junction(mix, amount):
    suporte = []
    if len(mix) == len(amount):
        for ind in range(len(mix)):
            nome = mix[ind][1]
            for ind2 in range(len(amount)):
                if nome == amount[ind2][0]:
                    ajuda = [amount[ind2][1], mix[ind][0], nome]
                    suporte.append(ajuda)
                    break
        return suporte
    else:
        print("Error")
        print(len(mix), len(amount))
        sys.exit(1)


def escrita(data, name):
    with codecs.open(name + "_bots.csv", 'w', encoding='utf-8') as arquivo:
        arquivo.write('"Name";"Posts";"Age"\n')
        for info in data:
            arquivo.write(f'"{str(info[2])}";"{str(info[0])}";"{str(info[1])}"\n')
        arquivo.close()



result = read_options()
if not result.get("success"):
    sys.exit(1)
folder = pasta(result.get("input"))
for input in folder:
    df = read(input)
    ref = dt.date(2010, 1, 1)
    wordlist = post_recente(df, ref)
    wordlist2 = idade(df, ref)
    bots = mix(wordlist, wordlist2)
    avalia = []
    for ind in range(len(bots)):
        avalia.append(bots[ind][1])
    amount = busca(df, avalia)
    conclusion = junction(bots, amount)
    conclusion.sort(reverse = True)
    escrita(conclusion, input[:-9])
