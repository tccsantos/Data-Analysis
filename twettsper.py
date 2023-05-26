import pandas as pd
import argparse
import sys

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


result = read_options()
if not result.get("success"):
    sys.exit(1)
df = pd.read_csv(result.get("input"))
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
max_top = 10
print('Número de Tweets:')
print(suporte)
print('Usuários que mais tweetaram:')
print(top[:10])
