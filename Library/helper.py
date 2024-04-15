import codecs
import pandas as pd


from csv import reader
from glob import glob
from collections import Counter



class helper:


    def __init__(self, type: str, arquivo: str, retorno: str = None, sep: str = ';') -> None:
        if type.lower() == 'pd' or type.lower() == 'pandas':
            self.file = pd.read_csv(arquivo, sep= sep)
        else:
            self.file = helper.leitor_csv(arquivo, sep)
        if retorno:
            self.ret = retorno
        else: self.ret = None


    def pasta_csv(pasta: str) -> list[str]:
        arquivo = pasta + '/*.csv'
        return sorted(glob(arquivo))
    

    def contagem(lista: list[any]) -> list[tuple[any, int]]:
        c = Counter(lista)
        return c.most_common()
    

    def leitor_csv(nome: str, sep: str = ';') -> list[any]:
        with open(nome, 'r', encoding= 'utf8') as arquivo:
            readable = reader(arquivo, delimiter=sep)
            next(readable, None)
            return list(readable)
        

    def gml(self, escrita: dict, pesoAresta: bool = False, pesoNoh: bool = False) -> None:
        if not self.ret: raise ValueError
        #noh = len(escrita)
        with codecs.open(self.file + ".gml", 'w', encoding='utf8') as arquivo:
            if pesoNoh:
                arquivo.write("graph\n[\n")
                for node, values in escrita.items():
                    weight = values[0]
                    arquivo.write(f'\tnode\n\t[\n\t\tid {str(node)}\n\t\tlabel "{str(node)}"\n\t\tweight {str(weight)}\n\t]\n')
            else:
                arquivo.write("graph\n[\n")
                for node in escrita.keys():
                    arquivo.write(f'\tnode\n\t[\n\t\tid {str(node)}\n\t\tlabel "{str(node)}"\n\t]\n')
            if pesoAresta:
                if pesoNoh:
                    for source, edges in escrita.items():
                        for aresta in edges[1]:
                            target = aresta[0]
                            weight = aresta[1]
                            label = f'aresta {str(source)} para {str(target)}'
                            arquivo.write(f'\tedge\n\t[\n\t\tsource {str(source)}\n\t\ttarget {str(target)}\n\t\tlabel "{str(label)}"\n\t\tweight {str(weight)}\n\t]\n')
                else:
                    for source, edges in escrita.items():
                        for aresta in edges:
                            target = aresta[0]
                            weight = aresta[1]
                            label = f'aresta {str(source)} para {str(target)}'
                            arquivo.write(f'\tedge\n\t[\n\t\tsource {str(source)}\n\t\ttarget {str(target)}\n\t\tlabel "{str(label)}"\n\t\tweight {str(weight)}\n\t]\n')
            else:
                if pesoNoh:
                    for source, edges in escrita.items():
                        for aresta in edges[1]:
                            target = aresta
                            label = f'aresta {str(source)} para {str(target)}'
                            arquivo.write(f'\tedge\n\t[\n\t\tsource {str(source)}\n\t\ttarget {str(target)}\n\t\tlabel "{str(label)}"\n\t]\n')
                else:
                    for source, edges in escrita.items():
                        for aresta in edges:
                            target = aresta
                            label = f'aresta {str(source)} para {str(target)}'
                            arquivo.write(f'\tedge\n\t[\n\t\tsource {str(source)}\n\t\ttarget {str(target)}\n\t\tlabel "{str(label)}"\n\t]\n')
                    
            arquivo.write("]")



