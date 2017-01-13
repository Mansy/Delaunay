import tkinter
import random
import numpy as np
import math
import copy

_WINDOW_SIZE = [1000, 1000]


def TrueY(COORDY):
    return _WINDOW_SIZE[1] - COORDY


class RIB(object):
    def __init__(self, NODES, TRIANGLES=None):
        self.NODES = [NODES[0], NODES[1]]

        if TRIANGLES is None:
            self.TRIANGLES = [None, None]
        else:
            self.TRIANGLES = [TRIANGLES[0], TRIANGLES[1]]


class TRIANGLE(object):
    def __init__(self, NODES, RIBS=None):
        self.NODES = NODES

        if RIBS is None:
            self.RIBS = [None, None, None]
        else:
            self.RIBS = RIBS


class DelaunayHelper(object):
    @staticmethod
    def ROTATE(A, B, C):
        return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])

    @staticmethod
    def Jarvis(ARRAY):
        def ROTATE(A, B, C):
            return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])

        PointsList = ARRAY[:]
        for i in range(1, len(PointsList)):
            if PointsList[i][0] < PointsList[0][0]:
                PointsList[i], PointsList[0] = PointsList[0], PointsList[i]

        HullNodes = [PointsList[0]]
        del PointsList[0]
        PointsList.append(HullNodes[0])

        while True:
            Right = 0
            for i in range(1, len(PointsList)):
                if ROTATE(HullNodes[-1], PointsList[Right], PointsList[i]) < 0:
                    Right = i
            if PointsList[Right] == HullNodes[0]:
                break
            else:
                HullNodes.append(PointsList[Right])
                del PointsList[Right]
        return HullNodes

    @staticmethod
    def DelaunayCheck(LIST):
        def GETPosFromCommonNodes(TNODES, COMMONNODES):
            return [pos for pos, node in enumerate(TNODES) if node not in COMMONNODES][0]

        def GETNeighborTriangle(Triangle, TRIANGLELIST):
            return TRIANGLELIST[1] if TRIANGLELIST[0] == Triangle else TRIANGLELIST[0]

        def CalculateAngle(A, B, C):
            AB = math.sqrt((B[0] - A[0]) * (B[0] - A[0]) + (B[1] - A[1]) * (B[1] - A[1]))
            AC = math.sqrt((C[0] - A[0]) * (C[0] - A[0]) + (C[1] - A[1]) * (C[1] - A[1]))
            BC = math.sqrt((C[0] - B[0]) * (C[0] - B[0]) + (C[1] - B[1]) * (C[1] - B[1]))
            cosA = (AB * AB + AC * AC - BC * BC) / (2 * AB * AC)
            return math.acos(cosA) * (180 / math.pi)

        for CurrentTriangle in LIST:
            for rib in CurrentTriangle.RIBS:
                if None not in rib.TRIANGLES:
                    NeighborTriangle = GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=rib.TRIANGLES)
                    NodeList = [rib.NODES[0], rib.NODES[1], CurrentTriangle.NODES[GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=rib.NODES)],
                                NeighborTriangle.NODES[GETPosFromCommonNodes(TNODES=NeighborTriangle.NODES, COMMONNODES=rib.NODES)]]
                    if CalculateAngle(NodeList[2], NodeList[0], NodeList[1]) + CalculateAngle(NodeList[3], NodeList[0], NodeList[1]) > 180:
                        return False
        return True

    @staticmethod
    def CalculateAngle(A, B, C):
        AB = math.sqrt((B[0] - A[0]) * (B[0] - A[0]) + (B[1] - A[1]) * (B[1] - A[1]))
        AC = math.sqrt((C[0] - A[0]) * (C[0] - A[0]) + (C[1] - A[1]) * (C[1] - A[1]))
        BC = math.sqrt((C[0] - B[0]) * (C[0] - B[0]) + (C[1] - B[1]) * (C[1] - B[1]))
        cosA = (AB * AB + AC * AC - BC * BC) / (2 * AB * AC)
        return math.acos(cosA) * (180 / math.pi)

    @staticmethod
    def GETNeighborTriangle(Triangle, TRIANGLELIST):
        return TRIANGLELIST[1] if TRIANGLELIST[0] == Triangle else TRIANGLELIST[0]

    @staticmethod
    def GETCommonNodes(NODES1, NODES2):
        return list(set(tuple(node) for node in NODES1) & set(tuple(node) for node in NODES2))

    @staticmethod
    def GETPosFromCommonNodes(TNODES, COMMONNODES):
        return [pos for pos, node in enumerate(TNODES) if node not in COMMONNODES][0]

    @staticmethod
    def CHECKSearchCondition(Triangle, NODE):
        def ROTATE(A, B, C):
            return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])

        for POS, Rib in enumerate(Triangle.RIBS):
            C1 = ROTATE(A=Rib.NODES[0], B=Rib.NODES[1], C=NODE)
            C2 = ROTATE(A=Rib.NODES[0], B=Rib.NODES[1], C=Triangle.NODES[POS])
            if C1 > 0 > C2 or C1 < 0 < C2:
                return True
        return False

    @staticmethod
    def GETCountTriangles(Triangle):
        return len([rib for rib in Triangle.RIBS if None not in rib.TRIANGLES])

    @staticmethod
    def CHECKNodeInTriangleFloat(TNODES, NODE):
        T1 = (TNODES[0][0] - NODE[0]) * (TNODES[1][1] - TNODES[0][1]) - \
             (TNODES[1][0] - TNODES[0][0]) * (TNODES[0][1] - NODE[1])

        T2 = (TNODES[1][0] - NODE[0]) * (TNODES[2][1] - TNODES[1][1]) - \
             (TNODES[2][0] - TNODES[1][0]) * (TNODES[1][1] - NODE[1])

        T3 = (TNODES[2][0] - NODE[0]) * (TNODES[0][1] - TNODES[2][1]) - \
             (TNODES[0][0] - TNODES[2][0]) * (TNODES[2][1] - NODE[1])

        if (T1 >= 0 and T2 >= 0 and T3 >= 0) or (T1 <= 0 and T2 <= 0 and T3 <= 0):
            return 2 if T1 == 0 or T2 == 0 or T3 == 0 else 1
        else:
            return 0

    @staticmethod
    def CHECKNodeInTriangleInt(TNODES, NODE):
        T1 = (round(TNODES[0][0]) - round(NODE[0])) * (round(TNODES[1][1]) - round(TNODES[0][1])) - \
             (round(TNODES[1][0]) - round(TNODES[0][0])) * (round(TNODES[0][1]) - round(NODE[1]))

        T2 = (round(TNODES[1][0]) - round(NODE[0])) * (round(TNODES[2][1]) - round(TNODES[1][1])) - \
             (round(TNODES[2][0]) - round(TNODES[1][0])) * (round(TNODES[1][1]) - round(NODE[1]))

        T3 = (round(TNODES[2][0]) - round(NODE[0])) * (round(TNODES[0][1]) - round(TNODES[2][1])) - \
             (round(TNODES[0][0]) - round(TNODES[2][0])) * (round(TNODES[2][1]) - round(NODE[1]))

        if (T1 >= 0 and T2 >= 0 and T3 >= 0) or (T1 <= 0 and T2 <= 0 and T3 <= 0):
            return 2 if T1 == 0 or T2 == 0 or T3 == 0 else 1
        else:
            return 0


class DelaunayMethod(object):
    def __init__(self, NODELIST, CANVAS):
        self.CANVAS = CANVAS
        self.HelpMethod = DelaunayHelper

        # Structure For Triangle
        self.NodeList = NODELIST
        self.HullNodes = []
        self.TriangleList = []

        # Hash Parameters
        self.Hash_R = 3
        self.Hash_CurrentHashSize = 2
        self.Hash_MaxPointsInHash = self.Hash_R * self.Hash_R * self.Hash_CurrentHashSize
        self.HashArray = np.empty((self.Hash_CurrentHashSize, self.Hash_CurrentHashSize), dtype=object)
        self.HashIndex = [0, 0]

    def Start(self):
        print('Start Delaunay Algorithm')
        print('Create Hull. Method - Jarvis')
        self.HullNodes = self.HelpMethod.Jarvis(ARRAY=self.NodeList)

        print('Remove Hull Nodes From NodeList')
        for Node in self.HullNodes:
            self.NodeList.remove(Node)

        ZeroNode = self.HullNodes.pop(0)
        print('\nStart Creating Triangles From Jarvis Hull')
        for i in range(len(self.HullNodes) - 1):
            NewTriangle = TRIANGLE(NODES=self.HelpMethod.Jarvis(ARRAY=[ZeroNode, self.HullNodes[i], self.HullNodes[i + 1]]))
            self.TriangleList.append(NewTriangle)
            print('Was Create Triangle ', NewTriangle.NODES)

        print('Create Ribs for Triangles')
        for CurrentTriangle in self.TriangleList:
            print('\nCurrent Triangle ==> ', CurrentTriangle.NODES)
            for ViewedTriangle in self.TriangleList:
                if CurrentTriangle != ViewedTriangle:
                    CommonNodes = self.HelpMethod.GETCommonNodes(NODES1=CurrentTriangle.NODES, NODES2=ViewedTriangle.NODES)
                    if len(CommonNodes) == 2:
                        CommonNodes = [list(CommonNodes[0]), list(CommonNodes[1])]
                        cpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=CommonNodes)
                        vpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=ViewedTriangle.NODES, COMMONNODES=CommonNodes)
                        CommonRib = RIB(NODES=CommonNodes, TRIANGLES=[CurrentTriangle, ViewedTriangle])
                        if CurrentTriangle.RIBS[cpos] is None and ViewedTriangle.RIBS[vpos] is None:
                            CurrentTriangle.RIBS[cpos] = CommonRib
                            ViewedTriangle.RIBS[vpos] = CommonRib

                        elif CurrentTriangle.RIBS[cpos] is not None and ViewedTriangle.RIBS[vpos] is None:
                            Rib = CurrentTriangle.RIBS[cpos]
                            Rib.NODES = CommonNodes
                            Rib.TRIANGLES = [CurrentTriangle, ViewedTriangle]
                            ViewedTriangle.RIBS[vpos] = Rib

                        elif CurrentTriangle.RIBS[cpos] is None and ViewedTriangle.RIBS[vpos] is not None:
                            Rib = ViewedTriangle.RIBS[vpos]
                            Rib.NODES = CommonNodes
                            Rib.TRIANGLES = [ViewedTriangle, CurrentTriangle]
                            CurrentTriangle.RIBS[cpos] = Rib

                        elif CurrentTriangle.RIBS[cpos] is not None and ViewedTriangle.RIBS[vpos] is not None:
                            if CurrentTriangle.RIBS[cpos] != ViewedTriangle.RIBS[vpos]:
                                CurrentTriangle.RIBS[cpos] = CommonRib
                                ViewedTriangle.RIBS[vpos] = CommonRib
                        print('\nWas Create Rib: ', CurrentTriangle.RIBS[cpos].NODES)
                        print('Between ', CurrentTriangle.NODES, ' and ', ViewedTriangle.NODES)

            for pos, rib in enumerate(CurrentTriangle.RIBS):
                if rib is None:
                    Nodes = CurrentTriangle.NODES[:]
                    Nodes.remove(CurrentTriangle.NODES[pos])
                    CurrentTriangle.RIBS[pos] = RIB(NODES=Nodes, TRIANGLES=[CurrentTriangle, None])

            if len([x for x in CurrentTriangle.RIBS if x is not None]) != 3:
                raise ValueError

        self.CANVAS.ParentFrame.TK.update()
        print('Rebuild To Delaunay')
        count = 0
        while not self.HelpMethod.DelaunayCheck(LIST=self.TriangleList):
            count += 1
            for CurrentTriangle in self.TriangleList:
                for rib in CurrentTriangle.RIBS:
                    if None not in rib.TRIANGLES:
                        NeighborTriangle = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=rib.TRIANGLES)
                        NodeList = [rib.NODES[0], rib.NODES[1], CurrentTriangle.NODES[self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=rib.NODES)],
                                    NeighborTriangle.NODES[self.HelpMethod.GETPosFromCommonNodes(TNODES=NeighborTriangle.NODES, COMMONNODES=rib.NODES)]]
                        if self.HelpMethod.CalculateAngle(NodeList[2], NodeList[0], NodeList[1]) + self.HelpMethod.CalculateAngle(NodeList[3], NodeList[0], NodeList[1]) > 180:
                            NODES1 = [NodeList[3], NodeList[2], NodeList[0]]
                            NODES2 = [NodeList[3], NodeList[2], NodeList[1]]
                            RIBNODES = [NodeList[3], NodeList[2]]

                            NRibs = NeighborTriangle.RIBS[:]
                            CRibs = CurrentTriangle.RIBS[:]

                            print('\nRebuild: ', NodeList[0], NodeList[1], NodeList[2], ' and ', NodeList[0], NodeList[1], NodeList[3])
                            print('to: ', NodeList[3], NodeList[2], NodeList[0], ' and ', NodeList[3], NodeList[2], NodeList[1])

                            CurrentTriangle.NODES = self.HelpMethod.Jarvis(ARRAY=NODES1)
                            CurrentTriangle.RIBS = [None, None, None]

                            NeighborTriangle.NODES = self.HelpMethod.Jarvis(ARRAY=NODES2)
                            NeighborTriangle.RIBS = [None, None, None]

                            CommonRib = RIB(NODES=RIBNODES, TRIANGLES=[CurrentTriangle, NeighborTriangle])
                            cpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=CommonRib.NODES)
                            npos = self.HelpMethod.GETPosFromCommonNodes(TNODES=NeighborTriangle.NODES, COMMONNODES=CommonRib.NODES)

                            CurrentTriangle.RIBS[cpos] = CommonRib
                            NeighborTriangle.RIBS[npos] = CommonRib

                            for R in NRibs:
                                if R.NODES[0] in CurrentTriangle.NODES and R.NODES[1] in CurrentTriangle.NODES:
                                    if CurrentTriangle in R.TRIANGLES:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=R.TRIANGLES)
                                    else:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=NeighborTriangle, TRIANGLELIST=R.TRIANGLES)

                                    cpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=R.NODES)
                                    R.TRIANGLES = [T, CurrentTriangle]
                                    CurrentTriangle.RIBS[cpos] = R

                                if R.NODES[0] in NeighborTriangle.NODES and R.NODES[1] in NeighborTriangle.NODES:
                                    if NeighborTriangle in R.TRIANGLES:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=NeighborTriangle, TRIANGLELIST=R.TRIANGLES)
                                    else:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=R.TRIANGLES)

                                    npos = self.HelpMethod.GETPosFromCommonNodes(TNODES=NeighborTriangle.NODES, COMMONNODES=R.NODES)
                                    R.TRIANGLES = [T, NeighborTriangle]
                                    NeighborTriangle.RIBS[npos] = R

                            for R in CRibs:
                                if R.NODES[0] in CurrentTriangle.NODES and R.NODES[1] in CurrentTriangle.NODES:
                                    if CurrentTriangle in R.TRIANGLES:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=R.TRIANGLES)
                                    else:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=NeighborTriangle, TRIANGLELIST=R.TRIANGLES)

                                    cpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=R.NODES)
                                    R.TRIANGLES = [T, CurrentTriangle]
                                    CurrentTriangle.RIBS[cpos] = R


                                if R.NODES[0] in NeighborTriangle.NODES and R.NODES[1] in NeighborTriangle.NODES:
                                    if NeighborTriangle in R.TRIANGLES:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=NeighborTriangle, TRIANGLELIST=R.TRIANGLES)
                                    else:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=R.TRIANGLES)

                                    npos = self.HelpMethod.GETPosFromCommonNodes(TNODES=NeighborTriangle.NODES, COMMONNODES=R.NODES)
                                    R.TRIANGLES = [T, NeighborTriangle]
                                    NeighborTriangle.RIBS[npos] = R
                            break

        print('Rebuild End By ', count, ' steeps')

        print('\nStart main loop for each NODE in NodeList')
        print('Initialize HashArray')
        for i in range(self.Hash_CurrentHashSize):
            for j in range(self.Hash_CurrentHashSize):
                self.HashArray[i, j] = self.TriangleList[0]

        for I in range(len(self.NodeList)):
        # for I in range(5):
            if I == self.Hash_MaxPointsInHash:
                print('Rebuild Hash array | reason - max points = ', I)
                self.RebuildHashArray()

            print('\n###########')
            print('NODE # ', I)
            print('###########\n')

            CurrentNode = self.NodeList[I]
            self.HashIndex = [math.trunc(CurrentNode[0] / (float(_WINDOW_SIZE[0]) / float(self.Hash_CurrentHashSize))),
                              math.trunc(TrueY(CurrentNode[1]) / (float(_WINDOW_SIZE[1]) / float(self.Hash_CurrentHashSize)))]

            CurrentTriangle = self.HashArray[self.HashIndex[0], self.HashIndex[1]]

            print('\nCurrent Node = ', CurrentNode)
            print('Current Triangle = ', CurrentTriangle.NODES)
            print('Hash Index = ', self.HashIndex)

            while self.HelpMethod.CHECKSearchCondition(Triangle=CurrentTriangle, NODE=CurrentNode):
                if self.HelpMethod.GETCountTriangles(Triangle=CurrentTriangle) == 1:
                    for rib in CurrentTriangle.RIBS:
                        if None not in rib.TRIANGLES:
                            CurrentTriangle = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=rib.TRIANGLES)
                            print('1 Triangle -> ', CurrentTriangle.NODES)

                else:
                    for pos, rib in enumerate(CurrentTriangle.RIBS):
                        if None not in rib.TRIANGLES:
                            C1 = self.HelpMethod.ROTATE(rib.NODES[0], rib.NODES[1], CurrentNode)
                            C2 = self.HelpMethod.ROTATE(rib.NODES[0], rib.NODES[1], CurrentTriangle.NODES[pos])
                            if C1 > 0 > C2 or C1 < 0 < C2:
                                CurrentTriangle = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=rib.TRIANGLES)
                                print('M Triangle -> ', CurrentTriangle.NODES)
                                break

            print('Search END. Triangle = ', CurrentTriangle.NODES, 'Node = ', CurrentNode)

            flag = self.HelpMethod.CHECKNodeInTriangleFloat(TNODES=CurrentTriangle.NODES, NODE=CurrentNode)
            if flag == 1:
                print('\nNode in Triangle')
                self.CreateThreeTriangles(CurrentTriangle=CurrentTriangle, CurrentNode=CurrentNode)
                SmallTriangleList = []
                print('set HASH ', self.HashIndex, ' triangle ', self.TriangleList[-1].NODES)

                SmallTriangleList.append(CurrentTriangle)
                SmallTriangleList.append(self.TriangleList[-2])
                SmallTriangleList.append(self.TriangleList[-1])
                self.UpdateToDelaunay(TriangleList=SmallTriangleList)

            elif flag == 2:
                pass

            else:
                flag = self.HelpMethod.CHECKNodeInTriangleInt(TNODES=CurrentTriangle.NODES, NODE=CurrentNode)
                if flag == 1:
                    print('\nNode in Triangle')
                    self.CreateThreeTriangles(CurrentTriangle=CurrentTriangle, CurrentNode=CurrentNode)
                    SmallTriangleList = []
                    print('set HASH ', self.HashIndex, ' triangle ', self.TriangleList[-1].NODES)

                    SmallTriangleList.append(CurrentTriangle)
                    SmallTriangleList.append(self.TriangleList[-2])
                    SmallTriangleList.append(self.TriangleList[-1])
                    self.UpdateToDelaunay(TriangleList=SmallTriangleList)

                elif flag == 2:
                    pass

                else:
                    print('error')

        self.Show()
        self.CANVAS.ParentFrame.TK.update()
        print('\nEND Method')

    def UpdateToDelaunay(self, TriangleList):
        count = 0
        while True:
            count += 1
            for CurrentTriangle in TriangleList:
                for rib in CurrentTriangle.RIBS:
                    if None not in rib.TRIANGLES:
                        NeighborTriangle = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=rib.TRIANGLES)
                        NodeList = [rib.NODES[0], rib.NODES[1], CurrentTriangle.NODES[self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=rib.NODES)],
                                    NeighborTriangle.NODES[self.HelpMethod.GETPosFromCommonNodes(TNODES=NeighborTriangle.NODES, COMMONNODES=rib.NODES)]]
                        if self.HelpMethod.CalculateAngle(NodeList[2], NodeList[0], NodeList[1]) + self.HelpMethod.CalculateAngle(NodeList[3], NodeList[0], NodeList[1]) > 180:
                            NODES1 = [NodeList[3], NodeList[2], NodeList[0]]
                            NODES2 = [NodeList[3], NodeList[2], NodeList[1]]
                            RIBNODES = [NodeList[3], NodeList[2]]

                            NRibs = NeighborTriangle.RIBS[:]
                            CRibs = CurrentTriangle.RIBS[:]

                            print('\nRebuild: ', NodeList[0], NodeList[1], NodeList[2], ' and ', NodeList[0], NodeList[1], NodeList[3])
                            print('to: ', NodeList[3], NodeList[2], NodeList[0], ' and ', NodeList[3], NodeList[2], NodeList[1])

                            CurrentTriangle.NODES = self.HelpMethod.Jarvis(ARRAY=NODES1)
                            CurrentTriangle.RIBS = [None, None, None]

                            NeighborTriangle.NODES = self.HelpMethod.Jarvis(ARRAY=NODES2)
                            NeighborTriangle.RIBS = [None, None, None]

                            CommonRib = RIB(NODES=RIBNODES, TRIANGLES=[CurrentTriangle, NeighborTriangle])
                            cpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=CommonRib.NODES)
                            npos = self.HelpMethod.GETPosFromCommonNodes(TNODES=NeighborTriangle.NODES, COMMONNODES=CommonRib.NODES)

                            CurrentTriangle.RIBS[cpos] = CommonRib
                            NeighborTriangle.RIBS[npos] = CommonRib

                            for R in NRibs:
                                if R.NODES[0] in CurrentTriangle.NODES and R.NODES[1] in CurrentTriangle.NODES:
                                    if CurrentTriangle in R.TRIANGLES:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=R.TRIANGLES)
                                    else:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=NeighborTriangle, TRIANGLELIST=R.TRIANGLES)

                                    cpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=R.NODES)
                                    R.TRIANGLES = [T, CurrentTriangle]
                                    CurrentTriangle.RIBS[cpos] = R

                                if R.NODES[0] in NeighborTriangle.NODES and R.NODES[1] in NeighborTriangle.NODES:
                                    if NeighborTriangle in R.TRIANGLES:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=NeighborTriangle, TRIANGLELIST=R.TRIANGLES)
                                    else:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=R.TRIANGLES)

                                    npos = self.HelpMethod.GETPosFromCommonNodes(TNODES=NeighborTriangle.NODES, COMMONNODES=R.NODES)
                                    R.TRIANGLES = [T, NeighborTriangle]
                                    NeighborTriangle.RIBS[npos] = R

                                for Tr in R.TRIANGLES:
                                    if Tr is not None and Tr not in TriangleList:
                                        TriangleList.append(Tr)

                            for R in CRibs:
                                if R.NODES[0] in CurrentTriangle.NODES and R.NODES[1] in CurrentTriangle.NODES:
                                    if CurrentTriangle in R.TRIANGLES:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=R.TRIANGLES)
                                    else:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=NeighborTriangle, TRIANGLELIST=R.TRIANGLES)

                                    cpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=R.NODES)
                                    R.TRIANGLES = [T, CurrentTriangle]
                                    CurrentTriangle.RIBS[cpos] = R

                                if R.NODES[0] in NeighborTriangle.NODES and R.NODES[1] in NeighborTriangle.NODES:
                                    if NeighborTriangle in R.TRIANGLES:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=NeighborTriangle, TRIANGLELIST=R.TRIANGLES)
                                    else:
                                        T = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=R.TRIANGLES)

                                    npos = self.HelpMethod.GETPosFromCommonNodes(TNODES=NeighborTriangle.NODES, COMMONNODES=R.NODES)
                                    R.TRIANGLES = [T, NeighborTriangle]
                                    NeighborTriangle.RIBS[npos] = R

                                for Tr in R.TRIANGLES:
                                    if Tr is not None and Tr not in TriangleList:
                                        TriangleList.append(Tr)

                            break
            if self.HelpMethod.DelaunayCheck(TriangleList):
                    break
        print('\nLoop was started ~ ', count)

    def CreateThreeTriangles(self, CurrentTriangle, CurrentNode):
        CRibs = CurrentTriangle.RIBS[:]
        CNodes = CurrentTriangle.NODES[:]
        T1NODES = self.HelpMethod.Jarvis(ARRAY=[CurrentNode, CurrentTriangle.NODES[0], CurrentTriangle.NODES[1]])
        T2NODES = self.HelpMethod.Jarvis(ARRAY=[CurrentNode, CurrentTriangle.NODES[1], CurrentTriangle.NODES[2]])
        T3NODES = self.HelpMethod.Jarvis(ARRAY=[CurrentNode, CurrentTriangle.NODES[2], CurrentTriangle.NODES[0]])

        print('New Triangle: ', T1NODES)
        print('New Triangle: ', T2NODES)
        print('New Triangle: ', T3NODES)

        CurrentTriangle.NODES = T1NODES
        CurrentTriangle.RIBS = [None, None, None]
        T2 = TRIANGLE(NODES=T2NODES)
        T3 = TRIANGLE(NODES=T3NODES)

        # CT and T2
        Nodes = self.HelpMethod.GETCommonNodes(NODES1=CurrentTriangle.NODES, NODES2=T2.NODES)
        Nodes = [list(Nodes[0]), list(Nodes[1])]
        cpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=Nodes)
        t2pos = self.HelpMethod.GETPosFromCommonNodes(TNODES=T2.NODES, COMMONNODES=Nodes)

        CommonRib = RIB(NODES=Nodes, TRIANGLES=[CurrentTriangle, T2])

        CurrentTriangle.RIBS[cpos] = CommonRib
        T2.RIBS[t2pos] = CommonRib

        # T2 and T3
        Nodes = self.HelpMethod.GETCommonNodes(NODES1=T3.NODES, NODES2=T2.NODES)
        Nodes = [list(Nodes[0]), list(Nodes[1])]
        t3pos = self.HelpMethod.GETPosFromCommonNodes(TNODES=T3.NODES, COMMONNODES=Nodes)
        t2pos = self.HelpMethod.GETPosFromCommonNodes(TNODES=T2.NODES, COMMONNODES=Nodes)

        CommonRib = RIB(NODES=Nodes, TRIANGLES=[T3, T2])

        T3.RIBS[t3pos] = CommonRib
        T2.RIBS[t2pos] = CommonRib

        # CT and T3
        Nodes = self.HelpMethod.GETCommonNodes(NODES1=CurrentTriangle.NODES, NODES2=T3.NODES)
        Nodes = [list(Nodes[0]), list(Nodes[1])]
        cpos = self.HelpMethod.GETPosFromCommonNodes(TNODES=CurrentTriangle.NODES, COMMONNODES=Nodes)
        t3pos = self.HelpMethod.GETPosFromCommonNodes(TNODES=T3.NODES, COMMONNODES=Nodes)

        CommonRib = RIB(NODES=Nodes, TRIANGLES=[CurrentTriangle, T3])

        CurrentTriangle.RIBS[cpos] = CommonRib
        T3.RIBS[t3pos] = CommonRib

        # CT and other
        cind = CurrentTriangle.RIBS.index(None)
        OldRib = CRibs[2]
        TmpTriangle = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=OldRib.TRIANGLES)
        if TmpTriangle is None:
            CurrentTriangle.RIBS[cind] = OldRib

        else:
            R = self.HelpMethod.GETPosFromCommonNodes(TNODES=TmpTriangle.NODES, COMMONNODES=OldRib.NODES)
            CurrentTriangle.RIBS[cind] = TmpTriangle.RIBS[R]

        # T2 and other
        t2ind = T2.RIBS.index(None)
        OldRib = CRibs[0]
        TmpTriangle = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=OldRib.TRIANGLES)
        if TmpTriangle is None:
            OldRib.TRIANGLES = [T2, None]
            T2.RIBS[t2ind] = OldRib
        else:
            R = self.HelpMethod.GETPosFromCommonNodes(TNODES=TmpTriangle.NODES, COMMONNODES=OldRib.NODES)
            T2.RIBS[t2ind] = TmpTriangle.RIBS[R]
            T2.RIBS[t2ind].TRIANGLES = [T2, TmpTriangle]

        # T3 and other
        t3ind = T3.RIBS.index(None)
        OldRib = CRibs[1]
        TmpTriangle = self.HelpMethod.GETNeighborTriangle(Triangle=CurrentTriangle, TRIANGLELIST=OldRib.TRIANGLES)
        if TmpTriangle is None:
            OldRib.TRIANGLES = [T3, None]
            T3.RIBS[t3ind] = OldRib
        else:
            R = self.HelpMethod.GETPosFromCommonNodes(TNODES=TmpTriangle.NODES, COMMONNODES=OldRib.NODES)
            T3.RIBS[t3ind] = TmpTriangle.RIBS[R]
            T3.RIBS[t3ind].TRIANGLES = [T3, TmpTriangle]

        self.HashArray[self.HashIndex[0], self.HashIndex[1]] = T3

        self.TriangleList.append(T2)
        self.TriangleList.append(T3)

    def RebuildHashArray(self):
        self.Hash_CurrentHashSize *= 2
        NewHashArray = np.empty((self.Hash_CurrentHashSize, self.Hash_CurrentHashSize), dtype=object)
        for i in range(len(self.HashArray)):
            for j in range(len(self.HashArray)):
                NewHashArray[2 * i, 2 * j] = self.HashArray[i, j]
                NewHashArray[2 * i, 2 * j + 1] = self.HashArray[i, j]
                NewHashArray[2 * i + 1, 2 * j] = self.HashArray[i, j]
                NewHashArray[2 * i + 1, 2 * j + 1] = self.HashArray[i, j]
        self.Hash_MaxPointsInHash = self.Hash_R * self.Hash_R * self.Hash_CurrentHashSize
        self.HashArray = NewHashArray

    def Show(self):
        for pos, Triangle in enumerate(self.TriangleList):
            print('Draw ', pos)
            COORDX0, COORDY0 = Triangle.NODES[0]
            COORDX1, COORDY1 = Triangle.NODES[1]
            COORDX2, COORDY2 = Triangle.NODES[2]
            self.CANVAS.create_line(COORDX0, TrueY(COORDY0), COORDX1, TrueY(COORDY1), fill='blue')
            self.CANVAS.create_line(COORDX1, TrueY(COORDY1), COORDX2, TrueY(COORDY2), fill='blue')
            self.CANVAS.create_line(COORDX2, TrueY(COORDY2), COORDX0, TrueY(COORDY0), fill='blue')


class CanvasFrame(tkinter.Canvas):
    def __init__(self, PARENTWINDOW):
        tkinter.Canvas.__init__(self, master=PARENTWINDOW, background='white', width=_WINDOW_SIZE[0], height=_WINDOW_SIZE[1])

        self.ParentFrame = PARENTWINDOW

        # Describe Active Buttons
        self.bind("<Button-1>", self.MouseLeftClick)
        self.bind("<Button-2>", self.PlusZoom)
        self.bind("<Button-3>", self.MinusZoom)

    def MouseLeftClick(self, event):
        x = float(self.canvasy(event.x)) + random.random()
        y = float(self.canvasy(event.y)) + random.random()
        y = math.fabs(_WINDOW_SIZE[1] - y)

        self.ParentFrame.NodeList.append([x, y])
        self.create_oval(x - 1, _WINDOW_SIZE[1] - y - 1, x + 1, _WINDOW_SIZE[1] - y + 1, outline="black", fill="black")

    def PlusZoom(self, event):
        self.scale("all", event.x, event.y, 1.1, 1.1)
        self.configure(scrollregion=self.bbox("all"))

    def MinusZoom(self, event):
        self.scale("all", event.x, event.y, 0.9, 0.9)
        self.configure(scrollregion=self.bbox("all"))


class MainWindow(tkinter.Frame):
    def __init__(self, PARENTFRAME):
        tkinter.Frame.__init__(self, master=PARENTFRAME)
        self.TK = PARENTFRAME

        # Create MenuBar for Window
        MenuBar = tkinter.Menu(PARENTFRAME)
        PARENTFRAME.config(menu=MenuBar)
        SubMenu = tkinter.Menu(MenuBar)
        MenuBar.add_cascade(label='Commands', menu=SubMenu)
        SubMenu.add_command(label='Start', command=lambda: self.Begin())
        SubMenu.add_command(label='10', command=lambda: self.DrawPoints(NUMBER=10))
        SubMenu.add_command(label='100', command=lambda: self.DrawPoints(NUMBER=100))
        SubMenu.add_command(label='1000', command=lambda: self.DrawPoints(NUMBER=1000))
        SubMenu.add_command(label='10000', command=lambda: self.DrawPoints(NUMBER=10000))
        SubMenu.add_command(label='100000', command=lambda: self.DrawPoints(NUMBER=100000))
        SubMenu.add_command(label='1000000', command=lambda: self.DrawPoints(NUMBER=1000000))

        # Create Canvas Frame on Window
        self.CanvasWidget = CanvasFrame(PARENTWINDOW=self)
        self.CanvasWidget.pack(side=tkinter.LEFT)

        # Describe Structure For Nodes
        self.NodeList = []

    def Begin(self):
        DelaunayMethod(NODELIST=self.NodeList, CANVAS=self.CanvasWidget).Start()
        print('END MAIN WINDOW')

    def DrawPoints(self, NUMBER):
        for i in range(NUMBER):
            COORDX = random.uniform(5, _WINDOW_SIZE[0] - 5)
            COORDY = random.uniform(5, _WINDOW_SIZE[1] - 5)
            self.NodeList.append([COORDX, COORDY])
            self.CanvasWidget.create_oval(COORDX - 1, TrueY(COORDY) - 1, COORDX + 1, TrueY(COORDY) + 1, fill='black')


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Delaunay Triangulation Python 3.5")

    MainWindow(PARENTFRAME=root).pack()

    root.resizable(height=False, width=False)
    root.mainloop()
