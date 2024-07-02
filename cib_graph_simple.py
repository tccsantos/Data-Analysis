import argparse
import sys


from argparse import RawTextHelpFormatter

sys.path.insert(1, 'DataAnalysis')
from Library.helper import helper, grafo



def edges(data: helper):
    cib = 1
    nodes = set()
    count = []
    for ind in data.file.index:
        if cib != data.file["cib"][ind]:

            if len(nodes) > 1:  
                for source in nodes:
                    for target in nodes:
                        if source != target:
                            count.append((source, target))

            nodes = set()
            cib += 1
        
        nodes.add(data.file['username'][ind])  
    if len(nodes) > 1:  
        for source in nodes:
            for target in nodes:
                if source != target:
                    count.append((source, target))
    return helper.contagem(count)


def analise(data: helper):
    gml = grafo(True, True)

    quantidade = helper.contagem(data.file["username"])
    for nome in quantidade:
        gml.setnodes(nome[0], nome[1])

    quantidade = edges(data)
    #print(quantidade[:5])
    for edge in quantidade:
        gml.setedges(edge[0][0], edge[0][1], edge[1])
    return gml
    

def read_options() -> dict:
        status = False

        parser = argparse.ArgumentParser(
            description="Basic Usage", formatter_class=RawTextHelpFormatter
        )
        parser.add_argument(
            "-i", "--input", help="CSV input File", required=True, default=""
        )
        parser.add_argument(
            "-o", "--output", help="Output file name", required=True, default=""
        )

        argument = parser.parse_args()

        if argument.input and argument.output:
            status = True

        if not status:
            print("Maybe you want to use -h for help")
            status = False

        return {"success": status, "input": argument.input, "output": argument.output}


def main():
    result = read_options()
    if not result.get('success'):
        print('missing data')
        sys.exit(0)
    
    data = helper(result["input"], "pd", result["output"])
    gml = analise(data)
    data.gml(gml)



if __name__ == "__main__":
    main()
