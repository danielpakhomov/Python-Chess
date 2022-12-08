from ast import While
from cgi import test
from random import randint
from xml.etree.ElementTree import tostring
import chess
from numpy import *
from copy import deepcopy
import time
board = chess.Board()
root = 2
#MAIN PROBLEM RIGHT NOW: CHANGE THE FORMAT OF THE SQUARETOPIECE STRINGS SO THE LETTER IS LOWER CASE.
#this needs to be done
def is_quiet(is_white, boardPosition):
    for i in range(1,6):
    
        attackedPlayerSpaces=squareToPieces(boardPosition.pieces(i,chess.WHITE if is_white else chess.BLACK))
        for space in attackedPlayerSpaces:
            #print(chess.BLACK if is_white else chess.WHITE)
            
            #print(board.attackers(chess.BLACK if is_white else chess.WHITE, chess.parse_square(space)))
            if squareToPieces(boardPosition.attackers(chess.BLACK if is_white else chess.WHITE, chess.parse_square(space))):
                #print(False)
                return False
    #print(True)            
    return True
def quiescent_search(moveDepth, is_white, boardPosition, alpha, beta, moveNum):
    if is_quiet(is_white, boardPosition) or moveDepth == 0 or boardPosition.outcome():
        return calculateHeuristic(boardPosition, moveNum)
    else:
        if is_white:
            currentMaxMoveVal = -1000000
            for potential_state in boardPosition.legal_moves:
                testedWhiteState= deepcopy(boardPosition)
                testedWhiteState.push_san(str(potential_state))
                currentMoveVal = quiescent_search(moveDepth-1, False, testedWhiteState,alpha,beta, moveNum)
                
                if max(currentMaxMoveVal,currentMoveVal) > currentMaxMoveVal:
                    currentMaxMoveVal=max(currentMaxMoveVal,currentMoveVal)
                    
                alpha = max(alpha, currentMaxMoveVal)
                if beta <=alpha:
                    break
            
            return currentMaxMoveVal
        if not is_white:
            currentMinMoveVal = 1000000
            
            for potential_state in boardPosition.legal_moves:
                testedBlackState= deepcopy(boardPosition)
                testedBlackState.push_san(str(potential_state))
                currentMoveVal = quiescent_search(moveDepth-1, True, testedBlackState,alpha,beta, moveNum)
                if min(currentMinMoveVal,currentMoveVal) < currentMinMoveVal:
                    currentMinMoveVal=currentMoveVal
                    
                beta = min(beta, currentMinMoveVal)
                if beta<=alpha:
                    break
                
            
            return currentMinMoveVal
    


def minimax(moveDepth,is_white, boardPosition,alpha,beta, moveNum):
    if moveDepth == root:
        starttime = time.time()
    if boardPosition.outcome():
        return calculateHeuristic(boardPosition, moveNum)
    if moveDepth == 0:
        if is_quiet(is_white, boardPosition):
            return calculateHeuristic(boardPosition, moveNum)
        else:
            return quiescent_search(2, is_white, boardPosition, alpha, beta, moveNum)
            
    if is_white:
        currentMaxMoveVal = -1000000
        for potential_state in boardPosition.legal_moves:
            testedWhiteState= deepcopy(boardPosition)
            #print(potential_state)
            testedWhiteState.push_san(str(potential_state))
            currentMoveVal = minimax(moveDepth-1, False, testedWhiteState,alpha,beta, moveNum)
            #print(currentMoveVal, " ",currentMaxMoveVal)
            #if moveDepth==(root-2):
                #print("current val at root-2: ",currentMoveVal)
            if max(currentMaxMoveVal,currentMoveVal) > currentMaxMoveVal:
                currentMaxMoveVal=max(currentMaxMoveVal,currentMoveVal)
                currentBestMove=deepcopy(potential_state)
                #print(currentBestMove)
            alpha = max(alpha, currentMaxMoveVal)
            if beta <=alpha:
                break
            
        if moveDepth==root:
            print("Chosen Move: ",currentBestMove)
            print("Heuristic Output: ",currentMaxMoveVal)
            print("Time Spent on Processing: ",(time.time()-starttime))
            return currentBestMove
        
        return currentMaxMoveVal
    if not is_white:
        currentMinMoveVal = 1000000
        
        for potential_state in boardPosition.legal_moves:
            testedBlackState= deepcopy(boardPosition)
            testedBlackState.push_san(str(potential_state))
            currentMoveVal = minimax(moveDepth-1, True, testedBlackState,alpha,beta, moveNum)
            if min(currentMinMoveVal,currentMoveVal) < currentMinMoveVal:
                currentMinMoveVal=currentMoveVal
            
                currentBestMove=deepcopy(potential_state)
            #if moveDepth==(root-1):
                #print("current val at root-1: ",currentMoveVal)
            beta = min(beta, currentMinMoveVal)
            if beta<=alpha:
                break
        
        if moveDepth==root:
            print(currentBestMove)
            print("Heuristic Output: ", currentMinMoveVal)
            print("Time Spent on Processing: ",(time.time()-starttime))
            return currentBestMove
        return currentMinMoveVal

#takes in a square from attackers and returns all of the positions the attackers are in, in an array
def squareToPieces(square):
    count = 1
    res = []
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    for peice in square.tolist():
        if peice:
            if count != 64:
                tempStr = alphabet[(count - ((count//8)*8)) - 1] + str((count//8+1)) 
            else:
                tempStr = alphabet[(count - ((count//8)*8)) - 1] + str((count//8)) 

            res.append(tempStr)
        count+=1
    return(res)

#Adds up the material thats left for both sides. White gives positive values, black gives negative values
def addPiecesLeft(board):
    total = 0
    colours = [chess.WHITE, chess.BLACK]
    for c in range(0, 2):
        for i in range(1, 6):
            piecesLeft = len(squareToPieces(board.pieces(i, colours[c]))) #gives us the number of a given piece (i) that is left for a certain colour (colours[c])
            match i:
                #pawns
                case 1:
                    if (c == 0):
                        total += piecesLeft
                    else:
                        total -= piecesLeft
                #knights
                case 2:
                    if (c == 0):
                        total += piecesLeft*3
                    else:
                        total -= piecesLeft*3
                #bishops
                case 3:
                    if (c == 0):
                        total += piecesLeft*3
                    else:
                        total -= piecesLeft*3
                #rooks
                case 4:
                    if (c == 0):
                        total += piecesLeft*5
                    else:
                        total -= piecesLeft*5
                #queens
                case 5:
                    if (c == 0):
                        total += piecesLeft*9
                    else:
                        total -= piecesLeft*9
    return(total)

def punishSideKnights(board):
    score = 0
    edgeFiles = [chess.A1, chess.A2, chess.A3, chess.A4, chess.A5, chess.A6, chess.A7, chess.A8,
            chess.H1, chess.H2, chess.H3, chess.H4, chess.H5, chess.H6, chess.H7, chess.H8]

    for square in edgeFiles:
        if (board.piece_type_at(square) == 2):
            if (board.color_at(square)):
                score -= 2
            else:
                score += 2
    return(score)

def punishWhiteUnDeveloped(board, moveNum):
    undevelopedWhite = 0
    total = 0
    whiteKnights = [chess.B1, chess.G1]
    whiteBishops = [chess.C1, chess.F1]
    
    for wk in whiteKnights:
        if ((board.piece_type_at(wk) == 2) and (board.color_at(wk))):
            undevelopedWhite += 1
    
    for wb in whiteBishops:
        if ((board.piece_type_at(wb) == 3) and (board.color_at(wb))):
            undevelopedWhite += 1

    if (moveNum < 3):
        total -= 0
    elif(moveNum < 6):
        total -= undevelopedWhite
    else:
        total -= undevelopedWhite*2
    
    return(total)

def punishBlackUnDeveloped(board, moveNum):
    undevelopedBlack = 0
    total = 0
    blackKinghts = [chess.B8, chess.G8]
    blackBishops = [chess.C8, chess.F8]
    
    for bk in blackKinghts:
        if ((board.piece_type_at(bk) == 2) and (not board.color_at(bk))):
            undevelopedBlack += 1
    
    for bb in blackBishops:
        if ((board.piece_type_at(bb) == 3) and (not board.color_at(bb))):
            undevelopedBlack += 1

    if (moveNum < 3):
        total -= 0
    elif(moveNum < 6):
        total -= undevelopedBlack
    else:
        total -= undevelopedBlack*2
    
    return(total)

def canCastle(board, moveNum):
    if (moveNum > 12):
        return(0)
    total = 0
    if (board.has_kingside_castling_rights(chess.WHITE)):
        total += 1.5
    if (board.has_queenside_castling_rights(chess.WHITE)):
        total += 1.5

    if (board.has_kingside_castling_rights(chess.BLACK)):
        total -= 1.5
    if (board.has_queenside_castling_rights(chess.BLACK)):
        total -= 1.5
    return(total)

def calculatePawns(board, moveNum):
    whitePawnsAtStart = 0
    blackPawnsAtStart = 0
    total = 0

    squares = [chess.A2, chess.B2, chess.C2, chess.D2, chess.E2, chess.F2, chess.G2, chess.H2,
                chess.A7, chess.B7, chess.C7, chess.D7, chess.E7, chess.F7, chess.G7, chess.H7]
    for s in squares:
        if (board.piece_type_at(s) == 1):
            #True if White, False if Black
            if (board.color_at(s)):
                whitePawnsAtStart += 1
            else:
                blackPawnsAtStart += 1

    if (moveNum > 4):
        if (whitePawnsAtStart > 4):
            total -= 1.5
        if (blackPawnsAtStart > 4):
            total += 1.5
    elif (moveNum > 2):
        if (whitePawnsAtStart > 6):
            total -= 1.5
        if (blackPawnsAtStart > 6):
            total += 1.5
    
    return(total)

def calculateHeuristic(board, moveNum): 
    if (board.outcome() is not None):
        if (board.outcome().result() == "1-0"):
            return(10000)
        elif (board.outcome().result() == "0-1"):
            return(-10000)
    elif(board.is_stalemate()):
        return(0)

    total = addPiecesLeft(board)
    total += punishSideKnights(board)
    total += punishWhiteUnDeveloped(board, moveNum)
    total += punishBlackUnDeveloped(board, moveNum)
    total += canCastle(board, moveNum)
    total += calculatePawns(board, moveNum)
    return(total)

def whiteInCheckmate():

    board = chess.Board()
    board.push_san("f4")
    board.push_san("e6")
    board.push_san("g4")
    board.push_san("d8h4")
    return(board)

def blackInCheckmate():
    
    board = chess.Board()
    board.push_san("e4")
    board.push_san("e5")
    board.push_san("d1h5")
    board.push_san("b8c6")
    board.push_san("f1c4")
    board.push_san("g8f6")
    board.push_san("h5f7")
    return(board)

#picks random move
def generateMove(board):
    while(1):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        tempStr = letters[randint(0, 7)] + str(randint(1, 8))
        addedStr = letters[randint(0, 7)] + str(randint(1, 8))
        if addedStr!=tempStr: #avoiding null moves
            tempStr += addedStr
            if (chess.Move.from_uci(tempStr) in board.legal_moves):
                return(tempStr)
        else:
            continue
#this currently just uses random moves but we can sub this with a call to minimax and provide appropriate parameters(i.e which player is the ai)
board = chess.Board()
def playGame():
    moveNum = 0
    while(1):
        moveNum += 1
        game=minimax(root,True,board,-Infinity,Infinity, moveNum)
        if type(game) is int:
            if game>0:
                print("white wins!")
            elif game<0:
                print("black wins!")
            else:
                print("draw!")
            break
                
        
        board.push_san(str(game))
        print(board)
        playerMove = input("Enter Move: ")
        while chess.Move.from_uci(playerMove) not in board.legal_moves:
            print("Illegal move. Please enter a valid move. Legal moves are:", board.legal_moves)
            playerMove = input("Enter Move: ")
        board.push_san(playerMove)
        
        print(board)

playGame()



