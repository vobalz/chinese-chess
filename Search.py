# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 01:27:42 2019

@author: User
"""

class node:
    def __init__(self, board, side):
        
        self.side = side
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.board = board
        self.children = []
            
    def addParent(self, p):
        self.parent.append(p)
        
    def addChild(self, children):
        for c in children:
            self.children.append(c)
            
    def getDepth(self,):
        d = 0
        if not self.chidlren:
            return 1
        else:
            for c in self.children:
                d = max(d, 1 + c.getDepth())
        return d

class minimax:
    def __init__(self, boardO):
        self.boardF = boardO
            
        self.dict_node = {}
        
    def getRoot(self,):
        root_board = self.boardF.board.copy()
        hash_v = hash(tuple(root_board))
        
        if self.dict_node.get(hash_v) is None:
            self.root = node(root_board, self.boardF.curSide)
        else:
            self.root = self.dict_node.get(hash_v)
    
    def constructTree(self,):
        self.getRoot()
        waiting_list = [self.root]
        waiting_children = []
        
        count = 0
        no_nodes = 0
        depth = 3
        
        while count < depth:
            if not waiting_list:
                print('depth: %d' % count)
            cur_node = waiting_list.pop(0)
            
            Moves = self.getMoves(cur_node.side, cur_node.board.copy())
            self.addChildren(cur_node, Moves, waiting_children)

            if not waiting_list:
                print('depth added 1')
                print('length of waiting list: %d' % len(waiting_children))
                count += 1
                if count < 3:
                    waiting_list = waiting_children.copy()
                else:
                    no_nodes += len(waiting_children)
                waiting_children = []
                no_nodes += len(waiting_list)
                
        waiting_children.clear()
        waiting_list.clear()
        no_nodes += 1
        sen = 'total number of nodes: %d \n' % no_nodes
        self.boardF.addLog(sen)
        print(sen)
            
    def getMoves(self, side, board):
        return self.boardF.getMovesSide(side, board)
        
    def addChildren(self, parent, dict_child, wait):
        if type(dict_child) is not dict:
            print('given parameter[1] is not type of dictionary')
            return False
        
        side = parent.side
        side ^= 1
        if not parent.children:
            for k, vs in dict_child.items():
                for v in vs:
                    old_i, old_j, new_i, new_j = v
                    
                    temp_board = self.boardF.moveExt(old_i, old_j, new_i, new_j, parent.board.copy())
                    hash_v = hash(tuple(temp_board))
                    
                    if self.dict_node.get(hash_v) is None:
                        child = node(temp_board, side)
                        parent.children.append(child)
                        self.dict_node[hash_v] = child
                    else:
                        child = self.dict_node.get(hash_v)
                    
                    wait.append(child)
        else:
            for c in parent.children:
                wait.append(c)
                
    def addDict(self, node):
        hash_v = hash(tuple(node.board))
        if self.dict_node.get(hash_v) is not None:
            print('the hash value is already exists, it will be replaced by the given node')
            
        self.dict_node[hash_v] = node.board.copy()
        
        
        
#    def constructT()