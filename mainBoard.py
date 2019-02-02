# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 21:06:02 2019

@author: User
"""
import chess
# chess type
GENERAL = 1
ADVISOR = 2
ELEPHANT = 3
HORSE = 4
CHARIOT = 5
CANNON = 6
SOLDIER = 7

class mainBoard:
    def __init__(self,):
        self.board = [0] * 90 # board 9 x 10 width x height / 90 in size
        self.curSide = 1
        
        self.names = {1 : 'general', 2: 'advisor', 3: 'elephant', 4: 'horse', 5: 'chariot', 6: 'cannon', 7: 'soldier'}
        
    def startGame(self,):
        self.side0 = []
        self.side1 = []
        self.setup()
        
    def setup(self, ):
        for i in range(4):
            for j in range(5):
                if i == 0:
                    pos = {0 : CHARIOT, 1: HORSE, 2: ELEPHANT, 3: ADVISOR, 4: GENERAL}
                elif i == 2:
                    pos = {1 : CANNON}
                elif i == 3:
                    pos = {0: SOLDIER, 2: SOLDIER, 4: SOLDIER}
                else:
                    pos = {0:0}
                try:
                    p = pos[j]
                except:
                    p = 0
#                print (p)
                # side == 0 indicate top side
                # else bottom side
                side = 0
                
                if p != 0:
                    self.board[i * 9 + j] = chess.chess(side, p, [i, j])
                    self.board[i * 9 + 8 - j] = chess.chess(side, p, [i, 8-j])
                    
                    self.side0.append(self.board[i * 9 + j])
                    if i * 9 + j != i * 9 + 8 -  j:
                        self.side0.append(self.board[i * 9 + 8 - j])
                        
                    side = 1
                    self.board[(9-i) * 9 + j] = chess.chess(side, p, [9-i, j])
                    self.board[(9-i) * 9 + 8 - j] = chess.chess(side, p, [9 - i, 8 - j])
                    
                    self.side1.append(self.board[(9-i) * 9 + j])
                    if (9-i) * 9 + 8 - j != (9-i) * 9 + j:
                        self.side1.append(self.board[(9-i) * 9 + 8 - j])
                        
                    if (i == 0 or i == 9) and j == 4:
                        self.general0 = self.board[4]
                        self.general1 = self.board[9 * 9 + 4]
                else:
                    self.board[i * 9 + j] = 0
#                print('[{0}, {1}] , [{0}, {2}], [{3}, {1}], [{3}, {2}]'.format(i, j, 8 - j, (9-i)))
                
    def printBoard(self, board):
        for i in range(10):
            pos = []
            for j in range(9):
                temp = board[i * 9 + j]
                if type(temp) is chess.chess:
                    pos.append(temp.name)
                else:
                    pos.append('_')
            print(pos)
            
    def nextPlayer(self,):
        self.curSide ^= 1
        if self.curSide == 0:
            dic = self.getMoves()
            for k, vs in dic.items():
                for v in vs:
                    sen = k + ': [{}, {}] --> [{}, {}]'.format(v[0], v[1], v[2], v[3])
                    print(sen)
#                    self.addLog(sen + '\n')
    
    def move(self, old_i, old_j, new_i, new_j, show):
        return self.moveIn(old_i, old_j, new_i, new_j, self.board, show)
    
    # for simulation
    def moveExt(self, old_i, old_j, new_i, new_j, board):
        temp1 = board[old_i * 9 + old_j]
        board[new_i * 9 + new_j] = temp1
        board[old_i * 9 + old_j] = 0
        
        return board
        
    # move from old position to new position
    # check if chosen piece is valid
    def moveIn(self, old_i, old_j, new_i, new_j, board, show):
#        print('ori_pos:', old_i, old_j, 'new_pos:', new_i, new_j)
        
        temp1 = board[old_i * 9 + old_j]
        temp2 = board[new_i * 9 + new_j]
        #validation
        valid = self.valid(old_i, new_i, old_j, new_j, board, show)
        if valid:
            board[old_i * 9 + old_j] = 0
            board[new_i * 9 + new_j] = temp1
            temp1.move([new_i, new_j])
            
            sen = self.names[temp1.type].upper() + ' [{}, {}] --> [{}, {}]'.format(old_i, old_j, new_i, new_j)
            print(sen)
            self.addLog(sen + '\n')
            
            
            if type(temp2) is chess.chess:
                temp2.captured = True
                if temp2.side == 1:
                    self.side1.remove(temp2)
                else:
                    self.side0.remove(temp2)
                
                sen = 'captured '+ self.names[temp2.type].upper()
                self.addLog(sen + '\n')
                print(sen)
                
            self.nextPlayer()
            return True, temp2
        else:
#            print('invalid')
#            print('reasons are wait to be implemented')
            return False, temp2
    
    def valid(self, old_i, new_i, old_j, new_j, board, show = False):
        temp1 = board[old_i * 9 + old_j]
#        temp2 = self.board[new_i * 9 + new_j]
        if temp1.side != self.curSide:
            if show:
                self.addLog('not your turn\n')
                print('not your turn')
            return False
        if type(temp1) is not chess.chess:
            if show:
                self.addLog('sleected empty piece\n')
                print('selected empty piece')
            return False
        if old_i == new_i and old_j == new_j:
            if show:
                self.addLog('select a new position\n')
                print('select a new position')
            return False
        if new_i < 0 or new_i > 9 or new_j < 0 or new_j > 8:
            if show:
                self.addLog('out of bounds')
                print('out of bounds')
            return False
#        print(temp1.name, temp1.position)
        return self.typeCheck(temp1, old_i, old_j, new_i, new_j, board, show)
        
    def typeCheck(self, chessO, old_i, old_j, new_i, new_j, board, show = False):
        temp2 = board[new_i * 9 + new_j]
#        print(chessO.name, chessO.type, CANNON)
        if type(temp2) is chess.chess and temp2.side == chessO.side:
            if show:
                self.addLog('contains ally piece\n')
                print('contains ally piece')
            return False
        
        if chessO.type == SOLDIER:
            return self.SoldierCheck(chessO, old_i, new_i, old_j, new_j, board, show)
        elif chessO.type == CANNON or chessO.type == CHARIOT:
#            print('type of cannon or chariot')
            return self.CannonOChariotCheck(old_i, new_i, old_j, new_j, chessO.type, board, show)
        elif chessO.type == ELEPHANT:
#            print('ELEPHANT piece')
            return self.ElephantCheck(old_i, new_i, old_j, new_j, board, show)
        elif chessO.type == ADVISOR or chessO.type == GENERAL:
            if chessO.type == GENERAL and self.isFlyingGeneral(board):
                if show:
                    self.addLog('flying general\n')
                    print('flying general')
                return True
            return self.AdvisorOrGeneralCheck(old_i, new_i, old_j, new_j, chessO.type, board, show)
        elif chessO.type == HORSE:
            return self.HorseCheck(old_i, new_i, old_j, new_j, board)
        
        return True
    
    def SoldierCheck(self, chessO, old_i, new_i, old_j, new_j, board, show = False):
        if abs(old_i - new_i) + abs(old_j - new_j) != 1:
            if show:
                self.addLog('soldier moved more than 1 position\n')
                print('soldier moved more than 1 position')
            return False
        if not chessO.crossedRiver() and abs(old_j - new_j) > 0:
            if show:
                self.addLog('have not crossed river, cannot move horizontally\n')
                print('have not crossed river, cannot move horizontally')
            return False
        if (chessO.side == 0 and new_i - old_i < 0) or (chessO.side == 1 and old_i - new_i < 0):
            if show:
                self.addLog('soldiers cannot move backward\n')
                print('soldiers cannot move backward')
            return False
        return True
    
    def CannonOChariotCheck(self, row_start, row_end, col_start, col_end, Ctype, board, show = False):
        count = 0
        temp2 = board[row_end * 9 + col_end]
        
#        print('ori_pos:', row_start, col_start, 'new_pos:', row_end, col_end)
#        print(temp2.name)
        if col_start == col_end:
            length = row_start - row_end
        elif row_start == row_end:
            length = col_start - col_end
        else:
            if show:
                self.addLog('cannon can only move in 1 directon, horizontally or vertically\n')
                print('cannon can only move in 1 directon, horizontally or vertically')
            return False
        
        for i in range(abs(length)):
            if col_start == col_end:
#                print('move vertically length:', length)
                
                r = row_start + i + 1
                if row_start > row_end:
                    r = row_start - i - 1
                pos = r * 9 + col_start
            else:
#                print('move horizontially length:', length)
                c = col_start + 1 + i
                if col_start > col_end:
                    c = col_start - 1 - i
                pos = row_start * 9 + c
            temp = board[pos]
#            print(temp)
            if type(temp) is chess.chess:
                count += 1
                
        if type(temp2) is chess.chess:
            if Ctype == CANNON and count != 2:
                if count == 1:
                    if show:
                        self.addLog('this piece cannot be captured, no platform / screen between cannon and the piece\n')
                        print('this piece cannot be captured, no platform / screen between cannon and the piece')
                elif count > 2:
                    if show:
                        self.addLog('there is more than 1 piece between cannon and the destination\n')
                        print('there is more than 1 piece between cannon and the destination')
                return False
            elif Ctype == CHARIOT and count != 1:
                
                if show:
                    self.addLog('there piece(s) in the path to the destination\n')
                    print('there piece(s) in the path to the destination')
                return False
        elif temp2 == 0 and count != 0:
            if show:
                self.addLog('there piece(s) in the path to the destination\n')
                print('there piece(s) in the path to the destination')
            return False
        
        return True
    
    def ElephantCheck(self, row_start, row_end, col_start, col_end, board, show = False):
        temp_old = board[row_start * 9 + col_start]
        if abs(row_start - row_end) != 2 and abs(col_start - col_end) != 2:
            if show:
                self.addLog('not moving as field 田\n')
                print('not moving as field 田')
            return False
        
        mid_i = int((row_start + row_end)/2)
        mid_j = int((col_start + col_end)/2)
        temp = board[mid_i * 9 + mid_j]
        if type(temp) is not chess.chess and temp != 0:
            if show:
                self.addLog('blocking the elephant\'s eye\n')
                print('blocking the elephant\'s eye')
            return False
        
        if (temp_old.side == 0 and row_end > 4) or (temp_old.side == 1 and row_end < 5):
            if show:
                self.addLog('cannot cross the river\n')
                print('cannot cross the river')
            return False
        
        return True
    
    def AdvisorOrGeneralCheck(self, row_start, row_end, col_start, col_end, Ctype, board, show = False):
        piece = board[row_start * 9 + col_start]
            
        if abs(row_start - row_end) > 1 or abs(col_start - col_end) > 1:
            if show:
                self.addLog('cannot move more than 1 space\n')
                print('cannot move more than 1 space')
            return False
#        print('[%d, %d] --> [%d, %d]' % (row_start, col_start, row_end, col_end))
        if col_end > 5 or col_end < 3 or (piece.side == 0 and row_end > 3) or (piece.side == 1 and row_end < 7):
            
            if show:
                self.addLog('cannot leave the palace\n')
                print('cannot leave the palace')
            return False
        if Ctype == ADVISOR:
            if abs(row_start - row_end) + abs(col_start - col_end) == 1:
                if show:
                    self.addLog('advisor should be moved diagonally\n')
                    print('advisor should be moved diagonally')
                return False
        elif Ctype == GENERAL:
            if abs(row_start - row_end) == 1 and abs(col_start - col_end) == 1:
                if show:
                    self.addLog('cannot move diagonally\n')
                    print('cannot move diagonally')
                return False
        return True
    
    def HorseCheck(self, row_start, row_end, col_start, col_end, board, show = False):
#        print('checking Horse piece')
        row_len = row_start - row_end
        col_len = col_start - col_end
        
#        print('ori_pos:', row_start, col_start, 'new_pos:', row_end, col_end)
        
        if abs(row_len) + abs(col_len) != 3:
            if show:
                self.addLog('not moving as 日\n')
                print('not moving as 日')
            return False
        
        if abs(col_len) == 2:
            i = -1 if col_len > 0 else 1
            temp = board[row_start * 9 + col_start + i]
        elif abs(row_len) == 2:
            i = -1 if row_len > 0 else 1
            temp = board[(row_start + i) * 9 + col_start]
        if type(temp) is chess.chess:
            if show:
                self.addLog('hobbling the horse\'s leg\n')
                print('hobbling the horse\'s leg')
            return False
        
#        print('horse passed')
        return True
        
    def isFlyingGeneral(self, board):
        x0 = self.general0.position[0]
        x1 = self.general1.position[0]
        y0 = self.general0.position[1]
        y1 = self.general1.position[1]
        
        if y0 == y1:
            for i in range(x1 - x0 - 1):
                index = i + x0
                p = board[index * 9 + y0]
                if type(p) is chess.chess:
                    return False
            return True
        else:
            return False
        
    def getMoves(self,):
        side = self.curSide
        return self.getMovesSide(side, self.board)
        
    def getMovesSide(self, side, board):
        result = {'G':[], 'A':[], 'E': [], 'H': [], 'R': [], 'C': [], 'S': []}
        
#        print()
#        print('Get current board moves: ')
#        self.printBoard(board)
            
        for p in board:
            if type(p) is chess.chess:
                ori_pos_x = int(board.index(p) / 9) 
                ori_pos_y = board.index(p) % 9
                if p.type == SOLDIER:
                    if self.valid(ori_pos_x, ori_pos_x + 1, ori_pos_y, ori_pos_y, board):
                        result['S'].append([ori_pos_x, ori_pos_y, ori_pos_x + 1, ori_pos_y])
                        
                    if self.valid(ori_pos_x, ori_pos_x - 1, ori_pos_y, ori_pos_y, board):
                        result['S'].append([ori_pos_x, ori_pos_y, ori_pos_x - 1, ori_pos_y])
                        
                    if self.valid(ori_pos_x, ori_pos_x, ori_pos_y, ori_pos_y + 1, board):
                        result['S'].append([ori_pos_x, ori_pos_y, ori_pos_x, ori_pos_y + 1])
                        
                    if self.valid(ori_pos_x, ori_pos_x, ori_pos_y, ori_pos_y - 1, board):
                        result['S'].append([ori_pos_x, ori_pos_y, ori_pos_x, ori_pos_y - 1])
                    
                elif p.type == CANNON or p.type == CHARIOT:
                    count = 0
                    x1, y1 = [ori_pos_x, ori_pos_y]
                    x2, y2 = [ori_pos_x, ori_pos_y]
                    while count < 4:
                        x1 -= 1
                        y1 -= 1
                        x2 += 1
                        y2 += 1
                        if x1 >= 0 and self.valid(ori_pos_x, x1, ori_pos_y, ori_pos_y, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, x1, ori_pos_y])
                        elif x1 == -1:
                            count += 1
                            
                        if y1 >= 0 and self.valid(ori_pos_x, ori_pos_x, ori_pos_y, y1, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x, y1])
                        elif y1 == -1:
                            count += 1    
                            
                        if x2 <= 9 and self.valid(ori_pos_x, x2, ori_pos_y, ori_pos_y, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, x2, ori_pos_y])
                        elif x2 == 10:
                            count += 1
                            
                        if y2 <= 8 and self.valid(ori_pos_x, ori_pos_x, ori_pos_y, y2, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x, y2])
                        elif y2 == 9:
                            count += 1
                        
                elif p.type == ELEPHANT:
                    xT = ori_pos_x - 2
                    xB = ori_pos_x + 2
                    yL = ori_pos_y - 2
                    yR = ori_pos_y + 2
                    if xB <= 9 and yR <= 8 and self.valid(ori_pos_x, xB, ori_pos_y, yR, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, xB, yR])
                        
                    if xB <= 9 and yL > -1 and self.valid(ori_pos_x, xB, ori_pos_y, yL, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, xB, yL])
                        
                    if xT > -1 and yR <= 8 and self.valid(ori_pos_x, xT, ori_pos_y, yR, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, xT, yR])
                        
                    if xT > -1 and yL > -1 and self.valid(ori_pos_x, xT, ori_pos_y, yL, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, xT, yL])
                
                elif p.type == HORSE:
                    if ori_pos_x - 1 > -1 and  ori_pos_y - 2 > -1 and self.valid(ori_pos_x, ori_pos_x - 1, ori_pos_y, ori_pos_y - 2, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x - 1, ori_pos_y - 2])
                        
                    if ori_pos_x + 1 < 10 and ori_pos_y - 2 > -1 and self.valid(ori_pos_x, ori_pos_x + 1, ori_pos_y, ori_pos_y - 2, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x + 1, ori_pos_y - 2])
                        
                    if ori_pos_x - 1 > -1 and ori_pos_y + 2 < 9 and self.valid(ori_pos_x, ori_pos_x - 1, ori_pos_y, ori_pos_y + 2, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x - 1, ori_pos_y + 2])
                        
                    if ori_pos_x + 1 < 10 and ori_pos_y + 2 < 9 and self.valid(ori_pos_x, ori_pos_x + 1, ori_pos_y, ori_pos_y + 2, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x + 1, ori_pos_y + 2])
                        
                    if ori_pos_x - 2 > -1 and ori_pos_y - 1 > -1 and self.valid(ori_pos_x, ori_pos_x - 2, ori_pos_y, ori_pos_y - 1, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x - 2, ori_pos_y - 1])
                        
                    if ori_pos_x - 2 > -1 and ori_pos_y + 1 < 9 and self.valid(ori_pos_x, ori_pos_x - 2, ori_pos_y, ori_pos_y + 1, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x - 2, ori_pos_y + 1])
                    
                    if ori_pos_x + 2 < 10 and ori_pos_y - 1 > -1 and self.valid(ori_pos_x, ori_pos_x + 2, ori_pos_y, ori_pos_y - 1, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x + 2, ori_pos_y - 1])
                        
                    if ori_pos_x + 2 < 10 and ori_pos_y + 1 < 9 and self.valid(ori_pos_x, ori_pos_x + 2, ori_pos_y, ori_pos_y + 1, board):
                        result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x + 2, ori_pos_y + 1])
                
                elif p.type == ADVISOR or p.type == GENERAL:
                    xT = ori_pos_x - 1
                    xB = ori_pos_x + 1
                    yL = ori_pos_y - 1
                    yR = ori_pos_y + 1
                    if p.type == GENERAL:
                        if self.isFlyingGeneral(board):
                            opponent = 0 if ori_pos_x == 9 else 9
                            result[p.name].append([ori_pos_x, ori_pos_y, opponent, ori_pos_y])
                        
                        if xT > -1 and self.valid(ori_pos_x, xT, ori_pos_y, ori_pos_y, board):
                            
                            result[p.name].append([ori_pos_x, ori_pos_y, xT, ori_pos_y])
                            
                        if xB <= 9 and self.valid(ori_pos_x, xB, ori_pos_y, ori_pos_y, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, xB, ori_pos_y])
                            
                        if yR <= 8 and self.valid(ori_pos_x, ori_pos_x, ori_pos_y, yR, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x, yR])
                            
                        if yL > -1 and self.valid(ori_pos_x, ori_pos_x, ori_pos_y, yL, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, ori_pos_x, yL])
                            
                    if p.type == ADVISOR:
                        if xT > -1 and yR < 8 and self.valid(ori_pos_x, xT, ori_pos_y, yR, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, xT, yR])
                            
                        if xB <= 9 and yL > -1 and self.valid(ori_pos_x, xB, ori_pos_y, yL, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, xB, yL])
                            
                        if xB <= 9 and yR <= 8 and self.valid(ori_pos_x, xB, ori_pos_y, yR, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, xB, yR])
                            
                        if xT > -1 and yL > -1 and self.valid(ori_pos_x, xT, ori_pos_y, yL, board):
                            result[p.name].append([ori_pos_x, ori_pos_y, xT, yL])
                
        return result
    
    def setLog(self, log):
        self.log = log
    
    def addLog(self, log):
        self.log.config(state = 'normal')
        self.log.insert('end', log)
        self.log.config(state = 'disabled')
        
#b = mainBoard()
#b.move(2, 1, 7, 1) # CANNON unit test 1: expect True tested True
#b.move(0, 3, 0, 2) # SOLDIER unit test 1 has not crossed river and move back: expect True tested True
#b.move(9, 2, 7, 0) # ELEPHANT unit test 1: expect True tested True
#b.printBoard()