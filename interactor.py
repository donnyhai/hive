

class Interactor:
    def __init__(self, board, board_subset):
        self.board = board
        self.board_subset = board_subset
        
    #player want to put stone on coord. is that a legal move ?
    def put_stone_condition(self, player, stone, coord):
        #stone belongs to player
        cond1 = stone.color == player.color 
        #stone is not on board
        cond2 = not stone.is_on_board 
        #field at coord is empty
        cond3 = self.board.board[coord[0]][coord[1]].is_empty 
        #at least one same color neighbour, no other color neighbour.
        #watch the cases, that no or just one stone is on the board
        cond4 = False
        neighbours = self.board.get_neighbours(coord).values()
        if len(self.board.nonempty_fields) == 0:
            cond4 = True
        elif len(self.board.nonempty_fields) == 1:
            cond4 = coord in neighbours
        else:
            for neigh in neighbours:
                field = self.board.board[neigh[0]][neigh[1]]
                if not field.is_empty:
                    if field.stone.color != stone.color:
                        cond4 = False
                        break
                    else:
                        cond4 = True
        #bee has been put until 4. stoneput
        cond5 = True
        if len(self.board.nonempty_fields) in {6,7} and not player.stones["bee"].is_on_board:
            cond5 = stone.type == "bee"
        return cond1 and cond2 and cond3  and cond4 and cond5
    
    #player want to move stone to coord. is that generally possible ? that means independently of 
    #the stone type ? note that this game is yet without the "assel" stone    
    def move_stone_condition(self, player, stone, coord):
        #stone.coordinate != coord, tm the board has to change with the move
        cond00 = stone.coordinate != coord
        #bee is on board
        cond0 = player.stones["bee"].is_on_board
        #stone belongs to player
        cond1 = stone.color == player.color
        #stone is on board
        cond2 = stone.is_on_board
        #coord is empty (just for stone.type != "bug")
        cond3 = True
        if stone.type != "bug":
            cond3 = self.board.board[coord[0]][coord[1]].is_empty 
        #boardstones are connected after taking away stone
        nonempty_fields = self.board.nonempty_fields.copy()
        cond4 = self.board.is_connected(nonempty_fields.remove(stone.coordinate))
        return cond00 and cond0 and cond1 and cond2 and cond3 and cond4
            
    
    #player puts stone on coord (if possible)
    def put_stone(self, player, stone, coord):
        if  not self.put_stone_condition(player, stone, coord):
            print("stoneput not possible")
        else:
            self.board[coord[0]][coord[1]].put_stone(stone)
            stone.is_on_board = True
            self.board.nonempty_fields.append(coord)
    
    
    #move stone of player to coord (if possible)       
    def move_stone(self, player, stone, coord):
        def move(stone, coord):
            self.board.board[stone.coordinate[0]][stone.coordinate[1]].remove_stone(stone)
            self.board.board[coord[0]][coord[1]].put_stone(stone)
        
        if not self.move_stone_condition(player, stone, coord):
            print("stone move not possible")
        else:
            if stone.type == "bee":
                if coord in self.board_subset.get_bee_fields(coord): move(stone, coord)
                else: print("bee move not possible")
            elif stone.type == "ant":
                if coord in self.board_subset.get_ant_fields(coord): move(stone, coord)
                else: print("ant move not possible")
            elif stone.type == "hopper":
                if coord in self.board_subset.get_hopper_fields(coord): move(stone, coord)
                else: print("hopper move not possible")
            elif stone.type == "spider":
                if coord in self.board_subset.get_spider_fields(coord): move(stone, coord)
                else: print("spider move not possible")
            elif stone.type == "bug":
                if coord in self.board_subset.get_bug_fields(coord): move(stone, coord)
                else: print("bug move not possible") 
                    
                    

    
    