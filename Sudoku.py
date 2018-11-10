# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 15:51:31 2018

@author: joergwilczynski

http://hodoku.sourceforge.net/en/techniques.php
"""


import sys
import os
from copy import deepcopy
import traceback 
import itertools    

# trace switches 
TRACE = False    
CHECKCELL = False
HIDDENSINGLES = False
NAKEDSINGLES = False
NAKEDPAIRS = False  
LOCKEDCANDIDATES1 = False
LOCKEDCANDIDATES2 = False
HIDDENPAIRS = False
NAKEDTRIPLES = False
NAKEDQUADRUPLES = False
HIDDENTRIPLES = False
HIDDENQUADRUPLES = False
XWING = False
SWORDFISH = False
XYWING = False
JELLYFISH = False
    

def initBoard(readInput, solveSudokuNo, fileName):
    """ The Sudoku board is modelled as a list of 9 rows.
        Each row contains entries for 9 cells.
        A cell entry is 
        - either an integer value (1-9) if the cell has been assigned a fixed value.
        - or a list of potential candidates for a cell 
    """

    Board = []    

    if readInput:
        # read initial Board from stdin
        
        print()
        print('Please enter your Sudoku')
        print('   enter 9 digits per row - use 0 for cells not set')
        print('   separators between digits are not required')
    
        for r in range(9):
            print('  row {}:'.format(r+1) )
            row = sys.stdin.readline()
            newRow=[]
            newRow.extend(row)
            row = []
            for i in range(min(len(newRow),9)):
                try:
                    n = int(newRow[i])
                except ValueError as e:
                    # ignore non-integer input
                    pass
                else:
                    row.append(n)
                
            while len(row) < 9:
                row.append(0)
            
            Board.append(row)           
                
    elif fileName != '':
        # read initial Board from file
                
        with open(fileName, 'r') as fin:
            
            rows = 0
            for line in fin:
                
                if rows > 8:
                    break
                
                if line[0] == '#':
                    # that's a comment line
                    print(line,end='')
                    continue
                
                rows += 1
                newRow=[]
                newRow.extend(line)
                row = []
                for i in range(min(len(newRow),9)):
                    try:
                        n = int(newRow[i])
                    except ValueError as e:
                        # ignore non-integer input
                        pass
                    else:
                        row.append(n)
                    
                while len(row) < 9:
                    row.append(0)
                
                Board.append(row)  
                
    else:
        # define initial Board
        
        emptyRow = [0,0,0,0,0,0,0,0,0]
        for r in range(9):
            Board.append(deepcopy(emptyRow))      

        if solveSudokuNo == 1:

            # 'Colors' + 'XY-Wing'
            Board[0] = [2,0,0,3,0,0,7,5,0]
            Board[1] = [0,0,5,0,0,1,0,0,9]
            Board[2] = [0,0,0,7,0,0,0,0,1]
            Board[3] = [0,0,0,8,3,0,0,1,7]
            Board[4] = [3,0,0,1,0,7,0,0,2] 
            Board[5] = [7,2,0,0,6,5,0,0,0]           
            Board[6] = [1,0,0,0,0,4,0,0,0]            
            Board[7] = [5,0,0,2,0,0,4,0,0]
            Board[8] = [0,9,6,0,0,3,0,0,8]
            
        elif solveSudokuNo == 2: 
                
            # 'XY-Wing' 
            Board[0] = [0,5,9,0,3,7,0,0,0]        
            Board[1] = [0,0,0,0,0,0,0,0,3]              
            Board[2] = [0,0,2,0,8,0,9,7,5]
            Board[3] = [0,2,0,0,0,8,0,0,0]
            Board[4] = [5,4,0,0,0,0,0,3,9]    
            Board[5] = [0,0,0,1,0,0,0,8,0]    
            Board[6] = [6,1,7,0,4,0,3,0,0]    
            Board[7] = [3,0,0,0,0,0,0,0,0]    
            Board[8] = [0,0,0,9,6,0,5,1,0]     

        elif solveSudokuNo == 3:
        
            # brute force after all        
            Board[0] = [6,0,0,7,0,0,0,0,0]
            Board[1] = [0,9,0,0,6,0,7,0,0]
            Board[2] = [0,5,0,0,0,2,0,0,0]
            Board[3] = [0,0,0,1,0,0,6,0,8]
            Board[4] = [4,0,8,0,2,0,9,0,5] 
            Board[5] = [2,0,3,0,0,5,0,0,0]
            Board[6] = [0,0,0,3,0,0,0,1,0]  
            Board[7] = [0,0,2,0,1,0,0,7,0]
            Board[8] = [0,0,0,0,0,4,0,0,9]

            
        elif solveSudokuNo == 4:
        
            # 'Colors'        
            Board[0] = [0,0,0,0,0,0,0,0,8]
            Board[1] = [4,0,0,7,0,0,0,9,0]
            Board[2] = [0,5,0,3,0,1,0,0,0]
            Board[3] = [0,1,0,0,0,5,9,0,0]
            Board[4] = [0,0,6,0,2,0,3,0,0] 
            Board[5] = [0,0,7,9,0,0,0,6,0]
            Board[6] = [0,0,0,1,0,3,0,7,0]
            Board[7] = [0,6,0,0,0,2,0,0,1]
            Board[8] = [3,0,0,0,0,0,0,0,0] 

        elif solveSudokuNo == 5:
            
            # brute force after all        
            Board[0] = [3,0,0,0,0,1,2,0,0]
            Board[1] = [0,6,0,0,0,0,0,1,0]
            Board[2] = [0,0,0,9,0,2,0,3,0]
            Board[3] = [0,0,9,0,7,0,0,4,0]
            Board[4] = [4,0,0,0,2,0,0,0,7] 
            Board[5] = [0,3,0,0,8,0,5,0,0]
            Board[6] = [0,9,0,7,0,6,0,0,0]
            Board[7] = [0,1,0,0,0,0,0,6,0]
            Board[8] = [0,0,5,3,0,0,0,0,4] 
                        
        elif solveSudokuNo == 6:
            
            # 'XY-Wing'   
            Board[0] = [7,3,0,0,0,0,0,0,0]
            Board[1] = [8,0,1,0,7,0,5,0,0]
            Board[2] = [0,9,6,0,5,0,0,0,0]
            Board[3] = [0,0,4,0,0,9,0,6,0]
            Board[4] = [0,0,0,2,6,7,0,0,0] 
            Board[5] = [0,7,0,5,0,0,2,0,0]
            Board[6] = [0,0,0,0,4,0,7,1,0]
            Board[7] = [0,0,9,0,1,0,6,0,5]
            Board[8] = [0,0,0,0,0,0,0,4,8]   
                         
        else: 
            exceptionText = 'Invalid Sudoku number entered: {}'.format(solveSudokuNo)
            raise(ValueError(exceptionText))
          

    #check the input
    loop = True    
    while loop:
    
        print()
        printTestBoard(Board,'Initial Board:', 0)
        print() 
           
    
        # check symmetry of input
        asymmetricBoard = False
        invalidCellValue = False
        exceptionText = ''
        for r in range(9):
            for c in range(9):
                if Board[r][c] != 0 and Board[8-r][8-c] == 0:
                    exceptionText = 'The initial Board is not set up symmetrically, see cells ({},{}) and ({},{})'.format(r,c,8-r,8-c)
                    asymmetricBoard = True
                    break
                if Board[r][c] not in range(10):
                    exceptionText = 'Invalid cell value {} at ({},{})'.format(Board[r][c],r,c)                
                    invalidCellValue = True
                    break
                    
            if  asymmetricBoard or invalidCellValue:
                break
                
        if asymmetricBoard:
            print(exceptionText)
            print('Do you want to reenter a row (r), abort (a), or try to solve the Sudoku anyhow (s)?')
            answer = sys.stdin.readline()
                        
            if answer[0] == 'a':
                raise AsymmetricBoardException(exceptionText)
            elif answer[0] == 's':
                loop = False
            else:
                while True:
                    print('Please enter a row number (1-9):')
                    n = sys.stdin.readline()
                    try:
                        nRow = int(n[0])
                    except ValueError as e:
                        # retry
                        pass
                    else:
                        # got a valid row number
                        print('  row {}:'.format(nRow) )
                        row = sys.stdin.readline()
                        newRow=[]
                        newRow.extend(row)
                        row = []
                        for i in range(min(len(newRow),9)):
                            try:
                                n = int(newRow[i])
                            except ValueError as e:
                                # ignore non-integer input
                                pass
                            else:
                                row.append(n)
                            
                        while len(row) < 9:
                            row.append(0)
                            
                        Board[nRow-1] = deepcopy(row) 
                        break
                        
        elif invalidCellValue:
            print(exceptionText)
            print('Do you want to reenter a row (r) or abort the Sudoku (a)?')
            answer = sys.stdin.readline()
            if answer[0] == 'a':
                raise ValueError(exceptionText)            
            else:
                while True:
                    print('Please enter a row number (1-9):')
                    n = sys.stdin.readline()
                    try:
                        nRow = int(n[0])
                    except ValueError as e:
                        # retry
                        pass
                    else:
                        # got a valid row number
                        print('  row {}:'.format(n) )
                        row = sys.stdin.readline()
                        newRow=[]
                        newRow.extend(row)
                        row = []
                        for i in range(min(len(newRow),9)):
                            try:
                                n = int(newRow[i])
                            except ValueError as e:
                                # ignore non-integer input
                                pass
                            else:
                                row.append(n)
                            
                        while len(row) < 9:
                            row.append(0)
                        
                        Board[nRow-1] = deepcopy(row)  
                        break
                    
        else:
            # input seems to be okay
            loop = False


    # inserting list of candidates instead of invalid cell value '0'
    initialCandidates = list(range(1,10))
    
    for r in range(9):
        for c in range(9):
            if type(Board[r][c]) is int and Board[r][c] == 0:
                Board[r][c] = deepcopy(initialCandidates)

                
    return Board
    


def removeInvalidCandidates(Board):
    """ Run a check over 3x3-blocks, rows and columns  
        and remove invalid candidates
    """
    
    # check 3x3 blocks
    for r in range(0,3):
        startRow = r * 3        
        for c in range(0,3):
            startCol = c * 3 
            Board = checkBlock(startRow, startCol, Board)
    
    # check rows
    for r in range(9):
        Board = checkRow(r, Board)
    
    # check columns
    for c in range(9):
        Board = checkColumn(c, Board) 
        
    return Board



def checkBlock(startRow, startCol, Board):
    """ check if a cell contains an integer value
        and remove from candidate list if appropriate
    """
    
    endRow = startRow + 3
    endCol = startCol + 3   
    
    for r in range(startRow, endRow):
        for c in range(startCol, endCol):
            cellValue = Board[r][c]
            if type(cellValue) is int:
                for rx in range(startRow, endRow):
                    for cx in range(startCol, endCol):
                        if type(Board[rx][cx]) is list:
                            try:
                                old = deepcopy(Board[rx][cx])
                                Board[rx][cx].remove(cellValue)
                                if CHECKCELL:
                                    print('     checkBlock: ({},{}): {} -> {}'.format(rx,cx,old, Board[rx][cx]))
                            except ValueError as e:
                                # that is ok
                                pass

                            if len(Board[rx][cx]) == 0:                               
                                exceptionText = 'Invalid Board: empty cell at ({},{})'.format(rx,cx)
                                raise EmptyCellException(exceptionText) 

                        elif c != cx and Board[rx][cx] == cellValue:
                            exceptionText = '{} is not unique in block, see cells ({},{}) and ({},{})'.format(cellValue,r,c,rx,cx )
                            raise NonUniqueValueException(exceptionText)
                                                    
    return Board



def checkRow(row, Board):
    """ check if a cell contains an integer value
        and remove from candidate list if appropriate
    """ 
    
    for c in range(9):
        cellValue = Board[row][c]
        if type(cellValue) is int:
            for cx in range(9):
                if type(Board[row][cx]) is list:
                    try:
                        old = deepcopy(Board[row][cx])
                        Board[row][cx].remove(cellValue)
                        if CHECKCELL:
                            print('     checkRow: ({},{}): {} -> {}'.format(row,cx,old, Board[row][cx]))
                    except ValueError as e:
                        # that is ok
                        pass
                    
                    if len(Board[row][cx]) == 0:                       
                        exceptionText = 'Invalid Board: empty cell at ({},{})'.format(row,cx)
                        raise EmptyCellException(exceptionText)
                elif c != cx and Board[row][cx] == cellValue:
                    exceptionText = '{} is not unique in row {}, see cells ({},{}) and ({},{})'.format(cellValue, row,row,c,row,cx )
                    raise NonUniqueValueException(exceptionText) 
                                                    
    return Board                        



def checkColumn(column, Board):
    """ check if a cell contains an integer value
        and remove from candidate list if appropriate
    """ 
    
    for r in range(9):
        cellValue = Board[r][column]
        if type(cellValue) is int:
            for rx in range(9):
                if type(Board[rx][column]) is list:
                    try:
                        old = deepcopy(Board[rx][column])
                        Board[rx][column].remove(cellValue)
                        if CHECKCELL:
                            print('     checkColumn: ({},{}): {} -> {}'.format(rx,column,old, Board[rx][column]))                            
                    except ValueError as e:
                        # that is ok
                        pass
                    
                    if len(Board[rx][column]) == 0:
                        exceptionText = 'Invalid Board: empty cell at ({},{})'.format(rx,column)
                        raise EmptyCellException(exceptionText)     
                elif r != rx and Board[rx][column] == cellValue:
                    exceptionText = '{} is not unique in column {}, see cells ({},{}) and ({},{})'.format(cellValue, column,r,column,rx,column )
                    raise NonUniqueValueException(exceptionText)                                                                     
    return Board



def findNakedSingles(Board):
    """ check for cells with a single candidate
    """

    checking = True    

    while checking:
        foundSingleCandidate = False        
        for r in range(9):
            for c in range(9):
                if type(Board[r][c]) is list and len(Board[r][c]) == 1:
                    Board[r][c] = Board[r][c][0]
                    if NAKEDSINGLES:
                        print('     NakedSingles: ({},{}) -> {}'.format(r,c,Board[r][c]))                    
                    Board = removeInvalidCandidates(Board)
                    foundSingleCandidate = True  
        # stop the loop if no candidate was found in the previous iteration            
        if not foundSingleCandidate:
            checking = False            

    return Board
    

    
def validateBoard(Board):
    """ check if the board is valid
    """

    retCode = 'INVALID'   
    count = 0
        
    for r in range(9):
        for c in range(9):
            if type(Board[r][c]) is list and Board[r][c] == []:
                retCode = 'INVALID'
                exceptionText = 'Invalid Board: empty cell at ({},{})'.format(r,c)
                raise EmptyCellException(exceptionText) 
            elif type(Board[r][c]) is int:
                count += 1
                retCode = 'VALID' 
                
    if retCode == 'VALID' and count == 81:
        retCode = 'SOLVED'
    
    return retCode
    
    

def findHiddenSingles(Board):
    """ Run an check over 3x3-blocks, rows and columns  
        and find Hidden Singles
    """

    # check 3x3 blocks             
    Board = findHiddenSinglesInBlocks(Board)

    # check rows
    Board = findHiddenSinglesInRows(Board,'Rows')

    # check columns
    Board = findHiddenSinglesInColumns(Board)

        
    return Board



def findHiddenSinglesInBlocks(Board):
    """ check if 3x3-blocks contain Hidden Singles
    """

    for r in range(0,3):
        startRow = r * 3   
        endRow = startRow + 3
       
        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3 
        
            hiddenSingle = True 
            
            while hiddenSingle: 
                noList = True      
                for r in range(startRow, endRow):
                    for c in range(startCol, endCol):
                        if type(Board[r][c]) is list:
                            noList = False
                            for candidate in Board[r][c]:
                                hiddenSingle = True                
                            
                                breakOut = False
                                for rx in range(startRow, endRow):
                                    for cx in range(startCol, endCol):
                                        if rx == r and cx == c:
                                            pass
                                        elif type(Board[rx][cx]) is list and candidate in Board[rx][cx]:
                                            # candidate is not a Hidden Single
                                            hiddenSingle = False
                                            breakOut = True
                                            break   
                                    if breakOut:
                                        break
                               
                                if hiddenSingle:
                                    old = deepcopy(Board[r][c])
                                    Board[r][c] = candidate
                                    if HIDDENSINGLES:
                                        print('     HiddenSinglesInBlocks: ({},{}): {} -> {}'.format(r,c,old,Board[r][c]))                                    
                                    Board = removeInvalidCandidates(Board)
            
                if noList:
                    hiddenSingle = False   
                           
    return Board



def findHiddenSinglesInColumns(Board):
    """ check if columns contain Hidden Singles
    """ 

    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findHiddenSinglesInRows(TransposedBoard, 'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)  
                                                                 
    return Board



def findHiddenSinglesInRows(Board, traceString):
    """ check if rows contain Hidden Singles
    """ 

    for row in range(9):
        
        hiddenSingle = True 
        
        while hiddenSingle:
            noList = True
            for c in range(9):
                if type(Board[row][c]) is list:
                    noList = False
                    for candidate in Board[row][c]:
                        hiddenSingle = True
                        for cx in range(9):
                            if cx == c:
                                pass
                            elif type(Board[row][cx]) is list and candidate in Board[row][cx]:
                                # candidate is not a Hidden Single
                                hiddenSingle = False
                                break
                            
                        if hiddenSingle:
                            old = deepcopy(Board[row][c])
                            Board[row][c] = candidate
                            if HIDDENSINGLES:
                                print('     HiddenSinglesIn{}: ({},{}): {} -> {}'.format(traceString,row,c,old,Board[row][c]))                                                                
                            Board = removeInvalidCandidates(Board)
        
            if noList:
                hiddenSingle = False 
                                                               
    return Board



def findNakedPairs(Board):
    """ Run an check over 3x3-blocks, rows and columns  
        and find Naked Pairs
    """    
    
    # check 3x3 blocks
    Board = findNakedPairsInBlocks(Board)

    # check rows
    Board = findNakedPairsInRows(Board, 'Rows')

    # check columns
    Board = findNakedPairsInColumns(Board)

                   
    return Board



def findNakedPairsInBlocks(Board):
    """ check if 3x3-blocks contain Naked Pairs
    """   
    
    for r in range(0,3):
        startRow = r * 3 
        endRow = startRow + 3
       
        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3 
        
            nakedPair = True
            pairsToSkip = []
            
            while nakedPair: 
                r1 = r2 = c1 = c2 = 0
                nakedPair = False
                breakOut = False
                for r in range(startRow, endRow):
                    for c in range(startCol, endCol):
                        if type(Board[r][c]) is list and len(Board[r][c]) == 2:
                            pair = Board[r][c] 

                            if pair not in pairsToSkip:
                                pairsToSkip.append(pair)
                                r1 = r; c1 = c
                            
                                for rx in range(startRow, endRow):
                                    for cx in range(startCol, endCol):
                                        if rx == r and cx == c:
                                            pass
                                        elif type(Board[rx][cx]) is list and pair == Board[rx][cx]:
                                            # a matching naked pair was found
                                            nakedPair = True
                                            r2 = rx; c2 = cx
                                            breakOut = True
                                            break   
                                    if breakOut:
                                        break
                                if breakOut:
                                    break                           
                    if breakOut:
                        break
                    
                breakOut = False
                
                if nakedPair:
                    # remove candidates of naked pair from other lists of candidates
                    for r in range(startRow, endRow):
                        for c in range(startCol, endCol):                    
                            if (r == r1 and c == c1) or (r == r2 and c == c2):
                                pass
                            elif type(Board[r][c]) is list:
                                if pair[0] in Board[r][c]:
                                    old = deepcopy(Board[r][c])
                                    Board[r][c].remove(pair[0])
                                    if NAKEDPAIRS:
                                        print('     NakedPairsInBlocks: ({},{}): {} -> {}'.format(r,c,old,Board[r][c]))                                   
                                if pair[1] in Board[r][c]:
                                    old = deepcopy(Board[r][c])
                                    Board[r][c].remove(pair[1])
                                    if NAKEDPAIRS:
                                        print('     NakedPairsInBlocks: ({},{}): {} -> {}'.format(r,c,old,Board[r][c]))                                   

                                    
    return Board



def findNakedPairsInColumns(Board):
    """ check if columns contain Naked Pairs
    """
    
    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findNakedPairsInRows(TransposedBoard,'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)                                                                   
                                    
    return Board



def findNakedPairsInRows(Board,traceString):
    """ check if rows contain Naked Pairs
    """
        
    for r in range(9):
    
        nakedPair = True
        pairsToSkip = []
        
        while nakedPair: 
            c1 = c2 = 0
            nakedPair = False
            breakOut = False
            for c in range(9):
                if type(Board[r][c]) is list and len(Board[r][c]) == 2:
                    pair = Board[r][c] 

                    if pair not in pairsToSkip:
                        pairsToSkip.append(pair)
                        c1 = c
                    
                        for cx in range(9):
                            if cx == c:
                                pass
                            elif type(Board[r][cx]) is list and pair == Board[r][cx]:
                                # a matching naked pair was found
                                nakedPair = True
                                c2 = cx
                                breakOut = True
                                break                              
                if breakOut:
                    break
                
            breakOut = False
            
            if nakedPair:
                # remove candidates of naked pair from other lists of candidates
                for c in range(9):                    
                    if (c == c1) or (c == c2):
                        pass
                    elif type(Board[r][c]) is list:
                        if pair[0] in Board[r][c]:
                            old = deepcopy(Board[r][c])
                            Board[r][c].remove(pair[0])
                            if NAKEDPAIRS:
                                print('     NakedPairsIn{}: ({},{}): {} -> {}'.format(traceString,r,c,old,Board[r][c]))                                                                  
                        if pair[1] in Board[r][c]:
                            old = deepcopy(Board[r][c])
                            Board[r][c].remove(pair[1])                                    
                            if NAKEDPAIRS:
                                 print('     NakedPairsIn{}: ({},{}): {} -> {}'.format(traceString,r,c,old,Board[r][c]))                                                                  
                                    
    return Board



def findHiddenPairs(Board):
    """ Run an check over 3x3-blocks, rows and columns  
        and find Hidden Pairs
    """    
    
    # check 3x3 blocks
    Board = findHiddenPairsInBlocks(Board)

    # check rows
    Board = findHiddenPairsInRows(Board,'Rows')

    # check columns
    Board = findHiddenPairsInColumns(Board)

                   
    return Board




def findHiddenPairsInBlocks(Board):
    """ check if 3x3-blocks contain Hidden Pairs
    """   

    for r in range(0,3):    
        startRow = r * 3 
        endRow = startRow + 3
       
        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3     

            pairsToSkip = []
            
            # iterate over block
            for rb in range(startRow, endRow):
                for cb in range(startCol, endCol):
                    
                    candidates = []
                    r1 = r2 = c1 = c2 = 0
                    # get potential pairs in cell rb,cb
                    if type(Board[rb][cb]) is list:
                        candidates.extend(Board[rb][cb])
                        
                        for p1 in range(len(candidates)):
                            for p2 in range(p1+1, len(candidates)):
                                # cell rb,cb contains pair p1,p2
                                r1 = rb; c1 = cb
                                foundSecondPair = False
                                breakout = False 
                                pair = [candidates[p1],candidates[p2]]
        
                                if pair not in pairsToSkip:
                                    pairsToSkip.append(pair)
                                
                                    for rx in range(startRow, endRow):
                                        for cx in range(startCol, endCol):                                    
                                                                           
                                            if rx == rb and cx == cb:
                                                continue
                                            if type(Board[rx][cx]) is list:
                                                if candidates[p1] in Board[rx][cx] and candidates[p2] in Board[rx][cx]:
                                                    # cell rx,cx contains pair candidates[p1],candidates[p2], too
                                                    
                                                    if foundSecondPair:
                                                        # one pair to many
                                                        foundSecondPair = False
                                                        breakout = True
                                                        break
                                                    else:
                                                        foundSecondPair = True
                                                        r2 = rx; c2 = cx                                                   
                                                elif candidates[p1] in Board[rx][cx] or candidates[p2] in Board[rx][cx]:
                                                    # no hidden pairs are possible anymore                                                
                                                    foundSecondPair = False
                                                    breakout = True 
                                                    break
                                                
                                        if breakout:
                                            break
                                            
                                if foundSecondPair:
                                    # there are two hidden (or two naked) pairs in this block
                                    # remove other candidates from this block
                                    old1 = deepcopy(Board[r1][c1])
                                    old2 = deepcopy(Board[r2][c2])                          
                                    Board[r1][c1] = [candidates[p1],candidates[p2]]
                                    Board[r2][c2] = [candidates[p1],candidates[p2]] 
                                    if HIDDENPAIRS:
                                        print('     HiddenPairsInBlocks: ({},{}): {} -> {} , ({},{}): {} -> {}'.format(r1,c1,old1,Board[r1][c1],r2,c2,old2,Board[r2][c2]))                                    
                    
    return Board



def findHiddenPairsInColumns(Board):
    """ check if columns contain Hidden Pairs
    """
    
    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findHiddenPairsInRows(TransposedBoard, 'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)  
                                        
    return Board



def findHiddenPairsInRows(Board, traceString):
    """ check if rows contain Hidden Pairs
    """

    for r in range(9):   
        pairsToSkip = []
        
        for c in range(9):
            candidates = []
            c1 = c2 = 0
            # get potential pairs in cell r,c
            if type(Board[r][c]) is list:
                candidates.extend(Board[r][c])
                
                for p1 in range(len(candidates)):
                    for p2 in range(p1+1, len(candidates)):
                        # cell r,c contains pair p1,p2
                        c1 = c
                        foundSecondPair = False
                        pair = [candidates[p1],candidates[p2]]
                        
                        if pair not in pairsToSkip:
                            pairsToSkip.append(pair)
                        
                            for cx in range(9):
                                if cx == c:
                                    continue
                                if type(Board[r][cx]) is list:
                                    if candidates[p1] in Board[r][cx] and candidates[p2] in Board[r][cx]:
                                        # cell r,cx contains pair candidates[p1],candidates[p2], too
                                        if foundSecondPair:
                                            # one pair to many
                                            foundSecondPair = False
                                            break
                                        else:
                                            foundSecondPair = True
                                            c2 = cx
                                    elif candidates[p1] in Board[r][cx] or candidates[p2] in Board[r][cx]:
                                        # no hidden pairs are possible anymore
                                        foundSecondPair = False
                                        break
                                    
                        if foundSecondPair:
                            # there are two hidden (or two naked) pairs in row r
                            # remove other candidates from these cells
                            old1 = deepcopy(Board[r][c1])
                            old2 = deepcopy(Board[r][c2])
                            Board[r][c1] = [candidates[p1],candidates[p2]]
                            Board[r][c2] = [candidates[p1],candidates[p2]]
                            if HIDDENPAIRS:
                                print('     HiddenPairsIn{}: ({},{}): {} -> {} , ({},{}): {} -> {}'.format(traceString,r,c1,old1,Board[r][c1],r,c2,old2,Board[r][c2]))                                                                                                    

    return Board



def excludeLockedCandidates1(Board):
    """ 
    Locked Candidates 1:
    Sometimes a candidate within a block is restricted to one row or column. 
    Since one of these cells must contain that specific candidate, 
    the candidate can safely be excluded from the remaining cells in that row
    or column outside of the block.
    """

    # Locked Candidates 1
    # loop over all 3x3-blocks
    for r in range(0,3):
        startRow = r * 3        
        endRow = startRow + 3

        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3 
            
            # get candidates in block 
            candidatesBlock = []
            for rx in range(startRow, endRow):
                for cx in range(startCol, endCol):
                     if type(Board[rx][cx]) is list:
                        candidatesBlock.extend(Board[rx][cx])           
            
            # convert to set to remove duplicates
            candidatesBlockSet = set(candidatesBlock)

            # check if a candidated in a block is confined to a row or column
            for candidate in candidatesBlockSet:
                rows = set([])
                columns = set([])
                for rx in range(startRow, endRow):
                    for cx in range(startCol, endCol):
                         if type(Board[rx][cx]) is list and candidate in Board[rx][cx]:
                             rows.add(rx)
                             columns.add(cx)
                if len(rows) == 1:
                    # candidate is confined to a row
                    # remove it from all cells of this row that are not in this block
                    rxx = rows.pop()
                    for cxx in range(9):
                        if cxx < endCol and cxx >= startCol:
                            # this is the current block
                            pass
                        else:
                            if type(Board[rxx][cxx]) is list: 
                                try:
                                    old = deepcopy(Board[rxx][cxx])
                                    Board[rxx][cxx].remove(candidate)
                                    if LOCKEDCANDIDATES1:
                                        print('     LockedCandidates1: ({},{}): {} -> {}'.format(rxx,cxx,old,Board[rxx][cxx]))                                                                                             
                                except ValueError as e:
                                    # that is ok
                                    pass                             
                        
                elif len(columns) == 1:
                    # candidate is confined to a column
                    # remove it from all cells of this column that are not in this block
                    cxx = columns.pop()
                    for rxx in range(9):
                        if rxx < endRow and rxx >= startRow:
                            # this is the current block
                            pass
                        else:
                            if type(Board[rxx][cxx]) is list: 
                                try:
                                    old = deepcopy(Board[rxx][cxx])
                                    Board[rxx][cxx].remove(candidate)
                                    if LOCKEDCANDIDATES1:
                                        print('     LockedCandidates1: ({},{}): {} -> {}'.format(rxx,cxx,old,Board[rxx][cxx]))                                                                                             
                                except ValueError as e:
                                    # that is ok
                                    pass

    return Board



def excludeLockedCandidates2(Board):
    """ 
    Locked Candidates 2:
    Sometimes a candidate within a row or column is restricted to one block. 
    Since one of these cells must contain that specific candidate, the 
    candidate can safely be excluded from the remaining cells in the block.
    """

    
    # Locked Candidates 2
    # loop over all 3x3-blocks
    for r in range(0,3):
        startRow = r * 3        
        endRow = startRow + 3

        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3 
            

            # check rows
            for rx in range(startRow, endRow):
                candidatesBlockRow = []
                for cx in range(startCol, endCol):
                    if type(Board[rx][cx]) is list:
                        candidatesBlockRow.extend(Board[rx][cx])

                # candidatesBlockRowSet contains the candidates of row rx in 
                # block (r,c)  (a set does not stores duplicates! ) 
                candidatesBlockRowSet = set(candidatesBlockRow)
                          
                # get ALL candidates of row rx of the Board
                candidatesRow = []
                for cx in range(9):
                    if type(Board[rx][cx]) is list:
                        candidatesRow.extend(Board[rx][cx])

                # remove all candiates of row rx in block (r,c) from 
                # list of candidates of row rx
                for candidate in candidatesBlockRow:
                    candidatesRow.remove(candidate)
                    
                # a member of candidatesBlockRowSet which is not in 
                # candidatesRow anymore can be removed from candidates of 
                # block (r,c) with exception of block row rx
                for candidate in candidatesBlockRowSet:
                    if candidate not in candidatesRow:
                        
                        for rxx in range(startRow, endRow):
                            if rxx != rx:
                                for cxx in range(startCol, endCol):
                                    if type(Board[rxx][cxx]) is list: 
                                        try:
                                            old = deepcopy(Board[rxx][cxx])
                                            Board[rxx][cxx].remove(candidate)
                                            if LOCKEDCANDIDATES2:
                                                print('     LockedCandidates2: ({},{}): {} -> {}'.format(rxx,cxx,old,Board[rxx][cxx]))                                             
                                        except ValueError as e:
                                            # that is ok
                                            pass                                


            # check columns
            for cx in range(startCol, endCol):
                candidatesBlockColumn = []
                for rx in range(startRow, endRow):
                    if type(Board[rx][cx]) is list:
                        candidatesBlockColumn.extend(Board[rx][cx])

                # candidatesBlockColumnSet contains the candidates of column cx in 
                # block (r,c)  (a set does not stores duplicates! ) 
                candidatesBlockColumnSet = set(candidatesBlockColumn)
                          
                # get ALL candidates of column cx of the Board
                candidatesColumn = []
                for rx in range(9):
                    if type(Board[rx][cx]) is list:
                        candidatesColumn.extend(Board[rx][cx])

                # remove all candiates of column cx in block (r,c) from 
                # list of candidates of column cx
                for candidate in candidatesBlockColumn:
                    candidatesColumn.remove(candidate)
                    
                # a member of candidatesBlockColumnSet which is not in 
                # candidatesColumn anymore can be removed from candidates of 
                # block (r,c) with exception of block column cx
                for candidate in candidatesBlockColumnSet:
                    if candidate not in candidatesColumn:
                        
                        for cxx in range(startCol, endCol):
                            if cxx != cx:
                                for rxx in range(startRow, endRow):
                                    if type(Board[rxx][cxx]) is list: 
                                        try:
                                            old = deepcopy(Board[rxx][cxx])
                                            Board[rxx][cxx].remove(candidate)
                                            if LOCKEDCANDIDATES2:
                                                print('     LockedCandidates2: ({},{}): {} -> {}'.format(rxx,cxx,old,Board[rxx][cxx]))                                                                                             
                                        except ValueError as e:
                                            # that is ok
                                            pass                                


    return Board



def findNakedTriples(Board):
    """ Run an check over 3x3-blocks, rows and columns  
        and find Naked Triples
    """    
    
    # check 3x3 blocks
    Board = findNakedTriplesInBlocks(Board)

    # check rows
    Board = findNakedTriplesInRows(Board,'Rows')

    # check columns
    Board = findNakedTriplesInColumns(Board)

                   
    return Board



def findNakedTriplesInBlocks(Board):
    """ check if 3x3-blocks contain Naked Triples
    """   
    
    for r in range(0,3):
        startRow = r * 3 
        endRow = startRow + 3
       
        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3 

            tripleToSkip = []
        
            for r1 in range(startRow,endRow):
                for c1 in range(startCol,endCol):
                    nakedTriple = False
                    breakOut = False 
         
                    if type(Board[r1][c1]) is list and (len(Board[r1][c1]) == 2 or len(Board[r1][c1]) == 3):
                        # that's the first candidate cell
                        for r2 in range(startRow,endRow):
                            for c2 in range(startCol,endCol):  
                                if c2 == c1 and r2 == r1:
                                    continue
                        
                                if type(Board[r2][c2]) is list and (len(Board[r2][c2]) == 2 or len(Board[r2][c2]) == 3):
                                    # that's the second candidate cell

                                    for r3 in range(startRow,endRow):
                                        for c3 in range(startCol,endCol):  
                                            if (c3 == c2 and r3 == r2) or (c3 == c1 and r3 == r1):
                                                continue

                                            if type(Board[r3][c3]) is list and (len(Board[r3][c3]) == 2 or len(Board[r3][c3]) == 3):
                                                # that's the third candidate cell 
                                                candidates = []
                                                candidates.extend(Board[r1][c1])
                                                candidates.extend(Board[r2][c2])
                                                candidates.extend(Board[r3][c3])
                                                candidateSet = set(candidates)
                                                
                                                # count frequency of candidates
                                                triple = dict((i, candidates.count(i)) for i in candidates)
                                                if len(triple) == 3:
                                                    # there are only 3 members in a triple
                                                    if candidateSet in tripleToSkip:
                                                        # leave c3 loop
                                                        breakOut = True
                                                        break 
                                                    else:
                                                        tripleToSkip.append(candidateSet)

                                                    nakedTriple = True
                                                    for k,v in triple.items():
                                                        if (v < 2 or v > 3):
                                                            # a Naked Triple requires a member count of 2 or 3
                                                            nakedTriple = False
                                                            break
                                                    if nakedTriple:
                                                        if NAKEDTRIPLES:
                                                            print('     Naked Triple found: ({},{}),({},{}),({},{})'.format(r1,c1,r2,c2,r3,c3))
                                                        # remove the members of the Naked Triple from other cells
                                                        for rx in range(startRow,endRow):
                                                            for cx in range(startCol,endCol):
                                                                
                                                                if (cx == c1 and rx == r1) or (cx == c2 and rx == r2) or (cx == c3 and rx == r3):
                                                                    pass
                                                                else:
                                                                    for k,v in triple.items():
                                                                        try:
                                                                            if type(Board[rx][cx]) is list:
                                                                                old = deepcopy(Board[rx][cx])
                                                                                Board[rx][cx].remove(k)
                                                                                if NAKEDTRIPLES:
                                                                                    print('     NakedTriplesInBlocks: ({},{}): {} -> {}'.format(rx,cx,old,Board[rx][cx]))                                                                                
                                                                        except ValueError as e:
                                                                            # that's ok
                                                                            pass
                                                        # leave c3 loop
                                                        breakOut = True
                                                        break
                                        if breakOut:
                                            # leave r3 loop
                                            break
                                    
                                    if breakOut:
                                        # leave c2 loop
                                        break
                            if breakOut:
                                # leave r2 loop
                                break                                        
                                    
                                    
    return Board



def findNakedTriplesInColumns(Board):
    """ check if columns contain Naked Triples
    """
    
    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findNakedTriplesInRows(TransposedBoard, 'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)
                                
    return Board



def findNakedTriplesInRows(Board, traceString):
    """ check if rows contain Naked Triples
    """
        
    for r in range(9):
    
        for c1 in range(9):
            nakedTriple = False
            breakOut = False
            if type(Board[r][c1]) is list and (len(Board[r][c1]) == 2 or len(Board[r][c1]) == 3):
                # that's the first candidate cell
                for c2 in range(c1+1,9):
                    if type(Board[r][c2]) is list and (len(Board[r][c2]) == 2 or len(Board[r][c2]) == 3):
                        # that's the second candidate cell
                        for c3 in range(c2+1,9):
                            breakOut = False
                            if type(Board[r][c3]) is list and (len(Board[r][c3]) == 2 or len(Board[r][c3]) == 3):
                                # that's the third candidate cell 
                                candidates = []
                                candidates.extend(Board[r][c1])
                                candidates.extend(Board[r][c2])
                                candidates.extend(Board[r][c3])
                                # count frequency of candidates
                                triple = dict((i, candidates.count(i)) for i in candidates)
                                if len(triple) == 3:
                                    # there are only 3 members in a triple
                                    nakedTriple = True
                                    for k,v in triple.items():
                                        if (v < 2 or v > 3):
                                            # a Naked Triple requires a member count of 2 or 3
                                            nakedTriple = False
                                            break
                                    if nakedTriple:
                                        if NAKEDTRIPLES:
                                            print('     Naked Triple found: ({},{}),({},{}),({},{})'.format(r,c1,r,c2,r,c3))                                        
                                        # remove the members of the Naked Triple from other cells
                                        for cx in range(9):
                                            if cx not in [c1,c2,c3]:
                                                for k,v in triple.items():
                                                    try:
                                                        if type(Board[r][cx]) is list:
                                                            old = deepcopy(Board[r][cx])
                                                            Board[r][cx].remove(k)
                                                            if NAKEDTRIPLES:
                                                                print('     NakedTriplesIn{}: ({},{}): {} -> {}'.format(traceString,r,cx,old,Board[r][cx]))                                                                
                                                    except ValueError as e:
                                                        # that's ok
                                                        pass
                                        # leave c3 loop
                                        breakOut = True
                                        break
                        if breakOut:
                            # leave c2 loop
                            break
                                
    return Board                                    
                                    


def findHiddenTriples(Board):
    """ Run an check over 3x3-blocks, rows and columns  
        and find Hidden Triples
    """    
    
    # check 3x3 blocks
    Board = findHiddenTriplesInBlocks(Board)

    # check rows
    Board = findHiddenTriplesInRows(Board, 'Rows')

    # check columns
    Board = findHiddenTriplesInColumns(Board)

                   
    return Board



def findHiddenTriplesInColumns(Board):
    """ check if columns contain Hidden Triples
    """
    
    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findHiddenTriplesInRows(TransposedBoard, 'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)  
                                        
    return Board



def findHiddenTriplesInRows(Board, traceString):
    """ check if rows contain Hidden Triples
    """

    for r in range(9):
        
        # collect triple candidates
        candidates = []    
        for c in range(9):            
            if type(Board[r][c]) is list:            
                candidates.extend(Board[r][c])            
            
        # count frequency of candidates
        tripleCandidates = dict((i, candidates.count(i)) for i in candidates) 
        deleteCandidates = []          
        for k,v in tripleCandidates.items():
            if (v < 2 or v > 3):
                # a Triple requires a member count of 2 or 3
                deleteCandidates.append(k)
        for delCan in deleteCandidates:        
            del tripleCandidates[delCan]
            try:
                while True:
                    candidates.remove(delCan)
            except ValueError as e:
                # that's ok
                pass

        if len(tripleCandidates) >= 3:
            # at least 3 candidates are required to form a triple
            
            # remove duplicates
            candidates = set(candidates)
            # group the candidates as combinations of 3 candidates
            combinations = list(itertools.combinations(candidates,3)) 
            for triple in combinations: 
                skipTriple = False
                # check if there are 3 cells that contain at least pairs of the 3 candidates
                cellList = [0,0,0,0,0,0,0,0,0]
                for c in range(9): 
                    candidatesPerCell = 0
                    if type(Board[r][c]) is list:  
                        if triple[0] in Board[r][c]:
                            candidatesPerCell += 1 
                        if triple[1] in Board[r][c]:
                            candidatesPerCell += 1                       
                        if triple[2] in Board[r][c]:
                            candidatesPerCell += 1
                    if candidatesPerCell == 1:
                        # only 1 triple candidate in cell -> not a triple
                        skipTriple = True
                        break
                    elif candidatesPerCell > 1:
                        cellList[c] = candidatesPerCell
                        
                if skipTriple:
                    continue
                
                tripleCells = 0
                for c in range(9):
                    if cellList[c] > 0:
                        tripleCells += 1
                        
                if tripleCells == 3:
                    # hidden triple found                                     
                
                    for c in range(9):
                        if cellList[c] > 1:
                            
                            # remove other candidates
                            # convert to set to do some arithmetic
                            old = deepcopy(Board[r][c])
                            Board[r][c] = deepcopy(sorted(list(set(Board[r][c]) - ( set(Board[r][c])-set(triple) ) )))
                            if HIDDENTRIPLES:
                                print('     HiddenTriplesIn{}: ({},{}): {} -> {}'.format(traceString,r,c,old,Board[r][c]))                                                                
                                                
    return Board



def findHiddenTriplesInBlocks(Board):
    """ check if 3x3 blocks contain Hidden Triples
    """

    for r in range(0,3):
        startRow = r * 3 
        endRow = startRow + 3
       
        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3 

            # collect triple candidates
            candidates = []    
            for r1 in range(startRow, endRow):  
                for c1 in range(startCol, endCol):                 
                    if type(Board[r1][c1]) is list:            
                        candidates.extend(Board[r1][c1])

            # count frequency of candidates
            tripleCandidates = dict((i, candidates.count(i)) for i in candidates) 
            deleteCandidates = []          
            for k,v in tripleCandidates.items():
                if (v < 2 or v > 3):
                    # a Triple requires a member count of 2 or 3
                    deleteCandidates.append(k)
            for delCan in deleteCandidates:        
                del tripleCandidates[delCan]
                try:
                    while True:
                        candidates.remove(delCan)
                except ValueError as e:
                    # that's ok
                    pass
            

            if len(tripleCandidates) >= 3:
                # at least 3 candidates are required to form a triple
                
                # remove duplicates
                candidates = set(candidates)
                # group the candidates as combinations of 3 candidates
                combinations = list(itertools.combinations(candidates,3)) 
                for triple in combinations: 
                    skipTriple = False
                    # check if there are 3 cells that contain at least pairs of the 3 candidates                    
                    cellList = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]                    
                    for r1 in range(startRow, endRow):  
                        for c1 in range(startCol, endCol):                    
                            candidatesPerCell = 0
                            if type(Board[r1][c1]) is list:  
                                if triple[0] in Board[r1][c1]:
                                    candidatesPerCell += 1 
                                if triple[1] in Board[r1][c1]:
                                    candidatesPerCell += 1                       
                                if triple[2] in Board[r1][c1]:
                                    candidatesPerCell += 1
                            if candidatesPerCell == 1:
                                # only 1 triple candidate in cell -> not a triple
                                skipTriple = True
                                break
                            elif candidatesPerCell > 1:
                                cellList[r1][c1] = candidatesPerCell

                        if skipTriple:
                            break
                            
                    if skipTriple:
                        continue
                    
                    tripleCells = 0
                    for r1 in range(startRow, endRow):  
                        for c1 in range(startCol, endCol):                     
                            if cellList[r1][c1] > 0:
                                tripleCells += 1
                            
                    if tripleCells == 3:
                        # hidden triple found                                     

                        for r1 in range(startRow, endRow):  
                            for c1 in range(startCol, endCol):                    
                                if cellList[r1][c1] > 1:
                                    
                                    # remove other candidates
                                    # convert to set to do some arithmetic
                                    old = deepcopy(Board[r1][c1])
                                    Board[r1][c1] = deepcopy(sorted(list(set(Board[r1][c1]) - ( set(Board[r1][c1])-set(triple) ) )))
                                    if HIDDENTRIPLES:
                                        print('     HiddenTriplesInBlocks: ({},{}): {} -> {}'.format(r1,c1,old,Board[r1][c1]))                                                                
                                                
    return Board



def findNakedQuadruples(Board):
    """ Run an check over 3x3-blocks, rows and columns  
        and find Naked Quadruples
    """    
    
    # check 3x3 blocks
    Board = findNakedQuadruplesInBlocks(Board)

    # check rows
    Board = findNakedQuadruplesInRows(Board, 'Rows')

    # check columns
    Board = findNakedQuadruplesInColumns(Board)

                   
    return Board



def findNakedQuadruplesInBlocks(Board):
    """ check if 3x3-blocks contain Naked Quadruples
    """   
    
    for r in range(0,3):
        startRow = r * 3 
        endRow = startRow + 3
       
        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3 

            quadrupleToSkip = []
        
            for r1 in range(startRow,endRow):
                for c1 in range(startCol,endCol):
                    nakedQuadruple = False
                    breakOut = False         
                    if type(Board[r1][c1]) is list and (len(Board[r1][c1]) >= 2 and len(Board[r1][c1]) <= 4):
                        # that's the first candidate cell
                        for r2 in range(startRow,endRow):
                            for c2 in range(startCol,endCol):  
                                if c2 == c1 and r2 == r1:
                                    continue
                        
                                if type(Board[r2][c2]) is list and (len(Board[r2][c2]) >= 2 and len(Board[r2][c2]) <= 4):
                                    # that's the second candidate cell

                                    for r3 in range(startRow,endRow):
                                        for c3 in range(startCol,endCol):  
                                            if (c3 == c2 and r3 == r2) or (c3 == c1 and r3 == r1):
                                                continue

                                            if type(Board[r3][c3]) is list and (len(Board[r3][c3]) >= 2 and len(Board[r3][c3]) <= 4):
                                                # that's the third candidate cell 
                                                
                                                for r4 in range(startRow,endRow):
                                                    for c4 in range(startCol,endCol):  
                                                        if (c4 == c3 and r4 == r3) or (c4 == c2 and r4 == r2) or (c4 == c1 and r4 == r1):
                                                            continue
            
                                                        if type(Board[r4][c4]) is list and (len(Board[r4][c4]) >= 2 and len(Board[r4][c4]) <= 4):
                                                            # that's the fourth candidate cell                                                
                                                
                                                            candidates = []
                                                            candidates.extend(Board[r1][c1])
                                                            candidates.extend(Board[r2][c2])
                                                            candidates.extend(Board[r3][c3])
                                                            candidates.extend(Board[r4][c4])
                                                            candidateSet = set(candidates)
                                                            
                                                            # count frequency of candidates
                                                            quadruple = dict((i, candidates.count(i)) for i in candidates)
                                                            if len(quadruple) == 4:
                                                                # there are only 4 members in a quadruple
                                                                if candidateSet in quadrupleToSkip:
                                                                    # leave c4 loop
                                                                    breakOut = True
                                                                    break 
                                                                else:
                                                                    quadrupleToSkip.append(candidateSet)
            
                                                                nakedQuadruple = True
                                                                for k,v in quadruple.items():
                                                                    if (v < 2 or v > 4):
                                                                        # a Naked Quadruple requires a member count of 2, 3 or 4
                                                                        nakedQuadruple = False
                                                                        break
                                                                if nakedQuadruple:
                                                                    if NAKEDQUADRUPLES:
                                                                        print('     Naked Quadruple found: ({},{}),({},{}),({},{}),({},{})'.format(r1,c1,r2,c2,r3,c3,r4,c4))                                        
                                                                    # remove the members of the Naked Quadruple from other cells
                                                                    for rx in range(startRow,endRow):
                                                                        for cx in range(startCol,endCol):
                                                                            
                                                                            if (cx == c1 and rx == r1) or (cx == c2 and rx == r2) or (cx == c3 and rx == r3) or (cx == c4 and rx == r4):
                                                                                pass
                                                                            else:
                                                                                for k,v in quadruple.items():
                                                                                    try:
                                                                                        if type(Board[rx][cx]) is list:
                                                                                            old = deepcopy(Board[rx][cx])
                                                                                            Board[rx][cx].remove(k)
                                                                                            if NAKEDQUADRUPLES:
                                                                                                print('     NakedQuadruplesInBlocks: ({},{}): {} -> {}'.format(rx,cx,old,Board[rx][cx]))                                                                                
                                                                                    except ValueError as e:
                                                                                        # that's ok
                                                                                        pass
                                                                    # leave c4 loop
                                                                    breakOut = True
                                                                    break
                                                    if breakOut:
                                                        # leave r4 loop
                                                        break
                                    
                                            if breakOut:
                                                # leave c3 loop
                                                break
                                        if breakOut:
                                            # leave r3 loop
                                            break                                        
                                if breakOut:
                                    # leave c2 loop
                                    break
                            if breakOut:
                                # leave r2 loop
                                break                                      
                                    
    return Board



def findNakedQuadruplesInColumns(Board):
    """ check if columns contain Naked Quadruples
    """

    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findNakedQuadruplesInRows(TransposedBoard, 'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)

                                
    return Board



def findNakedQuadruplesInRows(Board, traceString):
    """ check if rows contain Naked Quadruples
    """
        
    for r in range(9):
    
        for c1 in range(9):
            nakedQuadruple = False
            breakOut = False
            if type(Board[r][c1]) is list and (len(Board[r][c1]) >= 2 and len(Board[r][c1]) <= 4):
                # that's the first candidate cell
                for c2 in range(c1+1,9):
                    if type(Board[r][c2]) is list and (len(Board[r][c2]) >= 2 and len(Board[r][c2]) <= 4):
                        # that's the second candidate cell
                        for c3 in range(c2+1,9):                                                                                                                
                            if type(Board[r][c3]) is list and (len(Board[r][c3]) >= 2 and len(Board[r][c3]) <= 4):
                                # that's the third candidate cell 
                                for c4 in range(c3+1,9):                                                                                                                
                                    breakOut = False
                                    if type(Board[r][c4]) is list and (len(Board[r][c4]) >= 2 and len(Board[r][c4]) <= 4):
                                        # that's the fourth candidate cell                                 
                                
                                        candidates = []
                                        candidates.extend(Board[r][c1])
                                        candidates.extend(Board[r][c2])
                                        candidates.extend(Board[r][c3])
                                        candidates.extend(Board[r][c4])
                                
                                        # count frequency of candidates
                                        quadruple = dict((i, candidates.count(i)) for i in candidates)
                                        if len(quadruple) == 4:
                                            # there are only 4 members in a quadruple
                                            nakedQuadruple = True
                                            for k,v in quadruple.items():
                                                if (v < 2 or v > 4):
                                                    # a Naked Quadruple requires a member count of 2, 3 or 4
                                                    nakedQuadruple = False
                                                    break
                                            if nakedQuadruple:
                                                if NAKEDQUADRUPLES:
                                                    print('     Naked Quadruple found: ({},{}),({},{}),({},{}),({},{})'.format(r,c1,r,c2,r,c3,r,c4))                                        
                                                # remove the members of the Naked Quadruple from other cells
                                                for cx in range(9):
                                                    if cx not in [c1,c2,c3,c4]:
                                                        for k,v in quadruple.items():
                                                            try:
                                                                if type(Board[r][cx]) is list:
                                                                    old = deepcopy(Board[r][cx])
                                                                    Board[r][cx].remove(k)
                                                                    if NAKEDQUADRUPLES:
                                                                        print('     NakedQuadruplesIn{}: ({},{}): {} -> {}'.format(traceString,r,cx,old,Board[r][cx]))                                                                
                                                            except ValueError as e:
                                                                # that's ok
                                                                pass
                                                # leave c4 loop
                                                breakOut = True
                                                break
                                if breakOut:
                                    # leave c3 loop
                                    break
                if breakOut:
                    # leave c2 loop
                    break                                
                                
    return Board                                    

                                    

def findHiddenQuadruples(Board):
    """ Run an check over 3x3-blocks, rows and columns  
        and find Hidden Quadruples
    """    
    
    # check 3x3 blocks
    Board = findHiddenQuadruplesInBlocks(Board)

    # check rows
    Board = findHiddenQuadruplesInRows(Board, 'Rows')

    # check columns
    Board = findHiddenQuadruplesInColumns(Board)

                   
    return Board



def findHiddenQuadruplesInColumns(Board):
    """ check if columns contain Hidden Quadruples
    """
    
    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findHiddenQuadruplesInRows(TransposedBoard, 'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)  
                                        
    return Board



def findHiddenQuadruplesInRows(Board, traceString):
    """ check if rows contain Hidden Quadruples
    """

    for r in range(9):
        
        # collect quadruple candidates
        candidates = []    
        for c in range(9):  
           if type(Board[r][c]) is list:            
                candidates.extend(Board[r][c])  

        # count frequency of candidates
        quadrupleCandidates = dict((i, candidates.count(i)) for i in candidates) 
        
        deleteCandidates = []          
        for k,v in quadrupleCandidates.items():
            if (v < 2 or v > 4):
                # a Quadruple requires a member count of 2 or 3 or 4
                deleteCandidates.append(k)
        for delCan in deleteCandidates:        
            del quadrupleCandidates[delCan]
            try:
                while True:
                    candidates.remove(delCan)
            except ValueError as e:
                # that's ok
                pass

        if len(quadrupleCandidates) >= 4:
            # at least 4 candidates are required to form a quadruple
            
            # remove duplicates
            candidates = set(candidates)
            # group the candidates as combinations of 4 candidates
            combinations = list(itertools.combinations(candidates,4)) 
            for quadruple in combinations: 
                skipQuadruple = False
                # check if there are 4 cells that contain at least pairs of the 4 candidates
                cellList = [0,0,0,0,0,0,0,0,0]
                for c in range(9): 
                    candidatesPerCell = 0
                    if type(Board[r][c]) is list:  
                        if quadruple[0] in Board[r][c]:
                            candidatesPerCell += 1 
                        if quadruple[1] in Board[r][c]:
                            candidatesPerCell += 1  
                        if quadruple[2] in Board[r][c]:
                            candidatesPerCell += 1                            
                        if quadruple[3] in Board[r][c]:
                            candidatesPerCell += 1
                    if candidatesPerCell == 1:
                        # only 1 quadruple candidate in cell -> not a quadruple
                        skipQuadruple = True
                        break
                    elif candidatesPerCell > 1:
                        cellList[c] = candidatesPerCell
                        
                if skipQuadruple:
                    continue
                
                quadrupleCells = 0
                for c in range(9):
                    if cellList[c] > 0:
                        quadrupleCells += 1
                        
                if quadrupleCells == 4:
                    # hidden quadrupleCells found                                     
                
                    for c in range(9):
                        if cellList[c] > 1:
                            
                            # remove other candidates
                            # convert to set to do some arithmetic
                            old = deepcopy(Board[r][c])
                            Board[r][c] = deepcopy(sorted(list(set(Board[r][c]) - ( set(Board[r][c])-set(quadruple) ) )))
                            if HIDDENQUADRUPLES:
                                print('     HiddenQuadruplesIn{}: ({},{}): {} -> {}'.format(traceString,r,c,old,Board[r][c]))                                                                
                                                
    return Board



def findHiddenQuadruplesInBlocks(Board):
    """ check if 3x3 blocks contain Hidden Quadruples
    """

    for r in range(0,3):
        startRow = r * 3 
        endRow = startRow + 3
       
        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3 

            # collect quadruple candidates
            candidates = []    
            for r1 in range(startRow, endRow):  
                for c1 in range(startCol, endCol):                 
                    if type(Board[r1][c1]) is list:            
                        candidates.extend(Board[r1][c1])

            # count frequency of candidates
            quadrupleCandidates = dict((i, candidates.count(i)) for i in candidates) 
            deleteCandidates = []          
            for k,v in quadrupleCandidates.items():
                if (v < 2 or v > 4):
                    # a Quadruple requires a member count of 2 or 3 or 4
                    deleteCandidates.append(k)
            for delCan in deleteCandidates:        
                del quadrupleCandidates[delCan]
                try:
                    while True:
                        candidates.remove(delCan)
                except ValueError as e:
                    # that's ok
                    pass
            

            if len(quadrupleCandidates) >= 4:
                # at least 4 candidates are required to form a quadruple
                
                # remove duplicates
                candidates = set(candidates)
                # group the candidates as combinations of 4 candidates
                combinations = list(itertools.combinations(candidates,4)) 
                for quadruple in combinations: 
                    skipQuadruple = False
                    # check if there are 4 cells that contain at least pairs of the 4 candidates                    
                    cellList = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]                    
                    for r1 in range(startRow, endRow):  
                        for c1 in range(startCol, endCol):                    
                            candidatesPerCell = 0
                            if type(Board[r1][c1]) is list:  
                                if quadruple[0] in Board[r1][c1]:
                                    candidatesPerCell += 1 
                                if quadruple[1] in Board[r1][c1]:
                                    candidatesPerCell += 1                       
                                if quadruple[2] in Board[r1][c1]:
                                    candidatesPerCell += 1
                                if quadruple[3] in Board[r1][c1]:
                                    candidatesPerCell += 1                                    
                            if candidatesPerCell == 1:
                                # only 1 triple candidate in cell -> not a triple
                                skipQuadruple = True
                                break
                            elif candidatesPerCell > 1:
                                cellList[r1][c1] = candidatesPerCell

                        if skipQuadruple:
                            break
                            
                    if skipQuadruple:
                        continue
                    
                    quadrupleCells = 0
                    for r1 in range(startRow, endRow):  
                        for c1 in range(startCol, endCol):                     
                            if cellList[r1][c1] > 0:
                                quadrupleCells += 1
                            
                    if quadrupleCells == 4:
                        # hidden quadruple found                                     

                        for r1 in range(startRow, endRow):  
                            for c1 in range(startCol, endCol):                    
                                if cellList[r1][c1] > 1:
                                    
                                    # remove other candidates
                                    # convert to set to do some arithmetic
                                    old = deepcopy(Board[r1][c1])
                                    Board[r1][c1] = deepcopy(sorted(list(set(Board[r1][c1]) - ( set(Board[r1][c1])-set(quadruple) ) )))
                                    if HIDDENQUADRUPLES:
                                        print('     HiddenQuadruplesInBlocks: ({},{}): {} -> {}'.format(r1,c1,old,Board[r1][c1]))                                                                
                                                
    return Board



def findXWing(Board):
    """ Look for X-Wing pattern in rows and columns  
    """    

    # check rows
    Board = findXWingInRows(Board,'Rows')

    # check columns
    Board = findXWingInColumns(Board)

                   
    return Board



def findXWingInColumns(Board):
    """ Look for X-Wing pattern in columns
    """
    
    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findXWingInRows(TransposedBoard, 'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)  
                                        
    return Board



def findXWingInRows(Board, traceString):
    """ Look for X-Wing pattern in rows
    """ 
    
    #  {row:  {candidate: [col1, col2]} }
    xWingDict = {}
    
    for r in range(9):
        xwRowDict = {}
        # look for a candidate that occurs exactly twice in a row
        candidates = []
        for c in range(9):
            if type(Board[r][c]) is list:            
                candidates.extend(Board[r][c])        
            
        # count frequency of candidates
        candidateDict = dict((i, candidates.count(i)) for i in candidates)         
        for cand, freq in candidateDict.items():
            if (freq == 2): 
                cols = []
                for c in range(9):
                    if type(Board[r][c]) is list and cand in Board[r][c] : 
                        cols.append(c)
                xwRowDict[cand] = cols
        
        if xwRowDict != {}:        
            xWingDict[r] = xwRowDict
            
            
    for r1, rowDict in xWingDict.items():
        for cand1, cols1 in rowDict.items():        
            for r2, rowDict in xWingDict.items():
                if r1 != r2:
                    for cand2, cols2 in rowDict.items():
                        if cand1 == cand2 and cols1[0] == cols2[0] and cols1[1] == cols2[1]:
                            # X-Wing found
                            if XWING:
                                print('     findXWingIn{}: {}: ({},{}) , ({},{}) , ({},{}) , ({},{}) '.
                                      format(traceString,cand1,r1,cols1[0],r1,cols1[1],r2,cols1[0],r2,cols1[1]))  
                            
                            # remove candidate from columns                                                              
                            for r in range(9):
                                if r == r1 or r == r2:
                                    continue
                                else:
                                    if type(Board[r][cols1[0]]) is list:
                                        old = deepcopy(Board[r][cols1[0]])
                                        try:
                                            Board[r][cols1[0]].remove(cand1)
                                        except ValueError as e:
                                            # that's ok
                                            pass
                                        else:
                                            if XWING:
                                                print('     findXWingIn{}: ({},{}): {} -> {}'.format(traceString,r,cols1[0],old,Board[r][cols1[0]]))                                                                
                                    if type(Board[r][cols1[1]]) is list:
                                        old = deepcopy(Board[r][cols1[1]])
                                        try:
                                            Board[r][cols1[1]].remove(cand1)
                                        except ValueError as e:
                                            # that's ok
                                            pass
                                        else:
                                            if XWING:
                                                print('     findXWingIn{}: ({},{}): {} -> {}'.format(traceString,r,cols1[1],old,Board[r][cols1[1]]))                                                                

    return Board                                            



def findSwordfish(Board):
    """ Look for Swordfish pattern in rows and columns  
    """    

    # check rows
    Board = findSwordfishInRows(Board,'Rows')

    # check columns
    Board = findSwordfishInColumns(Board)

                   
    return Board



def findSwordfishInColumns(Board):
    """ Look for Swordfish pattern in columns
    """
    
    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findSwordfishInRows(TransposedBoard, 'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)  
                                        
    return Board



def findSwordfishInRows(Board, traceString):
    """ Look for Swordfish pattern in rows
    """ 
    
    #  {row:  {candidate: [col1, col2, col3]} }
    swordfishDict = {}
    
    for r in range(9):
        sfRowDict = {}
        # look for a candidate that occurs twice or three times in a row
        candidates = []
        for c in range(9):
            if type(Board[r][c]) is list:            
                candidates.extend(Board[r][c])        
            
        # count frequency of candidates
        candidateDict = dict((i, candidates.count(i)) for i in candidates)         
        for cand, freq in candidateDict.items():
            if (freq == 2 or freq == 3): 
                cols = []
                for c in range(9):
                    if type(Board[r][c]) is list and cand in Board[r][c] : 
                        cols.append(c)
                sfRowDict[cand] = cols
        
        if sfRowDict != {}:        
            swordfishDict[r] = sfRowDict
            
            
    for r1, rowDict in swordfishDict.items():
        for cand1, cols1 in rowDict.items():        
            for r2, rowDict in swordfishDict.items():
                if r1 != r2:
                    for cand2, cols2 in rowDict.items():
                        if cand1 == cand2:
                            colSet = set(cols1) | set(cols2)
                            if len(colSet) < 4:
                                for r3, rowDict in swordfishDict.items():
                                    if r1 != r2 and r1 != r3 and r2 != r3:  
                                        for cand3, cols3 in rowDict.items():                                                
                                            if cand2 == cand3:
                                                colSet = set(cols1) | set(cols2) | set(cols3)
                                                if len(colSet) < 4:                                                        
                                                    # Swordfish found
                                                    if SWORDFISH:
                                                        print('     findSwordfishIn{}: {}: row: {} cols: {} , row: {} cols: {} , row: {} cols:,{}'.
                                                              format(traceString,cand1,r1,cols1,r2,cols2,r3,cols3))  
                                    
                                                    # remove candidate from columns                                                              
                                                    for r in range(9):
                                                        if r == r1 or r == r2 or r == r3:
                                                            continue
                                                        else:
                                                            for col in colSet:
                                                                if type(Board[r][col]) is list:
                                                                    old = deepcopy(Board[r][col])
                                                                    try:
                                                                        Board[r][col].remove(cand1)
                                                                    except ValueError as e:
                                                                        # that's ok
                                                                        pass
                                                                    else:
                                                                        if SWORDFISH:
                                                                            print('     findSwordfishIn{}: ({},{}): {} -> {}'.format(traceString,r,col,old,Board[r][col]))                                                                
    
    return Board                                            



def findJellyfish(Board):
    """ Look for Jellyfish pattern in rows and columns  
    """    

    # check rows
    Board = findJellyfishInRows(Board,'Rows')

    # check columns
    Board = findJellyfishInColumns(Board)

                   
    return Board



def findJellyfishInColumns(Board):
    """ Look for Jellyfish pattern in columns
    """
    
    TransposedBoard = transposeBoard(Board)
            
    # do the work        
    TransposedBoard = findJellyfishInRows(TransposedBoard, 'TransposedColumns')
   
    Board = transposeBoard(TransposedBoard)  
                                        
    return Board



def findJellyfishInRows(Board, traceString):
    """ Look for Jellyfish pattern in rows
    """ 
    
    #  {row:  {candidate: [col1, col2, col3, col4]} }
    jellyfishDict = {}
    
    for r in range(9):
        jfRowDict = {}
        # look for a candidate that occurs two to four times in a row
        candidates = []
        for c in range(9):
            if type(Board[r][c]) is list:            
                candidates.extend(Board[r][c])        
            
        # count frequency of candidates
        candidateDict = dict((i, candidates.count(i)) for i in candidates)         
        for cand, freq in candidateDict.items():
            if (freq >= 2 and freq < 5): 
                cols = []
                for c in range(9):
                    if type(Board[r][c]) is list and cand in Board[r][c] : 
                        cols.append(c)
                jfRowDict[cand] = cols
        
        if jfRowDict != {}:        
            jellyfishDict[r] = jfRowDict
            
            
    for r1, rowDict in jellyfishDict.items():
        for cand1, cols1 in rowDict.items():        
            for r2, rowDict in jellyfishDict.items():
                if r1 != r2:
                    for cand2, cols2 in rowDict.items():
                        if cand1 == cand2:
                            colSet = set(cols1) | set(cols2)
                            if len(colSet) < 5:
                                for r3, rowDict in jellyfishDict.items():
                                    if r1 != r2 and r1 != r3 and r2 != r3:  
                                        for cand3, cols3 in rowDict.items():                                                
                                            if cand2 == cand3:
                                                colSet = set(cols1) | set(cols2) | set(cols3)
                                                if len(colSet) < 5: 
                                                    for r4, rowDict in jellyfishDict.items():
                                                        if r1 != r2 and r1 != r3 and r2 != r3 and r1 != r4 and r2 != r4 and r3 != r4:  
                                                            for cand4, cols4 in rowDict.items():                                                
                                                                if cand3 == cand4:
                                                                    colSet = set(cols1) | set(cols2) | set(cols3) | set(cols4)
                                                                    if len(colSet) < 5:                                                      
                                                                        # JellyfishDict found
                                                                        if JELLYFISH:
                                                                            print('     findJellyfishIn{}: {}: row: {} cols: {} , row: {} cols: {} , row: {} cols:{} , row: {} cols:{}'.
                                                                                  format(traceString,cand1,r1,cols1,r2,cols2,r3,cols3,r4,cols4))  
                                                        
                                                                        # remove candidate from columns                                                              
                                                                        for r in range(9):
                                                                            if r == r1 or r == r2 or r == r3 or r == r4:
                                                                                continue
                                                                            else:
                                                                                for col in colSet:
                                                                                    if type(Board[r][col]) is list:
                                                                                        old = deepcopy(Board[r][col])
                                                                                        try:
                                                                                            Board[r][col].remove(cand1)
                                                                                        except ValueError as e:
                                                                                            # that's ok
                                                                                            pass
                                                                                        else:
                                                                                            if JELLYFISH:
                                                                                                print('     findJellyfishIn{}: ({},{}): {} -> {}'.format(traceString,r,col,old,Board[r][col]))                                                                
                        
    return Board                                            



def findXYWing(Board):
    """ check if board contains XY-Wing pattern
    """
    
    # pairs = list of candidates
    # candidate = ( [pair] , (row,col) )
    verbosePairs = []
            
    for r in range(9):    
        for c in range(9):
            if type(Board[r][c]) is list and len(Board[r][c]) == 2:
                candidate = list( (Board[r][c],(r,c)) )
                verbosePairs.append(candidate)
                
    # potential candidates for XY-wing are combinations of pairs
    candidates = itertools.combinations(verbosePairs,3)
    
    for cand in candidates:            
        setC = set()
        setC.add(cand[0][0][0])
        setC.add(cand[0][0][1])
        setC.add(cand[1][0][0])
        setC.add(cand[1][0][1])            
        setC.add(cand[2][0][0])
        setC.add(cand[2][0][1])         
            
        if len(setC) == 3 and cand[0][0] != cand[1][0] and cand[0][0] != cand[2][0] and cand[1][0] != cand[2][0]:            
            # potential candidates for XY-wing are combinations of pairs
            # of three distinct candidates
            # pattern:  ab, bc, ac
             
            # There are two arrangements for a XY-wing pattern:
            #
            # 1) The three pairs form three vertices of a rectangle.
            #
            # 2) Two pairs have to reside in the same block and the third pair
            #    must be in the same row or column as one of the other pairs.
            
            r1 = cand[0][1][0]
            c1 = cand[0][1][1]
            r2 = cand[1][1][0]
            c2 = cand[1][1][1]                
            r3 = cand[2][1][0]
            c3 = cand[2][1][1] 
            
            
            if (r1 == r2 and r1 == r3) or (c1 == c2 and c1 == c3):
                # triple in a row or column
                continue
                        
            
            # Look for arrangement 1
            
            Board, modifiedBoard = findXYWingRectangle(Board,r1,c1,r2,c2,r3,c3)
            if modifiedBoard:
                return Board
            
            Board, modifiedBoard = findXYWingRectangle(Board,r2,c2,r3,c3,r1,c1)
            if modifiedBoard:
                return Board
            
            Board, modifiedBoard = findXYWingRectangle(Board,r3,c3,r1,c1,r2,c2)
            if modifiedBoard:
                return Board  
            
            
            # Look for arrangement 2
                        
            for r in range(0,3):
                startRow = r * 3 
                endRow = startRow + 3
               
                for c in range(0,3):
                    startCol = c * 3 
                    endCol = startCol + 3  
                    
                    Board, foundXYWing, modifiedBoard = findXYWingBlock(Board,startRow,endRow,startCol,endCol,r1,c1,r2,c2,r3,c3)
                    if modifiedBoard:
                        return Board
                    
                    if not foundXYWing:
                        Board, foundXYWing, modifiedBoard = findXYWingBlock(Board,startRow,endRow,startCol,endCol,r2,c2,r3,c3,r1,c1)
                    if modifiedBoard:
                        return Board
                    
                    if not foundXYWing:
                        Board, foundXYWing, modifiedBoard = findXYWingBlock(Board,startRow,endRow,startCol,endCol,r3,c3,r1,c1,r2,c2)
                    if modifiedBoard:
                        return Board 
      
    return Board                                    



def findXYWingRectangle(Board,r1,c1,r2,c2,r3,c3):
    """ The three pairs form three vertices of a rectangle.
    """
    
    modifiedBoard = False
    
    
    if r1 == r2:
        # basis of the rectangle
        
        if c1 == c3:
            # 4th vertex: (r3,c2)
            if type(Board[r3][c2]) is list:
                old = deepcopy(Board[r3][c2])
                # get the number that is to be removed
                x = (set(Board[r3][c1]) & set(Board[r1][c2])).pop()
                try:
                    Board[r3][c2].remove(x)
                except ValueError as e:
                    # that's ok
                    pass
                else: 
                    modifiedBoard = True
                    if XYWING:
                        print('     findXYWingRectangle: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                        print('                          ({},{}): {} -> {}'.format(r3,c2,old,Board[r3][c2])) 
                                                                  
                
        elif c2 == c3:
            # 4th vertex: (r3,c1)
            if type(Board[r3][c1]) is list:                                                                                                           
                old = deepcopy(Board[r3][c1])
                # get the number that is to be removed
                x = (set(Board[r3][c2]) & set(Board[r1][c1])).pop()
                try:
                    Board[r3][c1].remove(x)
                except ValueError as e:
                    # that's ok
                    pass
                else: 
                    modifiedBoard = True
                    if XYWING:
                        print('     findXYWingRectangle: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                        print('                          ({},{}): {} -> {}'.format(r3,c1,old,Board[r3][c1]))

    return Board, modifiedBoard



def findXYWingBlock(Board,startRow,endRow,startCol,endCol,r1,c1,r2,c2,r3,c3):
    """ Two pairs have to reside in the same block and the third pair
        must be in the same row or column as one of the other pairs.
    """
    
    foundXYWing = False
    modifiedBoard = False
    
                    
    if r1 >= startRow and r1 < endRow and c1 >= startCol and c1 < endCol and \
       r2 >= startRow and r2 < endRow and c2 >= startCol and c2 < endCol:
        # cand 1 and 2 are in the same block
        if r3 >= startRow and r3 < endRow and c3 >= startCol and c3 < endCol:
            # that's a triple in a block
            pass
        elif (r1 == r2 and r1 == r3) or (c1 == c2 and c1 == c3):
            # that's a triple in a row or column
            pass   
        elif r3 == r1:
            # cand 3 shares the row with cand 1 
            # cand 1 is the pivot
            foundXYWing = True

            # get the number that is to be removed from all intersections of cand 2 and 3
            x = (set(Board[r2][c2]) & set(Board[r3][c3])).pop()
            
            # get cols of block of cand 3
            for c in range(0,3):
                startCol3 = c * 3 
                endCol3 = startCol3 + 3
                if c3 < endCol3:
                    break

            #            
            # remove x from all intersections of cand 2 and 3
            #
            for c in range(startCol3,endCol3):
            
                if type(Board[r2][c]) is list:
                    old = deepcopy(Board[r2][c])
                    try:
                        Board[r2][c].remove(x)
                    except ValueError as e:
                        # that's ok
                        pass
                    else: 
                        modifiedBoard = True
                        if XYWING:
                            print('     findXYWingBlock: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                            print('                      ({},{}): {} -> {}'.format(r2,c,old,Board[r2][c]))                                                                

            for c in range(startCol,endCol):
            
                if c != c1 and type(Board[r1][c]) is list:
                    old = deepcopy(Board[r1][c])
                    try:
                        Board[r1][c].remove(x)
                    except ValueError as e:
                        # that's ok
                        pass
                    else: 
                        modifiedBoard = True
                        if XYWING:
                            print('     findXYWingBlock: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                            print('                      ({},{}): {} -> {}'.format(r1,c,old,Board[r1][c]))                                                                

        elif c3 == c1:
            # cand 3 shares the column with cand 1 
            # cand 1 is the pivot
            foundXYWing = True

            # get the number that is to be removed from all intersections of cand 2 and 3
            x = (set(Board[r2][c2]) & set(Board[r3][c3])).pop()
            
            # get rows of block of cand 3
            for r in range(0,3):
                startRow3 = r * 3 
                endRow3 = startRow3 + 3
                if r3 < endRow3:
                    break

            #            
            # remove x from all intersections of cand 2 and 3
            #
            for r in range(startRow3,endRow3):
            
                if type(Board[r][c2]) is list:
                    old = deepcopy(Board[r][c2])                    
                    try:
                        Board[r][c2].remove(x)
                    except ValueError as e:
                        # that's ok
                        pass
                    else: 
                        modifiedBoard = True
                        if XYWING:
                            print('     findXYWingBlock: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                            print('                      ({},{}): {} -> {}'.format(r,c2,old,Board[r][c2]))                                                                

            for r in range(startRow,endRow):
            
                if r != r1 and type(Board[r][c1]) is list:
                    old = deepcopy(Board[r][c1])
                    try:
                        Board[r][c1].remove(x)
                    except ValueError as e:
                        # that's ok
                        pass
                    else: 
                        modifiedBoard = True
                        if XYWING:
                            print('     findXYWingBlock: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                            print('                      ({},{}): {} -> {}'.format(r,c1,old,Board[r][c1]))                                                                


                                           
        elif r3 == r2:
            # cand 3 shares the row with cand 2 
            # cand 2 is the pivot
            foundXYWing = True
            
            # get the number that is to be removed from all intersections of cand 1 and 3
            x = (set(Board[r1][c1]) & set(Board[r3][c3])).pop()
            
            # get cols of block of cand 3
            for c in range(0,3):
                startCol3 = c * 3 
                endCol3 = startCol3 + 3
                if c3 < endCol3:
                    break

            #            
            # remove x from all intersections of cand 2 and 3
            #
            for c in range(startCol3,endCol3):
            
                if type(Board[r1][c]) is list:
                    old = deepcopy(Board[r1][c])
                    try:
                        Board[r1][c].remove(x)
                    except ValueError as e:
                        # that's ok
                        pass
                    else: 
                        modifiedBoard = True
                        if XYWING:
                            print('     findXYWingBlock: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                            print('                      ({},{}): {} -> {}'.format(r1,c,old,Board[r1][c]))                                                                

            for c in range(startCol,endCol):
            
                if c != c1 and type(Board[r2][c]) is list:
                    old = deepcopy(Board[r2][c])
                    try:
                        Board[r2][c].remove(x)
                    except ValueError as e:
                        # that's ok
                        pass
                    else: 
                        modifiedBoard = True
                        if XYWING:
                            print('     findXYWingBlock: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                            print('                      ({},{}): {} -> {}'.format(r2,c,old,Board[r2][c]))                                                                


        elif c3 == c2:
            # cand 3 shares the column with cand 2 
            # cand 2 is the pivot
            foundXYWing = True

            # get the number that is to be removed from all intersections of cand 2 and 3
            x = (set(Board[r1][c1]) & set(Board[r3][c3])).pop()
            
            # get rows of block of cand 3
            for r in range(0,3):
                startRow3 = r * 3 
                endRow3 = startRow3 + 3
                if r3 < endRow3:
                    break

            #            
            # remove x from all intersections of cand 2 and 3
            #
            for r in range(startRow3,endRow3):
            
                if type(Board[r][c1]) is list:
                    old = deepcopy(Board[r][c1])                    
                    try:
                        Board[r][c1].remove(x)
                    except ValueError as e:
                        # that's ok
                        pass
                    else: 
                        modifiedBoard = True
                        if XYWING:
                            print('     findXYWingBlock: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                            print('                      ({},{}): {} -> {}'.format(r,c1,old,Board[r][c1]))                                                                

            for r in range(startRow,endRow):
            
                if r != r2 and type(Board[r][c2]) is list:
                    old = deepcopy(Board[r][c2])
                    try:
                        Board[r][c2].remove(x)
                    except ValueError as e:
                        # that's ok
                        pass
                    else: 
                        modifiedBoard = True
                        if XYWING:
                            print('     findXYWingBlock: ({},{}) , ({},{}) , ({},{}))'.format(r1,c1,r2,c2,r3,c3))                                                                                       
                            print('                      ({},{}): {} -> {}'.format(r,c2,old,Board[r][c2]))                                                                




    return Board, foundXYWing, modifiedBoard



def findConjugatePairs(Board):
    """ check if board contains conjugate pairs of digits pattern
    """
    

    for r in range(0,3):
        startRow = r * 3 
        endRow = startRow + 3
       
        for c in range(0,3):
            startCol = c * 3 
            endCol = startCol + 3 

            candidates = []                
            for r1 in range(startRow,endRow):
                for c1 in range(startCol,endCol):
 
                    if type(Board[r1][c1]) is list:                
                        candidates.extend(Board[r1][c1])

            # count frequency of candidates
            candidateDict = dict((i, candidates.count(i)) for i in candidates)   
            
            for digit, count in candidateDict.items():
                if count == 2:
                    print('     findConjugatePairs: digit {} in block {},{}'.format(digit,r,c))                                                                                                               

    return Board



def transposeBoard(Board):
    """ transpose the board
    """

    tempBoard = deepcopy(Board)  
    
    TransposedBoard = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]        
        
    # transpose rows to columns
    for r in range(9):
        for c in range(9):
            TransposedBoard[c][r] = tempBoard[r][c]
                                
    return TransposedBoard



def solveSudoku(Board, recursion, fallBack):
    """ recurse till solved
    """
    
    newBoard = deepcopy(Board)
    
    for r in range(9):
        for c in range(9):
            if type(newBoard[r][c]) is list and newBoard[r][c] != []:
                next = deepcopy(newBoard[r][c])
                value = next[0]
                next.remove(value)
                safeBoard = deepcopy(newBoard)
                safeBoard[r][c] = deepcopy(next)   # may be []  !!!
                fallBack.insert(0, safeBoard)


                loop = True
                while loop:
                    loop = False
                    
                    # hypothesis
                    newBoard[r][c] = value 
                    if TRACE:
                        print('{}recursion: trying ({},{}) = {}'.format(recursion*' ',r,c,value))                               
    
                    try:    
                        retCode =''
                        
                        magicIterations = 50  
                        i = 0
                        runLoop = True
                        while i < magicIterations and retCode != 'SOLVED' and runLoop:  
                            i+=1
                            BoardStart = deepcopy(newBoard)
                            newBoard = removeInvalidCandidates(newBoard)
                            retCode = validateBoard(newBoard)                        
                            newBoard = findHiddenSingles(newBoard)       
                            retCode = validateBoard(newBoard)
                            newBoard = findNakedSingles(newBoard)
                            retCode = validateBoard(newBoard) 
                            newBoard = findNakedPairs(newBoard)
                            retCode = validateBoard(newBoard)  
                            newBoard = excludeLockedCandidates1(newBoard)
                            retCode = validateBoard(newBoard)                            
                            newBoard = excludeLockedCandidates2(newBoard)
                            retCode = validateBoard(newBoard)
                            newBoard = findHiddenPairs(newBoard)
                            retCode = validateBoard(newBoard)
                            newBoard = findNakedTriples(newBoard)
                            retCode = validateBoard(newBoard)                            
                            newBoard = findNakedQuadruples(newBoard)
                            retCode = validateBoard(newBoard) 
                            newBoard = findHiddenTriples(newBoard)
                            retCode = validateBoard(newBoard)
                            newBoard = findHiddenQuadruples(newBoard)
                            retCode = validateBoard(newBoard) 
                            newBoard = findXWing(newBoard)        
                            retCode = validateBoard(newBoard) 
                            newBoard = findSwordfish(newBoard)  
                            retCode = validateBoard(newBoard) 
                            newBoard = findXYWing(newBoard)
                            retCode = validateBoard(newBoard)                            
                            newBoard = findJellyfish(newBoard)
                            retCode = validateBoard(newBoard)  
                            if BoardStart == newBoard:
                                runLoop = False  
                    except EmptyCellException as e:
                        retCode = 'INVALID'
                    
                    if retCode == 'SOLVED':
                        loop = False                        
                        return newBoard, recursion
                    elif retCode == 'VALID':
                        loop = False
                        newBoard, recursion = solveSudoku(newBoard, recursion+1, fallBack)
                    elif retCode == 'INVALID':

                        if len(next) == 0:
                            # that's the dead end for this level of recursion -> need to roll back
                            if TRACE:
                                print('{}recursion exhausted: no more candidates left for cell ({},{}) need to roll back'.format(recursion*' ',r,c))
                                printBoard(newBoard, 'roll back required', recursion)
                            if len(fallBack) > 1:
                                del fallBack[0]
                                newBoard = fallBack.pop(0)
                                newBoard, recursion = solveSudoku(newBoard, recursion-1, fallBack)                            
                            loop = False 
                        else:
                            # restore board, select next candidate, retry
                            newBoard = deepcopy(Board)
                            value = next[0]
                            next.remove(value)
                            #if TRACE:
                            #   print('{}recursion: next candidate'.format(recursion*' '))
                            loop = True

                
    return newBoard, recursion                   

                    
                    
class EmptyCellException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class NonUniqueValueException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class AsymmetricBoardException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)



def printBoard(Board, Title, blanks):
    print()
    print('{}{}'.format(blanks*' ',Title))
    for r in range(9):
        print('{}{}'.format(blanks*' ',Board[r]))
    print()
        


def printTestBoard(Board, Title, blanks):
    testBoard = deepcopy(Board)
    for r in range(9):
        for c in range(9):
            if type(testBoard[r][c]) is list or testBoard[r][c] == 0:
                testBoard[r][c] = '-'

    print()
    print('{}{}'.format(blanks*' ',Title))
    print('{}{}'.format(blanks*' ','+-----+-----+-----+'))
    for r in range(0,3):
        print('{}|{} {} {}|{} {} {}|{} {} {}|'.format(blanks*' ',testBoard[r][0],testBoard[r][1],testBoard[r][2],testBoard[r][3],testBoard[r][4],testBoard[r][5],testBoard[r][6],testBoard[r][7],testBoard[r][8]))   
    print('+-----+-----+-----+')
    for r in range(3,6):
        print('{}|{} {} {}|{} {} {}|{} {} {}|'.format(blanks*' ',testBoard[r][0],testBoard[r][1],testBoard[r][2],testBoard[r][3],testBoard[r][4],testBoard[r][5],testBoard[r][6],testBoard[r][7],testBoard[r][8]))   
    print('+-----+-----+-----+')
    for r in range(6,9):
        print('{}|{} {} {}|{} {} {}|{} {} {}|'.format(blanks*' ',testBoard[r][0],testBoard[r][1],testBoard[r][2],testBoard[r][3],testBoard[r][4],testBoard[r][5],testBoard[r][6],testBoard[r][7],testBoard[r][8]))   
    print('{}{}'.format(blanks*' ','+-----+-----+-----+'))
    print()    
    


def usage(name, availableSudokus):
    print()
    print('usage:')
    print('{} <input|filename|number|usage>  [trace traceall traceCC traceHS traceNS traceHP traceNP traceHT tracNT traceHQ traceNQ traceLC1 traceLC2 traceXW traceSF traceXY traceJF]'.format(name))
    print('    <input>      will enable you to enter the Sudoku at the command line')
    print('    <filename>   the filename of an stored Sudoku')
    print('    <number>     the number (<{}) of the internally stored Sudoku to be solved'.format(availableSudokus+1))
    print('    <trace>      will write a basic trace' )
    print('    <traceall>   will write a verbose trace' )
    print('    <traceCC>' )  
    print('    ...' ) 
    print('    <traceJF>    will trace the specified algorithm' )       
    print('    <usage>      this message')    
    print()
    return
    
    
               
def main(): 
    """ try to solve a Sudoku by applying simple criteria:
          - NakedSingles
          - HiddenSingles
          - NakedPairs
          - HiddenPairs
          - Naked Triples
          - Hidden Triples          
          - Naked Quadruples 
          - Hidden Quadruples
          - LockedCandidates 
          - X-Wing 
          - Swordfish
          - X-Y-Wing 
          - Jellyfish                   
    """
 
    
    readInput = False
    fileName = ''
    availableSudokus = 6
    solveSudokuNo = availableSudokus
    
    global TRACE, CHECKCELL,                                                \
           HIDDENSINGLES, NAKEDSINGLES, NAKEDPAIRS, HIDDENPAIRS,            \
           NAKEDTRIPLES, NAKEDQUADRUPLES, HIDDENTRIPLES, HIDDENQUADRUPLES,  \
           LOCKEDCANDIDATES1, LOCKEDCANDIDATES2, XWING, SWORDFISH, XYWING,  \
           JELLYFISH
    
    #**********************************************
    # parse arguments passed:

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == 'usage':
                usage(sys.argv[0], availableSudokus)
                return
            elif arg == 'input':
                # read initial Board from stdin
                readInput = True              
            elif arg == 'trace':
                # basic tracing
                TRACE = True 
            elif arg == 'traceall':
                # trace switches 
                TRACE = True                     
                CHECKCELL = True
                HIDDENSINGLES = True
                NAKEDSINGLES = True
                NAKEDPAIRS = True  
                LOCKEDCANDIDATES1 = True
                LOCKEDCANDIDATES2 = True
                HIDDENPAIRS = True
                NAKEDTRIPLES = True
                NAKEDQUADRUPLES = True
                HIDDENTRIPLES = True
                HIDDENQUADRUPLES = True
                XWING = True
                SWORDFISH = True   
                XYWING = True 
                JELLYFISH = True
            elif arg == 'traceCC': 
                # trace switch     
                CHECKCELL = True
            elif arg == 'traceHS':
                # trace switch     
                HIDDENSINGLES = True
            elif arg == 'traceNS':
                # trace switch     
                NAKEDSINGLES = True
            elif arg == 'traceHP':
                # trace switch     
                HIDDENPAIRS = True
            elif arg == 'traceNP':
                # trace switch     
                NAKEDPAIRS = True
            elif arg == 'traceHT':
                # trace switch     
                HIDDENTRIPLES = True
            elif arg == 'traceNT':
                # trace switch     
                NAKEDTRIPLES = True
            elif arg == 'traceHQ':
                # trace switch     
                HIDDENQUADRUPLES = True
            elif arg == 'traceNQ':
                # trace switch     
                NAKEDQUADRUPLES = True    
            elif arg == 'traceLC1':
                # trace switch     
                LOCKEDCANDIDATES1 = True  
            elif arg == 'traceLC2':
                # trace switch     
                LOCKEDCANDIDATES2 = True                      
            elif arg == 'traceXW':
                # trace switch     
                XWING = True 
            elif arg == 'traceSF':
                # trace switch                
                SWORDFISH = True 
            elif arg == 'traceXY':
                # trace switch     
                XYWING = True                 
            elif arg == 'traceJF':
                # trace switch     
                JELLYFISH = True  
            else:
                # expect either an ordinal number of an internally stored Sudoku
                # or a filename of a stored Sudoku
                readInput = False

                try:
                    # did we get an ordinal number of an internally stored Sudoku?
                    solveSudokuNo = int(arg)
                    if solveSudokuNo not in range(1, availableSudokus+1):
                        print()
                        print('Invalid Sudoku number entered: {}'.format(solveSudokuNo))
                        usage(sys.argv[0], availableSudokus)
                        return                                
                except ValueError as e:
                    # did we get a filename of a stored Sudoku?
                    fileName = arg           
                    if not os.path.exists(fileName):
                        print()
                        print('Invalid argument passed: {}'.format(arg))
                        usage(sys.argv[0], availableSudokus)
                        return                        
    else:
        usage(sys.argv[0], availableSudokus)
        return

        
    #********************************************** 
    
    
    try:
        Board = initBoard(readInput, solveSudokuNo, fileName)               
        Board = removeInvalidCandidates(Board)       
        retCode = validateBoard(Board)
        print('The initial Board is: ', retCode) 

        magicIterations = 50  
        i = 0        
        runLoop = True
        while i < magicIterations and retCode != 'SOLVED' and runLoop:  
            i+=1
            BoardStart = deepcopy(Board)
            Board = findHiddenSingles(Board)       
            retCode = validateBoard(Board)
            Board = findNakedSingles(Board)
            retCode = validateBoard(Board) 
            Board = findNakedPairs(Board)
            retCode = validateBoard(Board) 
            Board = excludeLockedCandidates1(Board)
            retCode = validateBoard(Board)            
            Board = excludeLockedCandidates2(Board)
            retCode = validateBoard(Board)
            Board = findHiddenPairs(Board)
            retCode = validateBoard(Board)
            Board = findNakedTriples(Board)
            retCode = validateBoard(Board)
            Board = findNakedQuadruples(Board)
            retCode = validateBoard(Board) 
            Board = findHiddenTriples(Board)
            retCode = validateBoard(Board) 
            Board = findHiddenQuadruples(Board)
            retCode = validateBoard(Board)   
            Board = findXWing(Board)        
            retCode = validateBoard(Board) 
            Board = findSwordfish(Board)  
            retCode = validateBoard(Board) 
            Board = findXYWing(Board)
            retCode = validateBoard(Board)             
            Board = findJellyfish(Board)
            retCode = validateBoard(Board)
            if BoardStart == Board:
                runLoop = False    
        if TRACE:
            print()
            print('NS / HS / NP / LC / HP / NT / NQ / HT / HQ / XW / SF / XY / JF iterations: ', i)  
            print('Board is: ', retCode)

        
        # tests:  http://hodoku.sourceforge.net/en/techniques.php 
        
        #printTestBoard(Board, 'before conjugate pairs', 0) 
        #printBoard(Board, 'before conjugate pairs', 0) 
        #Board = findConjugatePairs(Board)
        #printBoard(Board, 'after conjugate pairs', 0)              
        #retCode = validateBoard(Board)       
        
        
        if retCode != 'SOLVED':  
            if TRACE:
                printTestBoard(Board, 'Board after NS / HS / NP / LC / HP / NT / NQ / HT / HQ / XW / SF / XY / JF iterations', 0) 
                printBoard(Board, 'Board after NS / HS / NP / LC / HP / NT / NQ / HT / HQ / XW / SF / XY / JF iterations', 0) 
    
            recursion = 0; fallBack = []        
            Board, recursion = solveSudoku(Board, recursion, fallBack)
            retCode = validateBoard(Board)
            if TRACE:
                print()
                print('After running a brute force algorithm the Board is: {}'.format(retCode))
        
    except Exception as e:
        traceback.print_exc()         
    else: 
        printTestBoard(Board, retCode, 0)
        
        if retCode != 'SOLVED':
            printBoard(Board, retCode, 0)
           

if __name__ == '__main__':    
    main() 