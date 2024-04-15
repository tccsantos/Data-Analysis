import pandas as pd
import codecs
import re
import argparse
import sys

from collections import Counter
from argparse import RawTextHelpFormatter
from glob import glob

def read_options():
    status = False

    parser = argparse.ArgumentParser(
        description="Basic Usage", formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-i", "--input", help="CSV input File", required=True, default=""
    )
    parser.add_argument(
        "-f", "--folder", help="Folder directory", required=True, default=""
    )

    argument = parser.parse_args()

    if argument.input and argument.folder:
        status = True

    if not status:
        print("Maybe you want to use -h for help")
        status = False

    return {"success": status, "input": argument.input, "folder": argument.folder}

def pasta(pasta):
    arquivo = pasta + '/*.csv'
    #print(arquivo)
    return sorted(glob(arquivo))

#Abrir o DataSet e verificar o comando que remove as duplicatas
#usuario = {}



#Criar um dicionario Usuario = Usuario[nome] = True/False
#Usuario.get("nome") return True/False

def analise(arquivos, input):
    df = pd.read_csv(input)
    df = df.drop_duplicates(subset = 'username')
    user = {}
    for ind in df.index:
        user[df["username"][ind]] = df["verified"][ind]
    for arquivo in arquivos:
        df = pd.read_csv(arquivo)
        dfa = df.drop_duplicates(subset = 'Source')
        df = df.drop_duplicates(subset = 'Target')
        print(arquivo[11:-4] + '\nCitam:\n')
        for ind in dfa.index:
            try:
                if user[str(dfa["Source"][ind])]:
                    print(("\t" + dfa["Source"][ind]))
            except Exception as e:
                print(e)
                pass
        print("\nCitados:")
        for ind in df.index:
            try:
                if user[str(df["Target"][ind])]:
                    print(("\t" + df["Target"][ind]))
            except Exception as e:
                #print(e)
                pass
        print('\n\n')



result = read_options()
if not result.get("success"):
    sys.exit(1)
arquivos = pasta(result.get("folder"))
#print(arquivos)
analise(arquivos, result.get("input"))


# import pickle 
# import math 
# object_pi = math.pi 
# file_pi = open('filename_pi.obj', 'w') 
# pickle.dump(object_pi, file_pi)
# import pickle 
# filehandler = open(filename, 'r') 
# object = pickle.load(filehandler)