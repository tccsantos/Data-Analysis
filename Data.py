import nltk
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys

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


result = read_options()
if not result.get("success"):
    sys.exit(1)
inputfile = result.get("input")
df = pd.read_csv(inputfile)
wordlist = []
for ind in df.index:
    try:
        word_tokens = df['created_at'][ind]
        wordlist.append(word_tokens[:10])
    except Exception as e:
        print(e)
        pass
FreqDist = nltk.FreqDist(wordlist)
top = FreqDist.most_common(len(wordlist))
print('Dias mais frequentes = ')
print(top[:10])
top.sort()
fig = plt.figure(figsize=(200, 50))
plt.subplots_adjust(bottom=0.1, left=0.2, right=0.8)
x = []
y = []
for a in range(0, len(top)-1):
    x.append(top[a][0])
    y.append(top[a][1])
plt.plot(x, y)
plt.show()
