import nltk
import pandas as pd
import datetime as dt


df = pd.read_csv('C:\\Users\Thiago\Documents\IC\ANTIDEMOCRATICOS_2017.csv')
wordlist = df['username']
wordlist2 = []
ref = dt.date(2018, 1, 1)
for ind in df.index:
    try:
        suporte = []
        sup = df['user_created_at'][ind]
        dia = dt.date(int(sup[0:4]), int(sup[5:7]), int(sup[8:10]))
        delta = ref - dia
        delta = delta.days
        suporte.append(delta)
        suporte.append(df['username'][ind])
        if suporte not in wordlist2:
            wordlist2.append(suporte)
    except Exception as e:
        print(e)
        pass
FreqDist = nltk.FreqDist(wordlist)
top = FreqDist.most_common(len(wordlist))
wordlist2.sort()
definitivo = []
for a in range(0, len(wordlist2)-1):
    apoio = []
    for b in range(0, len(top)-1):
        if wordlist2[a][1] == top[b][0]:
            apoio.append(top[b][1])
            apoio.append(wordlist2[a][0])
            apoio.append(wordlist2[a][1])
            definitivo.append(apoio)
            break
definitivo.sort(reverse=True)
print(definitivo[:50])
