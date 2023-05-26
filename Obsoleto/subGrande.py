import nltk
import pandas as pd
import csv
import datetime as dt

def find(str, ch):
    indice = 0
    while indice < len(str):
        if str[indice] == ch:
            return indice
        indice = indice + 1
    return -1

df = pd.read_csv('C:\\Users\Thiago\Documents\IC\ANTIDEMOCRATICOS_2017.csv')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = stopwords.words('portuguese')
custom_stop_words = ['rt', '@', '#', '.', '!', '?', ':', '...', '-', 'pra', 'q', 'https', '…', "'", '$']
my_stop_words= set(custom_stop_words + stop_words)
stop = ['#', '?', '!']
ref = dt.date(2018, 1, 1)
wordlist = []
help = 0
for ind in df.index:
    try:
        ajuda = []
        nome = df['username'][ind]
        sup = df['created_at'][ind]
        dia = dt.date(int(sup[0:4]), int(sup[5:7]), int(sup[8:10]))
        delta = ref - dia
        delta = delta.days
        y = True
        for ponta in range(0, len(wordlist) - 1):
            if nome == wordlist[ponta][0]:
                y = False
                if delta < wordlist[ponta][1]:
                    wordlist[ponta][1] = delta
                break
        if y:
            ajuda.append(nome)
            ajuda.append(delta)
            wordlist.append(ajuda)
        print(help)
        help += 1
    except Exception as e:
        print(e)
        pass
wordlist2 =[]
help = 0
for ind in df.index:
    try:
        suporte = []
        sup = df['user_created_at'][ind]
        dia = dt.date(int(sup[0:4]),int(sup[5:7]), int(sup[8:10]))
        delta = ref - dia
        delta = delta.days
        suporte.append(delta)
        suporte.append(df['username'][ind])
        if suporte not in wordlist2:
            wordlist2.append(suporte)
        print(help)
        help += 1
    except Exception as e:
        print(e)
        pass
wordlist2.sort()
definitivo = []
fim = len(wordlist)-1
for a in range(0, len(wordlist2)-1):
    apoio = []
    for b in range(0, fim):
        if wordlist2[a][1] == wordlist[b][0]:
            apoio.append(wordlist2[a][1])
            apoio.append(wordlist2[a][0] - wordlist[b][1])
            definitivo.append(apoio)
            break
print(definitivo[:50])