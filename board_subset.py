

class Board_Subset:
    def __init__(self, locator):
        self.locator = locator
        self.board = self.locator.board #note that the locator always contains the board object of the actual game
        #matrix has the sime size as board, is 1 in i,j iff we consider this field to be part 
        #of the set of fields we want to include at the moment (initialized with all fields, therefore all 1). 
        #the matrix will be helpful to get easier structural insides
        self.matrix = self.all_fields()
        
    def all_fields(self):
        return [[1] * self.size for i in range(self.size)]
    
    #a ground walking stone is on coord. where can it physically move ?
    #this function returns all possible ground fields, especially for the ant.
    #for the spider and bee conditions have to be added then at another code location.
    #with the help of the locator, which simulates all moving possibilities in forward, this function
    #checks whether on the way of one empty field to another a stone (ant) has to pass a too small gap 
    #for a stone to pass, which therefore does make the move impossible. As the locator saves his fields 
    #on the way, it is like a spion which goes first and checks the situation, then returns all fields 
    #which are ok, that means physically reachable on the ground. function can_move_to_neighbour_on_ground
    #of locator is helpful. 
    def get_ground_move_fields(self, coord):
        
        #return neighbours of coord in test_board which are ground-reachably and which arent in seen_by_locator
        def get_right_neighbours(coord):
            seen_by_locator = [self.locator.locations[k][1] for k in range(start_key - 1, self.locator.new_key)]
            neighbours = list(self.test_board.get_neighbours(coord).values())
            for neigh in neighbours:
                cond1 = not self.locator.can_move_to_neighbour_on_ground(coord, neigh, self.locator.test_board)
                cond2 = neigh in seen_by_locator
                if cond1 or cond2:
                    neighbours.remove(neigh)
            return neighbours
            
        #this function just gets applied on coordinates which are "right neighbours"
        def add_neigh_to_locator(dir_coord):   
            
            actual_stone = self.locator.get_position()
            self.locator.test_board.move_stone(actual_stone, dir_coord)
            self.locator.move_to_position(dir_coord, self.locator.test_board)
                
            right_neighbours = get_right_neighbours(dir_coord)
            if len(right_neighbours) == 0:
                return
            else:
                add_neigh_to_locator(right_neighbours.pop()) #possible error source, 
                #as just ONE neighbour is considered, but should be enough
        
        self.locator.move_to_position(coord)
        self.locator.test_board.copy_board(self.board)
        start_key = self.locator.new_key
        
        right_neighbours = get_right_neighbours(coord)
        
        for neigh in right_neighbours:
            #copy the actual board constellation into test_board
            self.locator.test_board.copy_board(self.board)
            #move locator back to the "starting" coordinate
            self.locator.move_to_position(coord, self.locator.test_board)
            #run the recursive function
            add_neigh_to_locator(neigh)
            
        ground_move_fields = [self.locator.locations[k].coordinate for k in range(start_key, self.locator.new_key)]    
        
        #set indicator matrix
        for i in range(self.board.size):
            for j in range(self.board.size):
                self.matrix[i][j] = 1 if (i,j) in ground_move_fields else self.matrix[i][j] = 0
        
        return ground_move_fields
         
    
        #hopper is on coord. where can it move ?
        def get_hopper_fields(self, coord):
            neighbours = self.board.get_neighbours(coord)
            hopper_fields = []
            #loop all the neighbours of coord and look for nonempty neighbours, 
            #and get the first empty field in every "direction"
            for i in range(5):
                neigh = neighbours[i]
                if not self.board.board[neigh[0]][neigh[1]].is_empty:
                    while not self.board.board[neigh[0]][neigh[1]].is_empty:
                        neigh = self.board.get_neighbours(neigh)[i]
                    hopper_fields.append(neigh)
            return hopper_fields
    
        
        