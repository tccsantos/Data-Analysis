import pandas as pd
import datetime as dt
import sys
import argparse


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


def read(input):
    try:
        df = pd.read_csv(input)
        return df.sort_values('username')
    except Exception as e:
        print(e)
        sys.exit(1)


def post_recente(df, ref):
    wordlist = []
    helper = df['username'][df.index[0]]
    ajuda = []
    verdade = 72000
    for ind in df.index:
        try:
            nome = df['username'][ind]
            if nome != helper:
                ajuda = [helper, verdade]
                wordlist.append(ajuda)
                helper = nome
                verdade = 72000
            sup = df['created_at'][ind]
            dia = dt.date(int(sup[0:4]), int(sup[5:7]), int(sup[8:10]))
            delta = dia - ref
            delta = delta.days
            if delta < verdade:
                verdade = delta
        except Exception as e:
            print(e)
            pass
    ajuda = [helper, verdade]
    wordlist.append(ajuda)
    return wordlist


def idade(df, ref):
    wordlist = []
    helper = None
    for ind in df.index:
        try:
            nome = df['username'][ind]
            if nome != helper:
                helper = nome
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
            phase = post[a][1] - idade[a][0]
            apoio.append(phase)
            apoio.append(post[a][0])
            definitivo.append(apoio)
        definitivo.sort()
        #print(definitivo[:200])
        return definitivo[:100]
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



result = read_options()
if not result.get("success"):
    sys.exit(1)
df = read(result.get("input"))
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
print(conclusion)
