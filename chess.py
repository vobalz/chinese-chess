# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 21:17:25 2019

@author: User
"""
# chess type
GENERAL = 1
ADVISOR = 2
ELEPANT = 3
HORSE = 4
CHARIOT = 5
CANNON = 6
SOLDIER = 7
name = {GENERAL : 'G', ADVISOR : 'A', ELEPANT : 'E', HORSE: 'H', CHARIOT : 'R', CANNON : 'C', SOLDIER : 'S'}

class chess:
    def __init__(self, side, Ctype, position):
        self.side = side
        self.type = Ctype
        self.position = position
        self.sideAt = side
        self.name = name[self.type]
        self.captured = False
    
    def move(self, position):
        self.position = position
        self.update()
        
    def update(self, ):
        if self.side == self.sideAt :
            if (self.side == 0 and self.position[1] > 4) or (self.side == 1 and self.position[1] < 5):
                self.sideAt ^= 1
                
    def crossedRiver(self,):
        return self.sideAt != self.side
    