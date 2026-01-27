import pygame

def draw_quadrant_circle(screen, color, line_width):
    """
    Draw the top-right quadrant circle

    Arguments 
        screen : 
        color : 
        line_width : 

    """
    width, height = screen.get_size()
    radius = height
    center = (0, height)

    # Dessin du cercle
    pygame.draw.circle(screen, color, center, radius, width=line_width)

    # Dessin des contours
    pygame.draw.line(screen, color, (0, height), (0, 0), width=line_width) #vertical
    pygame.draw.line(screen, color, (0, height), (width, height), width=line_width) #horizontal

    return screen