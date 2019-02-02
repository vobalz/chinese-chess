# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 04:34:28 2019

@author: User
"""

from tkinter import *
import mainBoard, chess, Search
from PIL import Image, ImageTk

class DragDropMixin(Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.original_x = 0
        self.original_y = 0
        self.bind("<Button-1>", self.drag_start)
        self.bind("<B1-Motion>", self.drag_motion)
        self.bind('<ButtonRelease-1>', self.drag_end)
            
    def setPosition(self, position):
        self.position = position
        
    def addPoints(self, lists):
        self.allPoints = lists
        
    def setMove(self, move):
        self.move = move
    
    def setUITrigger(self, update):
        self.UItrigger = update
    
    def updateLocation(self, x, y):
        self.place(x = x - 40, y = y - 35)
        
    def drag_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.original_x = self.winfo_x()
        self.original_y = self.winfo_y()
        self.lift()
#        print(self.winfo_x(), self.winfo_y())
#        print('original position:', self.position, 'at corrdinate:', self.allPoints[self.position])
    
    def drag_motion(self, event):
        x = self.winfo_x() - self.drag_start_x + event.x
        y = self.winfo_y() - self.drag_start_y + event.y
        self.place(x=x, y=y)
        
    def drag_end(self, event):
        x = self.winfo_x()
        y = self.winfo_y()
#        print(y, x)
        
        start_ind = self.position
        if start_ind > 9:
            start_ind -= 10
                
        updated = False
        for i in range(90):
            index = (i + start_ind) % 90
            point_x, point_y = self.allPoints[index]
            distance = abs(point_x - x - 10) + abs(point_y - y - 30)
            if distance < 50:
                valid, piece = self.move(self.position, index)
                if valid:
                    self.place(x = point_x - 35, y = point_y - 35)
                    self.position = index
                    updated = True
                    
                    if type(piece) is chess.chess:
                        self.UItrigger(piece)
                    return
                else:
                    self.place(x = self.original_x, y = self.original_y)
#                print('new position : ',index
                    
        if not updated:
            self.place(x = self.original_x, y = self.original_y)
                    
class interface(Tk):
   
    def __init__(self,):
        super().__init__()
#        self.wm_attributes('-transparentcolor', self['bg'])
        
        self.side0 = {'G' : [], 'A' : [], 'E' : [], 'H': [], 'R' : [], 'C' : [], 'S' : []}
        self.side1 = {'G' : [], 'A' : [], 'E' : [], 'H': [], 'R' : [], 'C' : [], 'S' : []}
        
        self.resizable(False, False)
        self.width = 860
        self.height = 860
        
        self.leftFrame = Frame(self, height = 946, width = self.width)
        self.leftFrame.pack(side = LEFT)
        self.butFrame = Frame(self.leftFrame, height = 86, width = self.width, bg = 'red')
        self.butFrame.pack(expand = YES, side = TOP) #, fill = X
                
        self.mainFrame = Canvas(self.leftFrame, height = self.height, width = self.width, bg = '#FFC96B')
        self.mainFrame.pack(expand = YES, side = TOP) # , fill = X
        self.drawBoard()
        
        self.drawDot()
        
        S = Scrollbar(self)
        self.logs = Text(self, height=4, width= 30, font = 'arial 12', spacing2 = 5)
        S.pack(side=RIGHT, fill=Y)
        self.logs.pack(side=RIGHT, fill=Y)
        S.config(command=self.logs.yview)
        self.logs.config(yscrollcommand=S.set)
        
        
        # initiate the board
        self.board = mainBoard.mainBoard()
        self.board.startGame()
        self.placePieces()
        self.board.setLog(self.logs)
            
        # search object
        self.search = Search.minimax(self.board)
        
    def drawBoard(self,):
        start_x = 70
        start_y = 70
        self.mainFrame.create_rectangle(5, 5, self.height, self.width, width = 10)
        self.mainFrame.create_rectangle(start_x, start_y, 790, 790, width = 3)
        for i in range(8):
            # horizontal lines
            self.mainFrame.create_line(start_x, start_y + 80 * (i+1), 790, start_y + 80 * (i+1), width = 3)
            
            # vertical lines
            self.mainFrame.create_line(start_x + 90 * (i+1), start_x, start_y + 90 * (i+1), 390, width = 3)
            self.mainFrame.create_line(start_x + 90 * (i+1), 470, start_y + 90 * (i+1), 790, width = 3)
            
            # cross in castle
            self.mainFrame.create_line(340, start_y, 520, 230, width = 3)
            self.mainFrame.create_line(520, start_y, 340, 230, width = 3)
            self.mainFrame.create_line(340, 630, 520, 790, width = 3)
            self.mainFrame.create_line(520, 630, 340, 790, width = 3)
        
    def drawDot(self,):
        self.allPoint = {} # set of point on the canvas corresponding to chess board
        start_x = 70
        start_y = 70
        
        for i in range(10):
            for j in range(9):
                temp_y = start_y + 90 * j
                self.allPoint[i * 9 + j] = [ temp_y, start_x]
            start_x += 80
            
    def placePieces(self,):
        if not self.allPoint:
            print('dictionary is empty')
            print('terminating application')
            self.destroy()
        
        names = {1 : 'general', 2: 'advisor', 3: 'elephant', 4: 'horse', 5: 'chariot', 6: 'cannon', 7: 'soldier'}

        index = 0
        for x in self.board.board:
            if type(x) is chess.chess:
                px, py = self.allPoint[index]
                
                Ctype = names[x.type]
                path = './pieces/' + Ctype + str(x.side) + '.png'
                img = Image.open(path)
                img = img.resize((70, 70), Image.ANTIALIAS)
                pic = ImageTk.PhotoImage(img)
                
                temp_Label = DragDropMixin(self.mainFrame, height = 70, width = 70, image = pic)
                temp_Label.photo = pic
                temp_Label.addPoints(self.allPoint)
                temp_Label.setMove(self.move)
                temp_Label.setUITrigger(self.updatePieces)
                temp_Label.setPosition(index)
                temp_Label.pack()
                self.mainFrame.create_window(px, py, window= temp_Label) 
                
                if x.side == 1:
                    self.side1[x.name].append(temp_Label)
                else:
                    self.side0[x.name].append(temp_Label)
            index += 1
    
    def updatePieces(self, piece):
        # piece is an chess class obejct
        l = self.side1 if piece.side == 1 else self.side0
        temp_l = l[piece.name]
        
        for p in temp_l:
            if (piece.position[0]* 9 +piece.position[1]) == p.position:
                p.destroy()
                temp_l.remove(p)
#                print('destroyed')
                return
    
    def move(self, old_pos, new_pos):
        old_i = int(old_pos / 9)
        old_j = old_pos % 9
        new_i = int(new_pos / 9)
        new_j = new_pos % 9
        v, p = self.board.move(old_i, old_j, new_i, new_j, show = True)
        
        if self.board.curSide == 0:
            self.search.constructTree()
            self.AImove(self.search.root)
        return v, p
    
    def AImove(self, root):
        import random
        moves = self.board.getMoves()
        name = ['G', 'A', 'E', 'H', 'R', 'C', 'S']
        pick = random.choice(name)
        x0, y0, x1, y1 = random.choice(moves[pick])
        old_ind = x0 * 9 + y0
        new_ind = x1 * 9 + y1
        
        v, p = self.move(old_ind, new_ind)
        if v:
            for piece in self.side0[pick]:
                if piece.position == old_ind:
                    piece.position = new_ind
                    x, y = self.allPoint[new_ind]
                    piece.updateLocation(x, y)
                
            if type(p) is chess.chess:
                self.updatePiece(p)
        
        
        
    def addLog(self, log):
        self.logs.insert(END, log)
                

app = interface()
app.mainloop()