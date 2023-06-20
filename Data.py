import nltk
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
#import re
import numpy as np

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

def solution(input):
    df = pd.read_csv(input)
    wordlist = []
    for ind in df.index:
        try:
            word_tokens = df['created_at'][ind]
            #wordlist.append(word_tokens[:10])
            wordlist.append(word_tokens[:7])
        except Exception as e:
            print(e)
            pass
    FreqDist = nltk.FreqDist(wordlist)
    top = FreqDist.most_common(len(wordlist))
    return top

def plot(top):
    x = []
    y = []
    #redex = re.compile("2017-")
    for a in range(0, len(top)):
        # x.append(redex.sub("", top[a][0]))
        x.append(a)
        y.append(top[a][1])
    #plt.figure(figsize=(20, 5), dpi = 100)
    plt.figure(figsize=(30, 5), dpi = 100)
    #plt.title("Tweets per day, 2017")
    plt.title("Tweets per month, 2014-2021")
    #plt.xlabel("Months", fontsize = 15)
    plt.xlabel("Years", fontsize = 15)
    plt.ylabel("Tweets", fontsize = 15)
    plt.subplots_adjust(bottom=0.1, left=0.1, right=0.9)
    plt.plot(x, y, label = "Tweets per month")
    plt.yscale("log")
    #plt.xticks(np. arange(0, 366, step = 31), ["January", "Febuary", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"])
    plt.xticks(np. arange(0, 96, step = 12), ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"])
    plt.legend()
    plt.savefig("./output/big.jpg", dpi = 150)
    plt.show()


result = read_options()
if not result.get("success"):
    sys.exit(1)
top = solution(result.get("input"))
print('Dias mais frequentes = ')
print(top[:10])
top.sort()
plot(top)
