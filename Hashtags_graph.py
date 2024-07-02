import pandas as pd
import argparse
import sys


from argparse import RawTextHelpFormatter


sys.path.insert(1, 'DataAnalysis')
from Library.helper import helper, grafo



def read_options():
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


def analysis(df) -> grafo:
    graph = grafo(weightedge= True)
    edges = []

    count	=	0
    size = len(df)
    ava = round(size/10)
    if ava > 1000: ava = 1000
    if ava < 1: ava = 1

    for ind in df.index:

        if not count%ava:
            p	=	(1.*count/size)*100	
            print("\t"+str(round(p,2))+" % finished")	
        count	=	count	+	1

        raw: str = df['hashtags'][ind]
        if type(raw) != str: continue
        #print(raw)
        sup: list[str] = list(set(raw.split()))
        hashtags = [name.lower() for name in sup]
        hashsize = len(hashtags)

        for i in range(hashsize):
            
            for j in range(i + 1, hashsize):
                edge = (hashtags[i], hashtags[j])
                edges.append(edge)
    
    count = helper.contagem(edges)
    for edge in count:
        if edge[1] < 2: break
        graph.setnodes(edge[0][0])
        graph.setnodes(edge[0][1])
        graph.setedges(edge[0][0], edge[0][1], edge[1])
    
    return graph


def main():
    result = read_options()

    if not result.get("success"):
        sys.exit(1)

    inputfile = result.get("input")
    outputfile = result.get("output")
    
    work = helper(inputfile, 'pd', outputfile, ';')
    graph = analysis(work.file)
    work.gml(graph)



if __name__ == "__main__":
    main()
