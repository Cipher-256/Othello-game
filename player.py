from config import WHITE, BLACK
#from minimax import Minimax
import random
import board
import othello
import numpy as np

def change_color(color):
    if color == BLACK:
        return WHITE
    else:
        return BLACK
WHITE

class Human:

    #Human player 

    def __init__(self, gui, color="black"):
        self.color = color
        self.gui = gui

    def get_move(self):
        """ #Uses gui to handle mouse
        """
        validMoves = self.current_board.get_valid_moves(self.color)
        while True:
            move = self.gui.get_mouse_input()
            if move in validMoves:
                break
        self.current_board.apply_move(move, self.color)
        return 0, self.current_board

    def get_current_board(self, board):
        self.current_board = board 

    def perform_action(self,action):

        reward=self.board.apply_move(action,color)
        state=self.board.board
        done=self.board.game_ended()
        return state,reward,done


class Computer:
    def __init__(self,gui,color):
        self.color=color
        self.gui=gui
        self.epsilon=0.3
        self.gamma=0.5     #discount factor
        self.learning_rate=0.1
        self.board=board.Board()
        self.q_table=[[0]*9]*64
        self.q_list=np.zeros((64),dtype=int)
 
    def q_next(self,move,direction):
        #move=(pos/8,pos%8)
        pos=move[0]*8+move[1]
        #rew=np.amax(self.q_table[pos,:])
        if direction == 1:
            # north
            row_inc = -1
            col_inc = 0
        elif direction == 2:
            # northeast
            row_inc = -1
            col_inc = 1
        elif direction == 3:
            # east
            row_inc = 0
            col_inc = 1
        elif direction == 4:
            # southeast
            row_inc = 1
            col_inc = 1
        elif direction == 5:
            # south
            row_inc = 1
            col_inc = 0
        elif direction == 6:
            # southwest
            row_inc = 1
            col_inc = -1
        elif direction == 7:
            # west
            row_inc = 0
            col_inc = -1
        elif direction == 8:
            # northwest
            row_inc = -1
            col_inc = -1
        else:
            row_inc=0
            col_inc=0
        new_move=(move[0]+row_inc,move[1]+col_inc)
        new_pos=new_move[0]*8+new_move[1]
        #return self.current_board.board
        return new_move,direction

    def maxele(self,arr):
        max=0
        ind=0
        for i in range(1,len(arr)):
            if arr[i]>max:
                max=arr[i]
                ind=i
        return max,ind


    def q_max(self,move):
        pos=int(move[0]*8)+move[1]
        print(pos)
        maxr,direction=self.maxele(self.q_table[pos])
        rew=self.q_table[pos][direction]
        #move=(pos//8,pos%8)
        print(move ,"q_max")
        return rew,direction


    def q_updation(self,move,direction):
        #print(move)
        pos=move[0]*8+move[1]
        #move=(pos//8,pos%8)
        print(move ,"q_up")
        rew=0
        for i in range(1, 9):
                rew+=self.board.flip(i, move,self.color)
        print(self.q_table[pos][direction])
        
        new_move,direction=self.q_next(move,direction)
        maxim,direc=self.q_max(new_move)
        self.q_table[pos][direction]=self.q_table[pos][direction]+self.learning_rate*(rew+self.gamma*maxim-self.q_table[pos][direction])
        

    def get_move(self):
        tradeoff=random.randrange(0,1)
        maxm=0
        best_move=(0,0)
        direction=0
        maxvalue=0
        #done=Falsecurrent_board
        observation=self.current_board
        #tradeoff==0.003
        if tradeoff<self.epsilon: #explore
            action=random.choice(self.current_board.get_valid_moves(self.color))
        #while not done:
        #print(self.current_board.get_valid_moves(self.color))
        else:
            print(self.current_board.get_valid_moves(self.color))

            for move in self.current_board.get_valid_moves(self.color):
                print(move)
                immrew,direc=self.q_max(move)
                for i in range(1,10):
                    new_move,new_direc=self.q_next(move,direc)
                    new_value,new_direc=self.q_max(new_move)
                    if maxvalue<=new_value:
                        maxvalue=new_value
                #new_move,new_direc=self.q_next(move,direc)
                #new_value,new_direc=self.q_max(new_move)
                if maxm<=self.gamma*immrew+(1-self.gamma)*maxvalue:
                    print("bm",best_move,maxm)
                    maxm,direction=immrew,direc
                    action=move
                    #new_action=new_move
                    #new_direcion=new_direc
            #self.q_updation(action,direc,new_action,new_direction)
            self.q_updation(action,direc)
        observation,reward,done=self.perform_step(action)
        return 0,self.current_board
        #observation=self.board.board=observation_

    def perform_step(self,action):
        #print("b",action[0],action[1])
        #move=(action//8,action%8)
        #print(move ,"ps")
        reward=self.current_board.apply_move(action,self.color)
        state=self.current_board.next_states(self.color)
        done=self.current_board.game_ended()
        return state,reward,done

    def get_current_board(self, board):
        self.current_board = board 
        return self.current_board


class RandomPlayer (Computer):

    def get_move(self):
        x = random.sample(self.current_board.get_valid_moves(self.color), 1)
        return x[0]
