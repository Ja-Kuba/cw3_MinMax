from platform import node
from numpy import true_divide
from connect_error import ConnectError
from board import Board
from random import randrange
from operator import itemgetter
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from graphviz import Source, render


class ConnectLogic():
    PLAYER_Y = 1
    PLAYER_R = 2
    WINNER_MOVE=2 
    DRAW_MOVE=1
    NORMAL_MOVE=0 
    NODE_NUM=0
    
    def __init__(self, b_row, b_col, **kwarg) -> None:
        print("ConnectLogic init")
        self.ROWS_CNT = b_row
        self.COLUMNS_CNT = b_col
        self.game_board = Board(self.ROWS_CNT, self.COLUMNS_CNT)
        self.currentPlayer = self.PLAYER_Y 
        self.initMinMax(**kwarg)        
    
    def getCurrentPlayer(self):
        return self.currentPlayer


    def switchPlayer(self):
        self.currentPlayer = self.switch_player(self.currentPlayer)
    
    
    def switch_player(self, player):
        new_player = self.PLAYER_R if player == self.PLAYER_Y else self.PLAYER_Y
        return new_player
        

    def makeMove(self, r, c):
        ret= self.makeMove_inner(r, c, self.game_board)
        if ret == self.NORMAL_MOVE: 
            self.switchPlayer()
        return ret

    def makeMove_inner(self, r, c, board):
        self.setField(r, c, self.currentPlayer, board)      
        if self.isWinningMove(r, c, board): 
            return self.WINNER_MOVE
        elif not board.anyMovesLeft():
            return self.DRAW_MOVE
        else:
            return self.NORMAL_MOVE


    def isWinningMove(self, r, c, board):
        return (
            self.isWinningMove_inner(r,c,-1, 1, board) or
            self.isWinningMove_inner(r,c, 1, 1, board) or
            self.isWinningMove_inner(r,c, 0, 1, board) or
            self.isWinningMove_inner(r,c, 1, 0, board) 
        )

    

    def isWinningMove_inner(self, r, c, r_dir, c_dir, board):
        y, r = board.findLongestSeries(r, c,  r_dir, c_dir)
        if   len(y) and max(y) == 4: return True 
        elif len(r) and max(r) == 4: return True 
        else: return False
    

    
    def setField(self, row, col, player, board):
        color = None
        if player == self.PLAYER_Y: color = Board.YELLOW_P
        elif player == self.PLAYER_R: color = Board.RED_P
        else: 
            raise ConnectError(f"Invalid player value: {player}")
        
        board.setValue(row, col, color)
    
    def checkField(self, row, col):
        return self.game_board.getValue(row, col)
    
    
    '''
    minmax methods
    '''
    def initMinMax(self, minmax_depth=3):
        self.MAX_Player = self.PLAYER_Y
        self.MIN_Player = self.PLAYER_R
        self.MINMAX_DEPTH = minmax_depth
    
    def MinMax(self):
        valid_moves = self.game_board.getAllValidMoves()
        moves = []
        self.NODE_NUM = 0
        root = Node("root")
        for move in valid_moves:
            m_ret = self.findNextMove_minmax(
                depth=self.MINMAX_DEPTH,
                move=move,
                board=self.game_board.copy(),
                player=self.currentPlayer,
                root=root
                )
            moves.append((m_ret[0], move, m_ret[1]))
                
        max_move = max(moves ,key=itemgetter(0))
        min_move = min(moves ,key=itemgetter(0))
        m = min_move if self.currentPlayer == self.MIN_Player else max_move
        #print("------------")
        #print(moves)
        #print(f"max_move: {max_move}")
        #print(f"min_move: {min_move}")
        #for pre, fill, node in RenderTree(root):
        #    print("%s%s" % (pre, node.name))
        DotExporter(root).to_dotfile("root.dot")
        Source.from_file('root.dot')
        render('dot', 'png', 'root.dot')     
        
        print(f"move: {m}")
            
        if m:
            ret = self.makeMove(m[1][0], m[1][1])    
            return ret
        else: 
            raise ConnectError("invalid game status no moves found")
        #m = randrange(len(moves))
    
    
    
    '''
    def MinimaxFull(s) // początkowo s = s0
        if s ∈ T then
            return w(s) // węzeł terminalny, wypłata
        end
        U := successors(s)
        for u in U do
            w(u) = MinimaxFull(u)
        end
        if max-move then // ruch gracza Max
            return max(w(u))
        else
            return min(w(u))
        end

    '''
    # return (score:int, move|None)
    #return m_max, m_min
    def findNextMove_minmax(self, depth, move, board, player, root):
        m_res = self.makeMove_inner(move[0], move[1], board)
        s =(self.scoreMove(move[0], move[1], board, m_res, player), move)
        self.NODE_NUM+=1
        ch = Node(f"{s}_{depth}_{self.NODE_NUM}", parent=root)
        if m_res != self.NORMAL_MOVE or depth == 0:
            #ret = (self.scoreMove(move[0], move[1], board, m_res, player), move) 
            ret = s

        else:
            moves = board.getAllValidMoves()
            scores = []
            for i, m in enumerate(moves):
                m_res = self.findNextMove_minmax(
                    depth=depth-1,
                    move=m,
                    board=board.copy(),
                    player=self.switch_player(player),
                    root=ch,
                )
                scores.append(m_res)

            max_move = max(scores ,key=itemgetter(0))
            min_move = min(scores ,key=itemgetter(0))

            ret = min_move if player == self.MIN_Player else max_move
        
        
        return ret
    
    
    
    def scoreMove(self, row, col, board, m_res, player):
        ret = 0
        k = -1 if player == self.MIN_Player else 1
        if m_res == self.WINNER_MOVE:
            ret=k*1000
        elif m_res == self.DRAW_MOVE:
            ret = 0
        else:
            max_score=0 
            min_score=0
            max_score, min_score = self.scoreMove_series(max_score, min_score, board, row, col,-1, 1)
            max_score, min_score = self.scoreMove_series(max_score, min_score, board, row, col, 1, 1)
            max_score, min_score = self.scoreMove_series(max_score, min_score, board, row, col, 0, 1)
            max_score, min_score = self.scoreMove_series(max_score, min_score, board, row, col, 1, 0)
            ret = max_score - min_score
        
        return ret

    def scoreMove_series(self, max_score, min_score, board, row, col, r_dir, c_dir):
        max_tmp, min_tmp = board.findLongestSeries(row, col, r_dir, c_dir)
        max_score +=sum(max_tmp)
        min_score +=sum(min_tmp)
        return (max_score, min_score)
