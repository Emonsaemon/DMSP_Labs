from collections import defaultdict
from itertools import permutations

with open('dmsp_lab_data(5)1.data') as file:
    graph1 = file.read()
with open('dmsp_lab_data(5)2.data') as file:
    graph2 = file.read()
graph1 = [string.split(' ') for string in graph1.split('\n')]
graph2 = [string.split(' ') for string in graph2.split('\n')]
nodes1 = len(graph1)
nodes2 = len(graph2)

class Node:
    def __init__(self, number):
        self.number = number
    def __repr__(self):
        return str(self.number)

def equal(defdictL, defdictR):
    notEqual = False
    for keyL in defdictL:
        for keyR in defdictR:
            if keyL.number == keyR.number and len(defdictL[keyL]) == len(defdictR[keyR]):
                tempList1 = [n.number for n in defdictL[keyL]]
                tempList2 = [n.number for n in defdictR[keyR]]
                tempList1.sort()
                tempList2.sort()
                if tempList1 != tempList2:
                    notEqual = True
                    break
        if notEqual:
            break
    return not notEqual

if nodes1 != nodes2:
    print("Кількість вершин не співпадає! Графи не ізоморфні.")
else:
    nodesNum = nodes1
    edges1 = list()
    edges2 = list()
    for i in range(nodesNum):
        for j in range(nodesNum):
            graph1[i][j] = int(graph1[i][j])
            graph2[i][j] = int(graph2[i][j])
        edges1.append(sum(graph1[i]))
        edges2.append(sum(graph2[i]))
    edges1.sort()
    edges2.sort()
    if edges1 != edges2:
        print("Степені вершин не співпадають! Графи не ізоморфні.")
    else:
        isomorphic = False
        neighbors1 = defaultdict(list)
        neighbors2 = defaultdict(list)
        nodes1 = [Node(number) for number in list(range(nodesNum))]
        nodes2 = [Node(number) for number in list(range(nodesNum))]
        for y in range(nodesNum):
            for x in range(nodesNum):
                if graph1[y][x] != 0:
                    neighbors1[nodes1[y]].append(nodes1[x])
                if graph2[y][x] != 0:
                    neighbors2[nodes2[y]].append(nodes2[x])
        counter = 0
        for variant in permutations(list(range(nodesNum))):
            if equal(neighbors1, neighbors2):
                print(counter, "ітерацій! Графи ізоморфні")
                isomorphic = True
                break
            else:
                index = 0
                for number in variant:
                    nodes2[index].number = number
                    index += 1
            counter += 1
        if not isomorphic:
            print("Зв'язки між вершинами не ідентичні! Графи не ізоморфні.")