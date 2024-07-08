import time
from collections import defaultdict


class UtilityList:
    def __init__(self, item):
        self.item = item
        self.elements = []
        self.sumIutils = 0
        self.sumRutils = 0

    def addElement(self, element):
        self.elements.append(element)
        self.sumIutils += element.iutils
        self.sumRutils += element.rutils


class Element:
    def __init__(self, tid, iutils, rutils):
        self.tid = tid
        self.iutils = iutils
        self.rutils = rutils


class HUIMiner:
    def __init__(self):
        self.startTimestamp = 0
        self.endTimestamp = 0
        self.huiCount = 0
        self.mapItemToTWU = {}
        self.joinCount = 0
        self.cmp = 0
        self.BUFFERS_SIZE = 200
        self.itemsetBuffer = [0] * self.BUFFERS_SIZE

    def runAlgorithm(self, input, output, minUtility):
        self.startTimestamp = time.time()
        self.mapItemToTWU = defaultdict(int)

        # First database scan to calculate TWU of each item
        with open(input, 'r') as file:
            for line in file:
                if line.startswith('#') or line.startswith('%') or line.startswith('@') or not line.strip():
                    continue

                items, transactionUtility = line.strip().split(':')
                items = list(map(int, items.split()))
                transactionUtility = int(transactionUtility)
                
                for item in items:
                    self.mapItemToTWU[item] += transactionUtility

        listOfUtilityLists = []
        mapItemToUtilityList = {}

        for item, twu in self.mapItemToTWU.items():
            if twu >= minUtility:
                uList = UtilityList(item)
                mapItemToUtilityList[item] = uList
                listOfUtilityLists.append(uList)

        listOfUtilityLists.sort(key=lambda ul: ul.item)

        tid = 0
        with open(input, 'r') as file:
            for line in file:
                if line.startswith('#') or line.startswith('%') or line.startswith('@') or not line.strip():
                    continue

                parts = line.strip().split(':')
                items = list(map(int, parts[0].split()))
                utilities = list(map(int, parts[2].split()))
                remainingUtility = 0
                revisedTransaction = []

                for item, utility in zip(items, utilities):
                    if self.mapItemToTWU[item] >= minUtility:
                        revisedTransaction.append((item, utility))
                        remainingUtility += utility

                revisedTransaction.sort(key=lambda x: x[0])

                for item, utility in revisedTransaction:
                    remainingUtility -= utility
                    utilityListOfItem = mapItemToUtilityList[item]
                    element = Element(tid, utility, remainingUtility)
                    utilityListOfItem.addElement(element)
                
                tid += 1

        with open(output, 'w') as self.writer:
            self.huiMiner(self.itemsetBuffer, 0, None, listOfUtilityLists, minUtility)

        self.endTimestamp = time.time()
        self.printStats()

    def compareItems(self, item1, item2):
        return (self.mapItemToTWU[item1] - self.mapItemToTWU[item2]) or (item1 - item2)

    def huiMiner(self, prefix, prefixLength, pUL, ULs, minUtility):
        for i, X in enumerate(ULs):
            if X.sumIutils >= minUtility:
                self.writeOut(prefix, prefixLength, X.item, X.sumIutils)

            if X.sumIutils + X.sumRutils >= minUtility:
                exULs = [self.construct(pUL, X, ULs[j]) for j in range(i + 1, len(ULs))]
                self.joinCount += len(exULs)
                self.itemsetBuffer[prefixLength] = X.item
                self.huiMiner(self.itemsetBuffer, prefixLength + 1, X, exULs, minUtility)

    def construct(self, P, px, py):
        pxyUL = UtilityList(py.item)
        for ex in px.elements:
            ey = self.findElementWithTID(py, ex.tid)
            if not ey:
                continue

            if not P:
                eXY = Element(ex.tid, ex.iutils + ey.iutils, ey.rutils)
                pxyUL.addElement(eXY)
            else:
                e = self.findElementWithTID(P, ex.tid)
                if e:
                    eXY = Element(ex.tid, ex.iutils + ey.iutils - e.iutils, ey.rutils)
                    pxyUL.addElement(eXY)
        return pxyUL

    def findElementWithTID(self, ulist, tid):
        first, last = 0, len(ulist.elements) - 1

        while first <= last:
            self.cmp += 1
            middle = (first + last) // 2
            if ulist.elements[middle].tid < tid:
                first = middle + 1
            elif ulist.elements[middle].tid > tid:
                last = middle - 1
            else:
                return ulist.elements[middle]
        return None

    def writeOut(self, prefix, prefixLength, item, utility):
        self.huiCount += 1
        self.writer.write(f"{' '.join(map(str, prefix[:prefixLength]))} {item} #UTIL: {utility}\n")

    def printStats(self):
        print("=============  HUI-MINER ALGORITHM - STATS =============")
        print(f" Total time ~ {(self.endTimestamp - self.startTimestamp) * 1000:.2f} ms")
        print(f" High-utility itemsets count : {self.huiCount}")
        print(f" Join count : {self.joinCount}")
        print(f" Number of comparisons = {self.cmp}")
        print("===================================================")


if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"
    min_utility = 30

    miner = HUIMiner()
    miner.runAlgorithm(input_file, output_file, min_utility)
