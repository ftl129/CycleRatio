'''
 ============================================================================
 Name        : Characterizing cycle structure in complex networks
 Author      : Tianlong Fan (tianlong.fan@unifr.ch)
 Description : An algorithm for computing cycle ratio
 
 Copyright (C) 2021 by Tianlong Fan. All rights reserved.

 Please cite the following paper if used:
   Fan T, Lü L, Shi D, et al. Characterizing cycle structure in complex networks. 
   arXiv preprint arXiv:2001.08541, 2020.
 ============================================================================
'''

# -*-coding:GBK-*-
__author__ = 'tianlong'

import time
import networkx as nx
import itertools



NetworkAddress = r'Network file path'
OutputDistributionFile = 'outputpath'
networkName = 'networkname'


Mygraph = nx.Graph()

rawC = 0
file = open(NetworkAddress)
while 1:
    lines = file.readlines(10000)
    if not lines:
        break
    for line in lines:
        #input format of the network
        line = line[:-1]
        Mygraph.add_edge(int(line[:6]), int(line[7:]))
file.close()




NodeNum = Mygraph.number_of_nodes()  #
print(networkName)
print('Number of nodes = ', NodeNum)
print("Number of deges:", Mygraph.number_of_edges())



DEF_IMPOSSLEN = NodeNum + 1 #Impossible simple cycle length

SmallestCycles = set()
NodeGirth = dict()
NumSmallCycles = 0
CycLenDict = dict()
CycleRatio = {}

SmallestCyclesOfNodes = {} #




Coreness = nx.core_number(Mygraph)

removeNodes =set()
for i in Mygraph.nodes():  #
    SmallestCyclesOfNodes[i] = set()
    CycleRatio[i] = 0
    if Mygraph.degree(i) <= 1 or Coreness[i] <= 1:
        NodeGirth[i] = 0
        removeNodes.add(i)
    else:
        NodeGirth[i] = DEF_IMPOSSLEN



Mygraph.remove_nodes_from(removeNodes)  #
NumNode = Mygraph.number_of_nodes()  #update

for i in range(3,Mygraph.number_of_nodes()+2):
    CycLenDict[i] = 0



def my_all_shortest_paths(G, source, target):
    pred = nx.predecessor(G, source)
    if target not in pred:
        raise nx.NetworkXNoPath(
            f"Target {target} cannot be reached" f"from given sources"
        )
    sources = {source}
    seen = {target}
    stack = [[target, 0]]
    top = 0
    while top >= 0:
        node, i = stack[top]
        if node in sources:
            yield [p for p, n in reversed(stack[: top + 1])]
        if len(pred[node]) > i:
            stack[top][1] = i + 1
            next = pred[node][i]
            if next in seen:
                continue
            else:
                seen.add(next)
            top += 1
            if top == len(stack):
                stack.append([next, 0])
            else:
                stack[top][:] = [next, 0]
        else:
            seen.discard(node)
            top -= 1


def getandJudgeSimpleCircle(objectList):#
    numEdge = 0
    for eleArr in list(itertools.combinations(objectList, 2)):
        if Mygraph.has_edge(eleArr[0], eleArr[1]):
            numEdge += 1
    if numEdge != len(objectList):
        return False
    else:
        return True


def getSmallestCycles():
    NodeList = list(Mygraph.nodes())
    NodeList.sort()
    #setp 1
    curCyc = list()
    for ix in NodeList[:-2]:  #v1
        if NodeGirth[ix] == 0:
            continue
        curCyc.append(ix)
        for jx in NodeList[NodeList.index(ix) + 1 : -1]:  #v2
            if NodeGirth[jx] == 0:
                continue
            curCyc.append(jx)
            if Mygraph.has_edge(ix,jx):
                for kx in NodeList[NodeList.index(jx) + 1:]:      #v3
                    if NodeGirth[kx] == 0:
                        continue
                    if Mygraph.has_edge(kx,ix):
                        curCyc.append(kx)
                        if Mygraph.has_edge(kx,jx):
                            SmallestCycles.add(tuple(curCyc))
                            for i in curCyc:
                                NodeGirth[i] = 3
                        curCyc.pop()
            curCyc.pop()
        curCyc.pop()
    # setp 2
    ResiNodeList = []  # Residual Node List
    for nod in NodeList:
        if NodeGirth[nod] == DEF_IMPOSSLEN:
            ResiNodeList.append(nod)
    if len(ResiNodeList) == 0:
        return
    else:
        visitedNodes = dict.fromkeys(ResiNodeList,set())
        for nod in ResiNodeList:
            if Coreness[nod] == 2 and NodeGirth[nod] < DEF_IMPOSSLEN:
                continue
            for nei in list(Mygraph.neighbors(nod)):
                if Coreness[nei] == 2 and NodeGirth[nei] < DEF_IMPOSSLEN:
                    continue
                if not nei in visitedNodes.keys() or not nod in visitedNodes[nei]:
                    visitedNodes[nod].add(nei)
                    if nei not in visitedNodes.keys():
                        visitedNodes[nei] = set([nod])
                    else:
                        visitedNodes[nei].add(nod)
                    if Coreness[nei] == 2 and NodeGirth[nei] < DEF_IMPOSSLEN:
                        continue
                    Mygraph.remove_edge(nod, nei)
                    if nx.has_path(Mygraph, nod, nei):
                        for path in my_all_shortest_paths(Mygraph, nod, nei):
                            lenPath = len(path)
                            path.sort()
                            SmallestCycles.add(tuple(path))
                            for i in path:
                                if NodeGirth[i] > lenPath:
                                    NodeGirth[i] = lenPath
                    Mygraph.add_edge(nod, nei)





def StatisticsAndCalculateIndicators(): #
    global NumSmallCycles
    NumSmallCycles = len(SmallestCycles)
    for cyc in SmallestCycles:
        lenCyc = len(cyc)
        CycLenDict[lenCyc] += 1
        for nod in cyc:
            SmallestCyclesOfNodes[nod].add(cyc)
    for objNode,SmaCycs in SmallestCyclesOfNodes.items():
        if len(SmaCycs) == 0:
            continue
        cycleNeighbors = set()
        NeiOccurTimes = {}
        for cyc in SmaCycs:
            for n in cyc:
                if n in NeiOccurTimes.keys():
                    NeiOccurTimes[n] += 1
                else:
                    NeiOccurTimes[n] = 1
            cycleNeighbors = cycleNeighbors.union(cyc)
        cycleNeighbors.remove(objNode)
        del NeiOccurTimes[objNode]
        sum = 0
        for nei in cycleNeighbors:
            sum += float(NeiOccurTimes[nei]) / len(SmallestCyclesOfNodes[nei])
        CycleRatio[objNode] = sum + 1




def printAndOutput_ResultAndDistribution(objectList,nameString,Outpath):
    addrespath = Outpath + nameString + '.txt'
    Distribution = {}#

    for value in objectList.values():
        if value in Distribution.keys():
            Distribution[value] += 1
        else:
            Distribution[value] = 1

    for (myk, myv) in Distribution.items():
        Distribution[myk] = myv / float(NodeNum)

    rankedDict_ObjectList = sorted(objectList.items(), key=lambda d: d[1], reverse=True)
    fileout3 = open(addrespath, 'w')
    for d in range(len(rankedDict_ObjectList)):
        fileout3.writelines("%6d %12.6f  \n" % (rankedDict_ObjectList[d][0],rankedDict_ObjectList[d][1]))
    fileout3.close()
    addrespath2 = Outpath + 'Distribution_' + nameString + '.txt'
    fileout2 = open(addrespath2, 'w')
    for (myk, myv) in Distribution.items():
        fileout2.writelines("%12.6f %12.6f  \n" % (myk, myv))
    fileout2.close()


def printAndOutput_BasicCirclesDistribution(myCycLenDict,nameString,Outpath): #Copy_AllSimpleCircle
    Distribution = myCycLenDict
    global NumSmallCycles
    print('\nDistribution of SmallestBasicCycles:')
    float_allBasicCircles = float(NumSmallCycles)
    addrespath2 = Outpath + 'Distribution_' + nameString + '.txt'
    fileout2 = open(addrespath2, 'w')
    for (myk, myv) in Distribution.items():
        if myv > 0:
            fileout2.writelines("%10d %15d  %12.6f  \n" % (myk, myv,myv/float_allBasicCircles))
            print('len:%10d,count:%10d,ratio:%12.6f' % (myk, myv,myv/float_allBasicCircles))
    fileout2.close()

    List= list(SmallestCycles)
    rankedSBC_Set = sorted(List, key=lambda d: len(d), reverse=True)
    addrespath3 = Outpath + 'allSmallestBasicCycles.txt'
    fileout3 = open(addrespath3, 'w')
    for cy in rankedSBC_Set:
        fileout3.writelines("%s\n" %list(cy))
    fileout3.close()





# main fun
StartTime = time.time()
getSmallestCycles()
EndTime1 = time.time()

StatisticsAndCalculateIndicators()


#output
printAndOutput_ResultAndDistribution(CycleRatio, 'CycleRatio', OutputDistributionFile)
printAndOutput_BasicCirclesDistribution(CycLenDict, 'SmallestBasicCircles',OutputDistributionFile)

Kenaddrespath = OutputDistributionFile + 'Total_SBC_' + networkName + '.txt'
fileoutKen = open(Kenaddrespath, 'w')

fileoutKen.writelines('networkName: %s\n' %networkName)
print('\nThe total number of the shortest basic cycles: %20d' % NumSmallCycles)
print('Time: ',EndTime1-StartTime)
fileoutKen.writelines('The total number of the shortest basic cycles: %20d\n' %NumSmallCycles)
fileoutKen.writelines('Time: %20.6f\n' % (EndTime1-StartTime))
fileoutKen.close()








