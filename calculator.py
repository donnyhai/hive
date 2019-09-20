import hexagon_stone as hs
import hexagon_graph as hg


#NOTE: calculator is not depending on players. for that see calculator_extended
class Calculator:
    def __init__(self, locator):
        self.locator = locator
        self.board = self.locator.board #note that the locator always contains the board object of the actual game
        #matrix has the sime size as board, is 1 in i,j iff we consider this field to be part 
        #of the set of fields we want to include at the moment (initialized with all fields, therefore all 1). 
        #the matrix will be helpful to get easier structural insides
        self.matrix = self.all_fields()
        self.empty_help_stone = hs.hexagon_stone(self.board.hexagon_size, "empty", 99)
        
        self.graph = hg.Hexagon_Graph(self.board) #doesnt contain points or edges yet
        
        
    def all_fields(self):
        return [[1] * self.board.size for i in range(self.board.size)]
    
    #are the stones connected after taking away stone on coord ? use hexagon_graph object
    def board_keeps_connected(self, coord):
        nonempty_fields = self.board.nonempty_fields.copy()
        nonempty_fields.remove(coord)
        self.graph.set_points(nonempty_fields)
        self.graph.set_edges(self.graph.calculate_standard_edges())
        return self.graph.is_connected()
    
    #which hexagons are moveable ? return is list of movable nonempty hexagons
    def get_movable_hexagons(self, color):
        nonempty_fields = self.board.nonempty_fields
        movable_hexagons = []
        for coord in nonempty_fields:
            hexagon  = self.board.board[coord[0]][coord[1]]
            cond0 = self.board_keeps_connected(coord)
            cond1 = not hexagon.has_bug_on
            cond2 = hexagon.color == color
            if cond0 and cond1 and cond2:
                movable_hexagons.append(hexagon)
        return movable_hexagons
    
    
    
    #input is the color of a stone which wants to be put onto the board from the side.
    #return is a list of board coords where this stone can be legally put to 
    def get_possible_put_fields(self, color):
        sol_fields = []
        for coord in self.board.nonempty_fields:
            for neigh in list(self.board.get_neighbours(coord).values()):
                #neigh must be empty
                if self.board.board[neigh[0]][neigh[1]].is_empty:
                    if color == "white":    opp_color = "black"
                    else:   opp_color = "white"
                    #neigh shall not have neighbours with different color as color
                    cond = True
                    for neigh2 in list(self.board.get_neighbours(neigh).values()):
                        if self.board.board[neigh2[0]][neigh2[1]].color == opp_color:   cond = False
                    if cond:    sol_fields.append(neigh)
        return sol_fields
    
    #move_hexagon wants to be moved, where can it move ? return is a list of board coords
    def get_possible_move_fields(self, move_hexagon):
        stone_type = move_hexagon.type
        board_pos = move_hexagon.board_pos
        if stone_type == "ant":     return self.get_ant_fields(board_pos)
        elif stone_type == "hopper":    return self.get_hopper_fields(board_pos)
        elif stone_type == "spider":    return self.get_spider_fields(board_pos)
        elif stone_type == "bee":   return self.get_bee_fields(board_pos)
        elif stone_type == "bug": return self.get_bug_fields(board_pos)
        
    
    
    
    #a ground walking stone is on coord. where can it physically move ?
    #this function returns all possible ground fields, especially for the ant.
    #use graph object
    def get_ground_move_fields(self, coord):
        self.graph.set_points(self.graph.calculate_all_empty_neighbours(coord))
        self.graph.set_edges(self.graph.calculate_ground_moving_edges(coord))
        ground_move_fields = self.graph.calculate_connected_component(coord)
        ground_move_fields.remove(coord) #remove this coord, as stone should not be able to move there
        return ground_move_fields
    
    #bee is on coord. where can it move ?
    def get_bee_fields(self, coord):
        return [coord1 for coord1 in self.get_ground_move_fields(coord) if self.graph.can_move_to_neighbour_on_ground(coord, coord1, self.board)]
    
    
    #ant is on coord. where can it move ?
    def get_ant_fields(self, coord):
        return self.get_ground_move_fields(coord)
    
    
    #hopper is on coord. where can it move ?
    def get_hopper_fields(self, coord):
        neighbours = self.board.get_neighbours(coord)
        hopper_fields = []
        #loop all the neighbours of coord and look for nonempty neighbours, 
        #and get the first empty field in every "direction"
        for i in range(6):
            neigh = neighbours[i]
            if not self.board.board[neigh[0]][neigh[1]].is_empty:
                while not self.board.board[neigh[0]][neigh[1]].is_empty:
                    neigh = self.board.get_neighbours(neigh)[i]
                hopper_fields.append(neigh)
        return hopper_fields

    #spider is on coord. where can she move ?
    def get_spider_fields(self, coord):
        self.graph.set_points(self.graph.calculate_all_empty_neighbours(coord))
        self.graph.set_edges(self.graph.calculate_ground_moving_edges(coord))
        self.graph.set_edges(self.graph.calculate_spider_move_edges())
        spider_fields = self.graph.get_graph_neighbours(coord)
        return spider_fields
    
    #bug is on coord. where can it move ?
    def get_bug_fields(self, coord):
        if self.board.board[coord[0]][coord[1]].underlaying_stones:
            return self.board.get_neighbours(coord).values()
        nonempty_neighbours = set(self.board.nonempty_fields).intersection(self.board.get_neighbours(coord).values())
        return self.get_bee_fields(coord) + list(nonempty_neighbours)
        
    #marienbug is on coord. where can it move ?
    def get_marienbug_fields(self, coord):
        pass

    
    
            








