import pygame

class SimulationUI:
    def __init__(self, width: int, height: int, bg_color: str, circle_color: str):
        """
        Initialise Pygame et la fenêtre
        """

        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.circle_color = circle_color
        
        #Initialisation Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Monte-Carlo Simulation")

    def handle_events(self) -> bool:
        """
        Gestionnaire d'événements les événements. Retourne False si on doit quitter.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw_quadrant_circle(self, line_width: int = 3):
        """
        Draw the top-right quadrant circle.
        """
        # On récupère les dimensions depuis l'instance
        width, height = self.screen.get_size()
        radius = height
        center = (0, height)

        # Dessin du cercle (Outline)
        pygame.draw.circle(self.screen, self.circle_color, center, radius, width=line_width)

        # Dessin des contours (Axes)
        pygame.draw.line(self.screen, self.circle_color, (0, height), (0, 0), width=line_width) # Vertical
        pygame.draw.line(self.screen, self.circle_color, (0, height), (width, height), width=line_width) # Horizontal

    def update(self):
        """
        Opérations sur l'écran d'affichage
        """

        #Nettoyage
        self.screen.fill(self.bg_color)
        
        #Dessin
        self.draw_quadrant_circle(line_width=3)
        #Affichage
        pygame.display.flip()

    def close(self):
        """
        Ferme Pygame
        """
        pygame.quit()

    def math_to_screen(self, x: float, y: float):
        """
        Transforme un point mathématique en coordonnées pixels (ex: 400, 300).
        Domaine mathématique [0, 1]
        """
        screen_x = int(x * self.width)
        screen_y = int(self.height - (y * self.height))
        return (screen_x, screen_y)
    
    def draw_point(self, x: float, y: float, color: str):
        """
        Dessine un point mathématique sur l'écran.
        """
        pixel_pos = self.math_to_screen(x, y)
        pygame.draw.circle(self.screen, color, pixel_pos, 2)