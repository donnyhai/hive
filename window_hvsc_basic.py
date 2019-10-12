import pygame
import game as g
import texts as t
import window_methods as wm
import variables as v
pygame.init()
clock = pygame.time.Clock()

 
class Window_HvsC_Basic:
    def __init__(self):
        self.running = False
        self.display = None
        self.game = None
        
        self.start_game_mode = True
        
        self.current_player_color = "white"
        self.game_over = False
        self.drag = False
        self.moved = False
        
        self.marked_hexagons = []
        self.src_hexagon = None
        self.dir_hexagon = None
        self.dir_hexagons = []
        self.counter = None
        self.pos = None
 
    def on_init(self):
        self.display = pygame.display.set_mode(v.window_size)
        pygame.display.set_caption("Spielbrett")
        self.game = g.HvsC_Game_Basic(self.display) #create self.game
        self.hum_player = self.game.players["white"]
        self.com_player = self.game.players["black"]
        self.running = True
    
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if not self.running:
            self.on_init()
            
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            
        self.on_cleanup()
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        
        if self.start_game_mode:
                        
            self.game.painter.draw_background(self.game.surfaces["surface_board"])
            self.game.painter.draw_background(self.game.surfaces["surface_stones"]["white"])
            self.game.painter.draw_background(self.game.surfaces["surface_stones"]["black"])
            self.game.painter.draw_background(self.game.surfaces["surface_text"]["white"])
            self.game.painter.draw_background(self.game.surfaces["surface_text"]["black"])

            self.game.painter.draw_set_of_hexagons(self.game.players["white"].side_stones.values(), self.game.surfaces["surface_stones"]["white"])
            self.game.painter.draw_set_of_hexagons(self.game.players["black"].side_stones.values(), self.game.surfaces["surface_stones"]["black"])
            self.game.painter.draw_all_stone_numbers(self.game.players["white"], self.game.surfaces)
            self.game.painter.draw_all_stone_numbers(self.game.players["black"], self.game.surfaces)
            
            self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons)
            
            self.game.painter.draw_ingame_frame(self.game.surfaces["surface_full"])
            
            self.start_game_mode = False 
            
            #print a text claiming that white begins
            self.game.painter.write_box_text(self.game.surfaces, t.welcome_text, "white")
            self.game.painter.write_box_text(self.game.surfaces, t.welcome_text, "black")
            
        elif not self.start_game_mode:
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if wm.point_in_surface(self.game.surfaces["surface_board"], event.pos):
                    if event.button == 1: #button 1: left mouse click
                        if not self.drag:
                            self.drag = True
                            self.pos = (event.pos, event.pos)
                            self.counter = 0
                    elif event.button == 5: #button 4: scroll in 
                        #the following if check ensures that you do not zoom to much out, as for some reason you cannot zoom in again 
                        #(why does this happen ? is there a better factor than 100 ?)
                        if self.game.board.hexagon_size > self.game.surfaces["surface_full"].get_width() // 80: 
                            ratio = 0.85 #zoom out
                            ep, dp = event.pos, self.game.board.draw_position
                            #make the event.pos the center of zooming
                            if self.game.board.scroll_is_inside_board(ep):   offset = ((1 - ratio) * (ep[0] - dp[0]), (1 - ratio) * (ep[1] - dp[1]))
                            else:   offset = (0,0)
                            self.game.interactor.scale_board(ratio)
                            self.game.interactor.translate_board(offset)
                            self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons, v.mark_size)
                    elif event.button == 4: #button 5: scroll out
                        ratio = 1.18 #zoom in
                        ep, dp = event.pos, self.game.board.draw_position
                        #make the event.pos the center of zooming
                        if self.game.board.scroll_is_inside_board(ep):   offset = ((1 - ratio) * (ep[0] - dp[0]), (1 - ratio) * (ep[1] - dp[1]))
                        else:   offset = (0,0)
                        self.game.interactor.scale_board(ratio)
                        self.game.interactor.translate_board(offset)
                        self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons, v.mark_size)
                    
            elif event.type == pygame.MOUSEMOTION and self.drag:
                if self.counter == 2: #makes the clicking nicer (there should not be dragging, just because a click was not completely precise)
                    self.moved = True
                    self.pos = self.pos[1], event.pos #save actual and one mousepos before to always add a new draw offset from pixel to pixel
                    if wm.point_in_surface(self.game.surfaces["surface_board"], self.pos[1]):
                        self.game.interactor.translate_board((self.pos[1][0] - self.pos[0][0], self.pos[1][1] - self.pos[0][1]))
                        self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons, v.mark_size)
                else: self.counter += 1
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.drag = False
                if self.moved:   self.moved = False
                else:
                    if self.game.buttons["center_button"].pressed(event.pos):
                        self.game.board.draw_position = self.game.board.initial_draw_position
                        self.game.interactor.scale_board(self.game.board.initial_hexagon_size / self.game.board.hexagon_size)
                        self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons, v.mark_size)
                        
                    elif self.game.buttons["back_button"].pressed(event.pos):
                        if not self.game.turn == ("white", 1): 
                            del self.game.board.past_boards[len(self.game.board.past_boards) - 1]
                            last_constellation = self.game.board.past_boards[len(self.game.board.past_boards) - 1]
                            self.game.interactor.put_into_constellation(last_constellation)
                            self.marked_hexagons.clear()
                            self.game.turn = last_constellation["turn"]
                            self.game_over = False
                            
                    elif self.game.buttons["restart_button"].pressed(event.pos):
                        #at this point we could just overwrite the actual board and players with a new init board and new 
                        #players, and then init a new interactor etc (see the chronology in class self.game). But by this we do not
                        #have the same board, player and stone objects as before, which we may want in the future to analize 
                        #gaming behavour better. Therefore the self.game gets restarted by resetting all board, player and stones attr
                        #manually.
                        self.game.interactor.restart_game()
                        self.game.turn = ("white", 1)
                        self.game_over = False
                    
                    else:
                        if not self.game_over:
                            #note, this is a list it shall contain exactly one nonempty hexagon iff the click was on this hexagon
                            clicked_hexagon = self.game.interactor.calculator.get_clicked_hexagon(event.pos)
                            
                            if clicked_hexagon.number != 99: #special condition, see calculator.get_clicked_hexagon and calculator.empty_help_stone
            
        # (white, 1)                
                                if self.game.turn == ("white", 1):
                                    self.dir_hexagon = self.game.board.board[v.first_stone_board_pos] #shall be middle hexagon of the empty board
                                    if not self.marked_hexagons:
                                        if clicked_hexagon.color == "white":
                                            self.src_hexagon = clicked_hexagon
                                            self.marked_hexagons = [self.src_hexagon, self.dir_hexagon]
                                            wm.mark_hexagons(self.game, self.marked_hexagons, v.mark_size)
                                    #in this case stone put will be executed and the turn goes one up
                                    elif clicked_hexagon == self.dir_hexagon:
                                        wm.unmark_hexagons(self.game, self.game.players["white"], self.marked_hexagons)
                                        self.game.interactor.execute_stone_put(self.game.players["white"], self.src_hexagon, self.dir_hexagon)
                                        self.game.turn_up()
                                        
        # computer reaction             
                                        first_put_stone = self.game.com_action.random_element(list(self.com_player.side_stones.values()))
                                        neigh_coords = self.game.board.get_neighbours(v.first_stone_board_pos).values()
                                        self.dir_hexagons = [self.game.board.board[coord] for coord in neigh_coords] #all empty neighbours of the middle hexagon
                                        self.dir_hexagon = self.game.com_action.random_element(self.dir_hexagons)
                                        self.game.interactor.execute_stone_put(self.com_player, first_put_stone, self.dir_hexagon)
#                                        if self.game.players["black"].can_act:                           
#                                            com_decision = self.game.com_action.get_action_decision()
#                                            self.game.interactor.execute_stone_put(self.game.players["black"], com_decision[0], com_decision[1])
                                        
                                        self.game.turn_up()
                                        #now turn is ("white", 2)
                                        
                                    #unmark marked hexagons
                                    else:
                                        if self.marked_hexagons: wm.unmark_hexagons(self.game, self.game.players["white"], self.marked_hexagons)
        # turn 2 - 4                    
                                #at least one white and one black stone are put now. now be has to be put until 4. turn
                                elif self.game.turn[1] in {2,3,4}:
                                    self.current_player_color = self.game.turn[0]
                                    bee_stone = list(self.game.players[self.current_player_color].stones["bee"].values())[0]
            #bee not put
                                    #putting phase: bee is not yet on board
                                    if not bee_stone.is_on_board:
                                        if not self.marked_hexagons:
                                            
                                            #mark put
                                            if clicked_hexagon in self.game.players[self.current_player_color].side_stones.values():
                                                self.src_hexagon = clicked_hexagon
                                                if self.src_hexagon in self.game.players[self.current_player_color].putable_hexagons:
                                                    #check whether clicked hexagon is bee in the case that it is turn 4 now
                                                    #note: we are in the case that the bee is not yet put
                                                    if self.game.turn[1] < 4 or clicked_hexagon.type == "bee": 
                                                        dir_hexagons_coords = self.game.interactor.calculator.get_possible_put_fields(self.current_player_color)
                                                        self.dir_hexagons = [self.game.board.board[coords] for coords in dir_hexagons_coords]
                                                        self.marked_hexagons = self.dir_hexagons + [self.src_hexagon]
                                                        wm.mark_hexagons(self.game, self.marked_hexagons, v.mark_size)
                                                    
                                        #execute put
                                        elif clicked_hexagon in self.dir_hexagons:
                                            wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                            self.game.interactor.execute_stone_put(self.game.players[self.current_player_color], self.src_hexagon, clicked_hexagon)
                                            self.game.turn_up() #set new turn
                                            #check whether opponent has any possible put or move, if not put turn up 
                                            if not self.game.players[self.game.turn[0]].can_act:  self.game.turn_up()
                                            #check winning condition
                                            self.game_over = wm.check_winner(self.game.painter, self.game.surfaces, self.current_player_color, self.game.interactor.calculator.winning_condition(self.current_player_color), self.game_over)
                                            self.dir_hexagons.clear()
                                            
                                            #put bee reminder:
                                            if self.current_player_color == "white":
                                                if not self.game.players["black"].stones["bee"][1].is_on_board:
                                                    self.game.painter.write_box_text(self.game.surfaces, t.bee_reminder, "black")
                                            else:
                                                if not self.game.players["white"].stones["bee"][1].is_on_board:
                                                    self.game.painter.write_box_text(self.game.surfaces, t.bee_reminder, "white")
                                            
                                        
                                        else:
                                            if self.marked_hexagons: wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
            #bee already put                          
                                    else:
                                        if not self.marked_hexagons:
                                            
                                            #mark put
                                            if clicked_hexagon in self.game.players[self.current_player_color].side_stones.values():
                                                self.src_hexagon = clicked_hexagon
                                                if self.src_hexagon in self.game.players[self.current_player_color].putable_hexagons:
                                                    dir_hexagons_coords = self.game.interactor.calculator.get_possible_put_fields(self.current_player_color)
                                                    self.dir_hexagons = [self.game.board.board[coords] for coords in dir_hexagons_coords]
                                                    self.marked_hexagons = self.dir_hexagons + [self.src_hexagon]
                                                    wm.mark_hexagons(self.game, self.marked_hexagons, v.mark_size)
                                            
                                            #mark move
                                            elif clicked_hexagon in self.game.players[self.current_player_color].stones_list:
                                                self.src_hexagon = clicked_hexagon
                                                if self.src_hexagon in self.game.players[self.current_player_color].moveable_hexagons:
                                                    dir_hexagons_coords = self.game.interactor.calculator.get_possible_move_fields(self.src_hexagon)
                                                    self.dir_hexagons = [self.game.board.board[coords] for coords in dir_hexagons_coords]
                                                    self.marked_hexagons = self.dir_hexagons + [self.src_hexagon]
                                                    wm.mark_hexagons(self.game, self.marked_hexagons, v.mark_size)
                                        
                                        #execute put
                                        elif self.src_hexagon in self.game.players[self.current_player_color].side_stones.values():
                                            if clicked_hexagon in self.dir_hexagons:
                                                wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                                self.game.interactor.execute_stone_put(self.game.players[self.current_player_color], self.src_hexagon, clicked_hexagon)
                                                self.game.turn_up() #set new turn
                                                #check whether opponent has any possible put or move, if not put turn up 
                                                if not self.game.players[self.game.turn[0]].can_act:  self.game.turn_up()
                                                #check winning condition
                                                self.game_over = wm.check_winner(self.game.painter, self.game.surfaces, self.current_player_color, self.game.interactor.calculator.winning_condition(self.current_player_color), self.game_over)
                                                self.dir_hexagons.clear()
                                                
                                                #put bee reminder:
                                                if self.current_player_color == "white":
                                                    if not self.game.players["black"].stones["bee"][1].is_on_board:
                                                        self.game.painter.write_box_text(self.game.surfaces, t.bee_reminder, "black")
                                                else:
                                                    if not self.game.players["white"].stones["bee"][1].is_on_board:
                                                        self.game.painter.write_box_text(self.game.surfaces, t.bee_reminder, "white")
                                                
                                            else: 
                                                if self.marked_hexagons: wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                        
                                        #execute move
                                        elif self.src_hexagon in self.game.players[self.current_player_color].stones_list:
                                            if clicked_hexagon in self.dir_hexagons and clicked_hexagon.board_pos != self.src_hexagon.board_pos: 
                                                wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                                if self.src_hexagon.type == "bug":
                                                    if not clicked_hexagon.is_empty or len(self.src_hexagon.underlaying_stones) > 0:
                                                        self.game.interactor.move_bug_on_nonempty_stone(self.game.players[self.current_player_color], self.src_hexagon, clicked_hexagon)
                                                    else: self.game.interactor.execute_stone_move(self.game.players[self.current_player_color], self.src_hexagon, clicked_hexagon)
                                                else: self.game.interactor.execute_stone_move(self.game.players[self.current_player_color], self.src_hexagon, clicked_hexagon)
                                                self.game.turn_up() #set new turn
                                                #check whether opponent has any possible put or move, if not put turn up 
                                                if not self.game.players[self.game.turn[0]].can_act:  self.game.turn_up()
                                                #check winning condition
                                                self.game_over = wm.check_winner(self.game.painter, self.game.surfaces, self.current_player_color, self.game.interactor.calculator.winning_condition(self.current_player_color), self.game_over)
                                                self.dir_hexagons.clear()
                                                
                                                #put bee reminder:
                                                if self.current_player_color == "white":
                                                    if not self.game.players["black"].stones["bee"][1].is_on_board:
                                                        self.game.painter.write_box_text(self.game.surfaces, t.bee_reminder, "black")
                                                else:
                                                    if not self.game.players["white"].stones["bee"][1].is_on_board:
                                                        self.game.painter.write_box_text(self.game.surfaces, t.bee_reminder, "white")
                                                
                                            else: 
                                                if self.marked_hexagons: wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                        
                                        else: 
                                            if self.marked_hexagons: wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                    
                                    
        # turn > 4                        
                                elif self.game.turn[1] > 4:           
                                    self.current_player_color = self.game.turn[0]
                                    
                                    if not self.marked_hexagons:
                                        
                                        #mark put
                                        if clicked_hexagon in self.game.players[self.current_player_color].side_stones.values():
                                            self.src_hexagon = clicked_hexagon
                                            if self.src_hexagon in self.game.players[self.current_player_color].putable_hexagons:
                                                dir_hexagons_coords = self.game.interactor.calculator.get_possible_put_fields(self.current_player_color)
                                                self.dir_hexagons = [self.game.board.board[coords] for coords in dir_hexagons_coords]
                                                self.marked_hexagons = self.dir_hexagons + [self.src_hexagon]
                                                wm.mark_hexagons(self.game, self.marked_hexagons, v.mark_size)
                                        
                                        #mark move
                                        elif clicked_hexagon in self.game.players[self.current_player_color].stones_list:
                                            self.src_hexagon = clicked_hexagon
                                            if self.src_hexagon in self.game.players[self.current_player_color].moveable_hexagons:
                                                dir_hexagons_coords = self.game.interactor.calculator.get_possible_move_fields(self.src_hexagon)
                                                self.dir_hexagons = [self.game.board.board[coords] for coords in dir_hexagons_coords]
                                                self.marked_hexagons = self.dir_hexagons + [self.src_hexagon]
                                                wm.mark_hexagons(self.game, self.marked_hexagons, v.mark_size)
                                        
                                    #execute put
                                    elif self.src_hexagon in self.game.players[self.current_player_color].side_stones.values():
                                        if clicked_hexagon in self.dir_hexagons:
                                            wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                            self.game.interactor.execute_stone_put(self.game.players[self.current_player_color], self.src_hexagon, clicked_hexagon)
                                            self.game.turn_up() #set new turn
                                            #check whether opponent has any possible put or move, if not put turn up 
                                            if not self.game.players[self.game.turn[0]].can_act:  self.game.turn_up()
                                            #check winning condition
                                            self.game_over = wm.check_winner(self.game.painter, self.game.surfaces, self.current_player_color, self.game.interactor.calculator.winning_condition(self.current_player_color), self.game_over)
                                            self.dir_hexagons.clear()
                                        else: 
                                            if self.marked_hexagons: wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                    
                                    #execute move
                                    elif self.src_hexagon in self.game.players[self.current_player_color].stones_list:
                                        if clicked_hexagon in self.dir_hexagons and clicked_hexagon.board_pos != self.src_hexagon.board_pos:
                                            wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                            if self.src_hexagon.type == "bug":
                                                if not clicked_hexagon.is_empty or len(self.src_hexagon.underlaying_stones) > 0:
                                                    self.game.interactor.move_bug_on_nonempty_stone(self.game.players[self.current_player_color], self.src_hexagon, clicked_hexagon)
                                                else: self.game.interactor.execute_stone_move(self.game.players[self.current_player_color], self.src_hexagon, clicked_hexagon)
                                            else: self.game.interactor.execute_stone_move(self.game.players[self.current_player_color], self.src_hexagon, clicked_hexagon)
                                            self.game.turn_up() #set new turn
                                            #check whether opponent has any possible put or move, if not put turn up 
                                            if not self.game.players[self.game.turn[0]].can_act:  self.game.turn_up()
                                            #check winning condition
                                            self.game_over = wm.check_winner(self.game.painter, self.game.surfaces, self.current_player_color, self.game.interactor.calculator.winning_condition(self.current_player_color), self.game_over)
                                            self.dir_hexagons.clear()
                                        
                                        else:
                                            if self.marked_hexagons: wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                                    else:
                                        if self.marked_hexagons: wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)
                            else:
                                if self.marked_hexagons: wm.unmark_hexagons(self.game, self.game.players[self.current_player_color], self.marked_hexagons)

        pygame.display.update()
        clock.tick(v.FPS)
        
        


 
#if __name__ == "__main__" :
#    theApp = App()
#    theApp.on_execute()