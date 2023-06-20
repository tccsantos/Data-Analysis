import pandas as pd
import argparse
import sys
# import matplotlib.pyplot as plt
# import numpy as np
# import re

from argparse import RawTextHelpFormatter
from collections import Counter


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
        return df
    except Exception as e:
        print(e)
        sys.exit(1)


result = read_options()
if not result.get("success"):
    sys.exit(1)
df = read(result.get("input"))
wordlist = []
suporte = 0
for ind in df.index:
    try:
        wordlist.append(df['username'][ind])
        suporte += 1
    except Exception as e:
        print(e)
        pass
c = Counter(wordlist)
top = c.most_common()
print('Número de Tweets:')
print(suporte)
print('Usuários que mais tweetaram:')
print(top[:10])
# top = np.array(top)
# x = top[:,0]
# y = np.array_str(top[:,1])
# y = re.sub(r"[]'[]", "", y)
# y = y.split()
# for a in y:
#     a = int(a)
# print(y)

# #plt.plot()
