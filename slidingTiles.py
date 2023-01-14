import random
from datetime import datetime, timedelta
from time import sleep
from os.path import exists

def liscpy(inputList, outputList):
    inpLen = len(inputList)
    outputList = [0] * inpLen
    for i in range(0, inpLen):
        outputList[i] = inputList[i]
    return outputList


def listtostr(lis):
    rsltstr = ""
    for i in lis:
        rsltstr += str(i)
    return rsltstr


class board:
    def __init__(self):
        self.OGboard = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.board_list = {}
        self.board_list_len = 0
        self.plays_to_make = []
        self.movementList = [-3, 1, 3, -1]
        self.eval(self.OGboard, -1, 0)

    def eval(self, b, lastPlay, totalSeq):
        if self.hash(b, lastPlay, totalSeq):
            moves, zeroi = self.getMoves(b)
            for m in moves:
                appendableboard = []
                appendableboard = liscpy(b, appendableboard)
                self.plays_to_make.append((appendableboard, m, zeroi, self.board_list_len,totalSeq))
            self.board_list_len += 1

    def player(self):
        start = datetime.now()
        lastStateLen = self.board_list_len
        lastQueueLen = len(self.plays_to_make)
        staterate = 0
        queuerate = 0
        while self.plays_to_make:
            if (datetime.now() - start) >= timedelta(seconds=1):
                newStateLen = self.board_list_len
                newQueueLen = len(self.plays_to_make)
                staterate = newStateLen - lastStateLen
                queuerate = newQueueLen - lastQueueLen
                lastQueueLen = newQueueLen
                lastStateLen = newStateLen
                start = datetime.now()
            b, m, zeroi,lastPlay,totalSeq = self.plays_to_make[0]
            # print(b)
            self.plays_to_make = self.plays_to_make[1:]
            movedBoard, zeroin = self.switch(b, m, zeroi)
            self.eval(movedBoard, lastPlay, totalSeq +1)
            strText = f"Board State Count: {self.board_list_len} Queue Counter: {len(self.plays_to_make)} "
            strText2 = f"{self.board_list_len}/181440"
            strTextLen = len(strText)
            strText += str(movedBoard[0:3])
            strText += '\n' + strText2 + " " * (strTextLen - len(strText2)) + str(movedBoard[3:6])
            if queuerate == 0:
                queuerate = 1
            strText += '\n' + " " * strTextLen + str(movedBoard[
                                                     6:9]) + f"\n (states|queue)/sec: ({staterate}|{queuerate})   r:{staterate / queuerate}  0i:{zeroi}\n\n\n"
            print(strText.replace(',', ''))

    def hash(self, b, lastStep, totalSeq):
        key = listtostr(b)
        if key in self.board_list:
            if self.board_list[key][1] > totalSeq:
                self.board_list[key] = [lastStep, totalSeq]
                return True
            return False  # if hashstr in self.board_list:
        self.board_list[listtostr(b)] = [lastStep, totalSeq]
        return True

    def switch(self, b, move, zeroIndex):
        movedBoard = []
        movedBoard = liscpy(b, movedBoard)
        temp = movedBoard[zeroIndex]
        movedBoard[zeroIndex] = movedBoard[zeroIndex + move]
        movedBoard[zeroIndex + move] = temp
        return movedBoard, zeroIndex + move

    def getMoves(self, board):
        # self.movementList = [-3,1,3,-1]
        zeroIndex = board.index(0)
        zeroIndexModThree = zeroIndex % 3
        movesToMake = []

        if zeroIndex < 3:
            # top row
            movesToMake.append(self.movementList[2])
        elif zeroIndex > 5:
            # bottom row
            movesToMake.append(self.movementList[0])
        else:
            movesToMake.append(self.movementList[0])
            movesToMake.append(self.movementList[2])
            # middle row
        if zeroIndexModThree == 0:
            movesToMake.append(self.movementList[1])
            # left Column
        elif zeroIndexModThree == 1:
            movesToMake.append(self.movementList[1])
            movesToMake.append(self.movementList[3])
            # middleColumn
        else:
            movesToMake.append(self.movementList[3])
        return movesToMake, zeroIndex
        # right Column

if exists("./SlidingTilesData.txt"):
    stFile = open("./SlidingTilesData.txt", 'r')
    stTxt = stFile.read()
    stFile.close()
    stDict = eval(stTxt)
    stDictLen = len(stDict)
else:
    brd = board()
    brd.player()
    stDict = brd.board_list
    stDictLen = brd.board_list_len
    f = open("./SlidingTilesData.txt", 'w')
    f.write(str(brd.board_list))
    f.close()

def getItemByIndex(n=0):
    if n < 0:
        n += stDictLen
    for i, key in enumerate(stDict.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")


def craftBrdDisp(strArr, b, lastBoard=False):
    if not strArr:
        strArr = ["", "", "", "", ""]
    board = ""
    blen = len(b)
    for i in range(0, blen):
        board += b[i]
        if (i + 1) % 3 != 0:
            board += " "
    strArr[0] += " _____ "
    strArr[1] += "[" + board[0:5] + "]"
    strArr[2] += "[" + board[5:10] + "]"
    strArr[3] += "[" + board[10:15] + "]"
    strArr[4] += " ‾‾‾‾‾ "
    if not lastBoard:
        strArr[0] += "    "
        strArr[1] += "    "
        strArr[2] += " -> "
        strArr[3] += "    "
        strArr[4] += "    "
    if len(strArr[0]) > 100 and not lastBoard:
        printBrdDisp(strArr)
        strArr = ["", "", "", "", ""]
    return strArr


def printBrdDisp(strArr):
    for s in strArr:
        print(s.replace('0', ' '))


def getBoardSequence(tbk):
    sequenceLen = 0
    if tbk in stDict:
        firstIndex = stDict[tbk][0]
        indexList = [(firstIndex, tbk)]
        index = firstIndex
        while index >= 0:
            key = getItemByIndex(index)
            indexList.append((index, key))
            index = stDict[key][0]
        #indexList = list(reversed(indexList))
        strArr = []
        for i in range(0, len(indexList) - 1):
            strArr = craftBrdDisp(strArr, indexList[i][1])
        strArr = craftBrdDisp(strArr, indexList[len(indexList) - 1][1], True)
        printBrdDisp(strArr)
        sequenceLen = len(indexList)
    else:
        print("board state not possible")
    return sequenceLen


def getLargestSequence():
    largestSequence = 0
    largestSequenceKey = None
    sameLengthBoards = []
    count = -1
    for k in stDict:
        count += 1
        # if k[8] == '0':
        print(str(count / stDictLen)[2:4] + "% finished")
        seqLen = stDict[k][1]
        if seqLen > largestSequence:
            largestSequence = seqLen
            largestSequenceKey = k
            sameLengthBoards.clear()
        if seqLen == largestSequence and len(sameLengthBoards) < 11:
            sameLengthBoards.append(k)
    print("Hardest Board(s) to get to")
    strArr = []
    strArr = craftBrdDisp(strArr, largestSequenceKey, True)
    for k in sameLengthBoards:
        strArr = craftBrdDisp(strArr, k, True)
    printBrdDisp(strArr)
    print("with a sequence length of", largestSequence)
    print("board state can be reached by")
    getBoardSequence(largestSequenceKey)


print("Enter board to query, r for random board, l for largest sequence, or e to exit\nuse 0 to represent the empty/blank tile")
tbk = input(":")
index = 0
while tbk != 'e':
    if tbk == 'l':
        getLargestSequence()
    elif tbk == 'r':
        tbk = getItemByIndex(random.randint(0, len(stDict)))
    getBoardSequence(tbk)
    tbk = input(":")
