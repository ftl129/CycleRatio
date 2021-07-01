# -*-coding:GBK-*-

__author__ = 'tianlong'


import time
import networkx as nx
import collections

import itertools #��Ӧ�ɵ���֤һ��Ȧ�Ƿ��Ǽ�Ȧ�ķ���
import copy






NetworkAddress = r'Input an path of a netowrk'
OutputDistributionFile ='Input an path to save the result'
networkName = 'Net name'



Mygraph = nx.Graph()

file = open(NetworkAddress)
while 1:
    lines = file.readlines(10000)
    if not lines:
        break
    for line in lines:
        line = line[:-1]
        Mygraph.add_edge(int(line[:6]), int(line[7:]))


file.close()


# #ʾ������
# Mygraph.add_edge(1,2)
# Mygraph.add_edge(1,3)
# Mygraph.add_edge(1,4)
# Mygraph.add_edge(1,5)
# Mygraph.add_edge(2,3)
# Mygraph.add_edge(2,4)
# Mygraph.add_edge(2,5)
# Mygraph.add_edge(3,4)
# Mygraph.add_edge(3,6)
# Mygraph.add_edge(3,8)
# Mygraph.add_edge(6,7)
# Mygraph.add_edge(7,8)
#
# Mygraph.add_edge(5,9)
# Mygraph.add_edge(9,10)
# Mygraph.add_edge(9,11)


# Mygraph.add_edge(9,12)
# Mygraph.add_edge(9,13)
# Mygraph.add_edge(9,14)





FTL = Mygraph.number_of_nodes()
print (networkName)
print ('FTL = ', FTL)


myalltime = []
CycleRatio = {} #Ȧ��
CycleNumber = {} #Ȧ��
SmallestCyclesOfNodes = {} #�ڵ����СȦ
Perimeter ={} #�ڵ���ܳ�
alltempCircle = set() #��¼����cyles,������cycle���ظ������粻�����[1,2,3]��[1,3,2]��

for i in Mygraph.nodes(): #��ʼ��
    Perimeter[i] = 0  #ȫ����ʼ��Ϊ0
    SmallestCyclesOfNodes[i] = set()
    CycleNumber[i] = 0



#ɾ������ֵ����1�ĵ㼰�����������ڵ�֮�������
def pruningNodesWithCoreness1():
    CorenessDict = nx.core_number(Mygraph)
    for id,value in CorenessDict.items():
        if value == 1:
            # print("ID = %5d,Coreness = %5d"%(id,value))
            CycleRatio[id] = 0 #��Ȧ�ṹ���ʶ�����0
            Mygraph.remove_node(id)







def getandJudgeSimpleCircle(objectList):#����1���Ǽ򵥻���������
    isSimpleCycle = False
    cycle = list(objectList)
    if objectList.__len__() == 3:
        if Mygraph.has_edge(cycle[0], cycle[1]) and Mygraph.has_edge(cycle[0], cycle[2]) and Mygraph.has_edge(cycle[1], cycle[2]):
            isSimpleCycle = True  # ��������
    else:
        CircleCheck = []
        numEdge = 0
        for eleArr in list(itertools.combinations(objectList, 2)):
            if Mygraph.has_edge(eleArr[0], eleArr[1]):
                numEdge = numEdge + 1
                CircleCheck.append([eleArr[0], eleArr[1]])
        if numEdge != objectList.__len__():
            return []
        path = []
        CircleCheck2 = copy.deepcopy(CircleCheck)
        iniLen = CircleCheck2.__len__()
        inde = 0
        while 1:
            inde = 0
            restL0 = CircleCheck2.__len__()
            for i, j in CircleCheck.__iter__():
                if path.__len__() == 0:
                    path.append(i)
                    path.append(j)
                    CircleCheck2.pop(inde)
                elif i == path[-1]:
                    path.append(j)
                    CircleCheck2.pop(inde)
                elif i == path[0]:
                    path.insert(0, j)
                    CircleCheck2.pop(inde)
                elif j == path[-1]:
                    path.append(i)
                    CircleCheck2.pop(inde)
                elif j == path[0]:
                    path.insert(0, i)
                    CircleCheck2.pop(inde)
                else:
                    inde = inde + 1
            if CircleCheck2.__len__() == 0:
                break
            if restL0 == CircleCheck2.__len__():
                break
            CircleCheck = copy.deepcopy(CircleCheck2)
        if path.__len__() == iniLen + 1 and path[0] == path[-1]:
            isSimpleCycle = True



    if isSimpleCycle:
        cycle.sort()
        Cyclen = cycle.__len__()

        global alltempCircle

        if tuple(cycle) not in alltempCircle:
            addFlag = False
            for elementC in cycle:
                if Perimeter[elementC] == 0:
                    addFlag = True
                    Perimeter[elementC] = Cyclen
                elif Perimeter[elementC] == Cyclen:
                    addFlag = True
                elif Perimeter[elementC] > Cyclen:
                    Perimeter[elementC] = Cyclen
                    addFlag = True

            if addFlag == 1:
                # print '����Ȧ��',cycle
                alltempCircle.add(tuple(cycle))
        else:
            return 0  #



# BFS algorithm
def SmallestCyclesSetBasedBFS(root):
    # AccessStr = list()
    AccessStr = collections.deque()
    AccessStr.append(set([root]))
    queue = collections.deque([root])
    LayerNum = 0
    while queue:  # ����ܳ�����0�����ѭ��
        vertex = queue.popleft()
        curAccStr = set(AccessStr.popleft())

        for neighbour in Mygraph.neighbors(vertex):
                # print 'neighbour',neighbour
                if len(curAccStr)<3:
                    if neighbour != root:
                        queue.append(neighbour)
                        newStr = curAccStr | set([neighbour])
                        AccessStr.append(newStr)
                else:
                    if neighbour == root:
                        # print 'neighbour == root'
                        getandJudgeSimpleCircle(curAccStr)
                    else:
                        if not neighbour in curAccStr:
                            if Perimeter[root]==0:
                                queue.append(neighbour)
                                newStr = curAccStr | set([neighbour])
                                AccessStr.append(newStr)
        LayerNum += 1






Copy_AllSimpleCircle = set()

def StatisticsAndCalculateIndicators(): #
    while len(alltempCircle)>0:
        tempNodeC =alltempCircle.pop()
        shortestLengthC = len(tempNodeC)
        circleClock = False
        for elementC in tempNodeC:
            if Perimeter[elementC] == shortestLengthC:
                SmallestCyclesOfNodes[elementC].add(tempNodeC)
                CycleNumber[elementC] = CycleNumber[elementC] + 1
                circleClock = True
        if circleClock:
            Copy_AllSimpleCircle.add(tempNodeC)
    for SBc in Copy_AllSimpleCircle:
        LengthSBc = len(SBc)
        for elementSBc in SBc:
            if Perimeter[elementSBc] < LengthSBc:
                SmallestCyclesOfNodes[elementSBc].add(SBc)
                CycleNumber[elementC] = CycleNumber[elementC] + 1

    for objNode,SmaCycs in SmallestCyclesOfNodes.items():
        # print 'objNode,SmaCycs',objNode,SmaCycs
        if len(SmaCycs)==0:
            continue
        cycleNeighbors =set()#Ȧ�ھ�
        NeiOccurTimes = {} #�ھӳ��ִ���
        for cyc in SmaCycs:
            for n in cyc:
                if n in NeiOccurTimes.keys():
                    NeiOccurTimes[n] +=1
                else:
                    NeiOccurTimes[n] = 1
            # print 'cycleNeighbors,', cycleNeighbors
            cycleNeighbors = cycleNeighbors.union(cyc)
            # print 'cyc,',cyc
            # print 'cycleNeighbors,', cycleNeighbors
        cycleNeighbors.remove(objNode)#�Ƴ�Ŀ��ڵ�
        del NeiOccurTimes[objNode]
        # print 'cycleNeighbors,', cycleNeighbors
        # print 'NeiOccurTimes,', NeiOccurTimes
        sum = 0
        for nei in cycleNeighbors:
            # print nei
            # print 'SmallestCyclesOfNodes[nei]:',SmallestCyclesOfNodes[nei],len(SmallestCyclesOfNodes[nei])
            # print NeiOccurTimes[nei], len(SmallestCyclesOfNodes[nei])
            sum += float(NeiOccurTimes[nei]) / len(SmallestCyclesOfNodes[nei])
        CycleRatio[objNode] = sum + 1 #�����Լ�
        # print 'Ȧ��: ',objNode,CycleRatio[objNode]




def printAndOutput_ResultAndDistribution(objectList,nameString,Outpath):
    Listname = nameString
    addrespath = Outpath + Listname + '.txt'
    Distribution = {}#

    for value in objectList.values():
        if value in Distribution.keys():
            Distribution[value] += 1
        else:
            Distribution[value] = 1

    for (myk, myv) in Distribution.items():
        Distribution[myk] = myv / float(FTL)

    rankedDict_ObjectList = sorted(objectList.items(), key=lambda d: d[1], reverse=True)
    fileout3 = open(addrespath, 'w')
    for d in range(len(rankedDict_ObjectList)):
        fileout3.writelines("%6d %12.6f  \n" % (rankedDict_ObjectList[d][0],rankedDict_ObjectList[d][1]))
    fileout3.close()
    addrespath2 = Outpath + 'Distribution_' + Listname + '.txt'
    fileout2 = open(addrespath2, 'w')
    for (myk, myv) in Distribution.items():
        fileout2.writelines("%12.6f %12.6f  \n" % (myk, myv))
    fileout2.close()





def printAndOutput_BasicCirclesDistribution(objectList,nameString,Outpath): #Copy_AllSimpleCircle
    Listname = nameString
    Distribution = {}#
    for di in objectList:  #
        lendi = len(di)
        if lendi in Distribution.keys():
            Distribution[lendi] += 1
        else:
            Distribution[lendi] = 1
    allBasicCircles = Copy_AllSimpleCircle.__len__()
    print ('\nDistributionofSmallestBasicCycles:')
    float_allBasicCircles = float(allBasicCircles)
    addrespath2 = Outpath + 'Distribution_' + Listname + '.txt'
    fileout2 = open(addrespath2, 'w')
    for (myk, myv) in Distribution.items():
        fileout2.writelines("%10d %15d  %12.6f  \n" % (myk, myv,myv/float_allBasicCircles))
        print ('len:%10d,count:%10d,pro:%12.6f' % (myk, myv,myv/float_allBasicCircles))
    fileout2.close()


    #����������С����Ȧ���� ���ճ��ȴӴ�С
    List= list(objectList)
    rankedSBC_Set = sorted(List, key=lambda d: len(d), reverse=True)
    addrespath3 = Outpath + 'allSmallestBasicCycles.txt'
    fileout3 = open(addrespath3, 'w')
    for cy in rankedSBC_Set:
        # print 'cy:',cy
        fileout3.writelines("%s\n" %list(cy))
    fileout3.close()


    return (Distribution, allBasicCircles)




#������
pruningNodesWithCoreness1()
time_start = time.time()
for i in Mygraph.nodes:
    # print '����ڵ����СȦ:',i
    SmallestCyclesSetBasedBFS(i)

time_end = time.time();  # time.time()Ϊ1970.1.1����ǰʱ��ĺ�����

print ('\n\n\n\n����Ȧ�����ܹ���ʱ��'),
myalltime.append(time_end - time_start)
print (time_end - time_start),
print ("s")

StatisticsAndCalculateIndicators()

# SBC_Distribution = {}
# SBC_NUM = 0

printAndOutput_ResultAndDistribution(Perimeter, 'Perimeter', OutputDistributionFile)
printAndOutput_ResultAndDistribution(CycleNumber, 'CycleNumber', OutputDistributionFile)
printAndOutput_ResultAndDistribution(CycleRatio, 'CycleRatio', OutputDistributionFile)
SBC_Distribution, SBC_NUM = printAndOutput_BasicCirclesDistribution(Copy_AllSimpleCircle, 'SmallestBasicCircles',
                                                                    OutputDistributionFile)

Kenaddrespath = OutputDistributionFile + 'Total_SBC_' + networkName + '.txt'
fileoutKen = open(Kenaddrespath, 'w')

print ('\n��С����Ȧ������%20d' % Copy_AllSimpleCircle.__len__())
# print ('����ʱ�䣺%20.2f\n' % myalltime[0])
fileoutKen.writelines('��С����Ȧ������%20d\n' % Copy_AllSimpleCircle.__len__())
fileoutKen.writelines('����ʱ�䣺%20.2f\n' % myalltime[0])
fileoutKen.close()







