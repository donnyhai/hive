#methods for window

def unmark_hexagons(hexagons, display, display_before, marked_hexagons):
    display.blit(display_before, (0,0))
    for hexagon in hexagons:
        hexagon.is_marked = False
    marked_hexagons.clear()  
    

def draw_markings(game, display, game_surface, clicked_hexagon, dir_hexagons):
    game.painter.draw_hexagon_marking(clicked_hexagon, display, (255,0,0), mark_mode = 5)
    game.painter.draw_set_of_hexagon_markings(dir_hexagons, game_surface, (0,255,0), mark_mode = 5)