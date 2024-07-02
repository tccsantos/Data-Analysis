import argparse
import sys


from argparse import RawTextHelpFormatter

sys.path.insert(1, 'DataAnalysis')
from Library.helper import helper, grafo



def edges(data: helper, gml : grafo):
    cib = 1
    count = []
    for ind in data.file.index:
        if cib != data.file["cib"][ind]:
            quantidade = helper.contagem(count)
            for edge in quantidade:
                try:
                    gml.setedges(edge[0], cib, edge[1])
                except SyntaxError:
                    print(edge, cib)
                    sys.exit(0)

            cib += 1
            count = []
        
        count.append(data.file['username'][ind])  
    
    quantidade = helper.contagem(count)
    for edge in quantidade:
        try:
            gml.setedges(edge[0], cib, edge[1])
        except SyntaxError:
            print(edge, cib)
            sys.exit(0)
    
    return gml


def analise(data: helper):
    gml = grafo(True, True)

    quantidade = set(data.file["username"])
    for nome in quantidade:
        gml.setnodes(nome, 1)
    
    quantidade = helper.contagem(data.file["cib"])
    for event in quantidade:
        gml.setnodes(event[0], event[1])

    gml = edges(data, gml)
    
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
