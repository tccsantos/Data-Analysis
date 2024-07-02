import codecs
import pandas as pd


from csv import reader
from glob import glob
from collections import Counter



class grafo:

    def __init__(self, weightnode = False, weightedge = False) -> None:
        self.nodes: set = set()
        self.edges: dict[any, set] = dict()
        self.weightnode: bool = weightnode
        self.weightedge: bool = weightedge

        if weightnode: self.nodew: dict = dict()
        else: self.nodew: dict = None
        
        if weightedge: self.edgesw: dict = dict()
        else: self.edgesw: dict = None
    

    def setnodes(self, node, weight: int | None = None):
            self.nodes.add(node)
            if self.weightnode:
                self.setnodeweight(node, weight)
    

    def setedges(self, source, target, weight: int | None = None):
        if source not in self.nodes or target not in self.nodes: raise SyntaxError
        if self.edges.get(source) == None:
            self.edges[source] = {target}
            if self.weightedge:
                self.setedgeweight(source, target, weight)
        else:
            self.edges[source].add(target)
            if self.weightedge:
                self.setedgeweight(source, target, weight)
    

    def setnodeweight(self, node, weight: int):
        if type(weight) != int:
            raise ValueError
        
        if not self.nodew.get(node):
            self.nodew[node] = weight
    

    def setedgeweight(self, source, target, weight: int):
        if type(weight) != int:
            raise ValueError
        
        edge = (source, target)
        self.edgesw[edge] = weight


class helper:


    def __init__(self, arquivo: str, type: str = '', retorno: str = None, sep: str = ';') -> None:
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
        

    def gml(self, escrita: grafo) -> None:
        if not self.ret: raise ValueError
        with codecs.open(self.ret + ".gml", 'w', encoding='utf8') as arquivo:
            if escrita.weightnode:
                arquivo.write("graph\n[\n")
                for node, weight in escrita.nodew.items():
                    arquivo.write(f'\tnode\n\t[\n\t\tid {str(node)}\n\t\tlabel "{str(node)}"\n\t\tweight {str(weight)}\n\t]\n')
            else:
                arquivo.write("graph\n[\n")
                for node in escrita.nodes:
                    arquivo.write(f'\tnode\n\t[\n\t\tid {str(node)}\n\t\tlabel "{str(node)}"\n\t]\n')
            if escrita.weightedge:
                for edge, weight in escrita.edgesw.items():
                    source = edge[0]
                    target = edge[1]
                    label = f'aresta {str(source)} para {str(target)}'
                    arquivo.write(f'\tedge\n\t[\n\t\tsource {str(source)}\n\t\ttarget {str(target)}\n\t\tlabel "{str(label)}"\n\t\tweight {str(weight)}\n\t]\n')
            else:
                for source, targets in escrita.edges.items():
                    for target in targets:
                        label = f'aresta de {str(source)} para {str(target)}'
                        arquivo.write(f'\tedge\n\t[\n\t\tsource {str(source)}\n\t\ttarget {str(target)}\n\t\tlabel "{str(label)}"\n\t]\n')
                    
            arquivo.write("]")


    def dict_sort(d: dict) -> dict:
        new = dict()

        while(True):
            i = 0
            big = -1
            big_key = None

            for key, values in d.items():
                i += 1
                if values > big:
                    big = values
                    big_key = key
                
            new[big_key] = big
            d.pop(big_key)

            if i <= 1: break
        
        return new