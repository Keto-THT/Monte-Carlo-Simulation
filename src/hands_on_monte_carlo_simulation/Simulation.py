import pygame
import threading


class SimulationUI:
    def __init__(self, width: int, height: int, bg_color: str, circle_color: str):
        """
        Initialise Pygame et la fenêtre
        """

        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.circle_color = circle_color
        
        # Statistiques
        self.total_points = 0
        self.inside_points = 0
        self.lock = threading.Lock()  # Pour synchroniser l'accès aux stats
        
        # Initialisation Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height + 100))  # +100 pour les stats
        pygame.display.set_caption("Monte-Carlo Simulation - Approximation de π")
        
        # Police pour le texte
        self.font = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

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
        width = self.width
        height = self.height
        radius = height
        center = (0, height)

        # Dessin du cercle (Outline)
        pygame.draw.circle(self.screen, self.circle_color, center, radius, width=line_width)

        # Dessin des contours (Axes)
        pygame.draw.line(self.screen, self.circle_color, (0, height), (0, 0), width=line_width)  # Vertical
        pygame.draw.line(self.screen, self.circle_color, (0, height), (width, height), width=line_width)  # Horizontal

    def draw_statistics(self):
        """
        Affiche les statistiques en bas de l'écran
        """
        stats_y = self.height + 10
        
        # Calcul de π
        if self.total_points > 0:
            pi_estimate = 4.0 * self.inside_points / self.total_points
        else:
            pi_estimate = 0.0
        
        # Texte des statistiques
        with self.lock:
            points_text = self.font_small.render(
                f"Points totaux: {self.total_points}", 
                True, 
                (0, 0, 0)
            )
            inside_text = self.font_small.render(
                f"Points dans le quadrant: {self.inside_points}", 
                True, 
                (0, 128, 0)
            )
            pi_text = self.font.render(
                f"Approximation de π: {pi_estimate:.6f}", 
                True, 
                (0, 0, 255)
            )
        
        # Affichage
        self.screen.blit(points_text, (10, stats_y))
        self.screen.blit(inside_text, (10, stats_y + 25))
        self.screen.blit(pi_text, (10, stats_y + 50))

    def update(self):
        """
        Opérations sur l'écran d'affichage
        """

        # Nettoyage
        self.screen.fill(self.bg_color)
        
        # Dessin du quadrant
        self.draw_quadrant_circle(line_width=3)
        
        # Affichage des statistiques
        self.draw_statistics()
        
        # Affichage
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
    
    def draw_point(self, x: float, y: float, color: str, radius: int = 2):
        """
        Dessine un point mathématique sur l'écran.
        
        Args:
            x: Coordonnée x dans [0, 1]
            y: Coordonnée y dans [0, 1]
            color: Couleur du point (nom ou RGB tuple)
            radius: Rayon du point en pixels
        """
        pixel_pos = self.math_to_screen(x, y)
        pygame.draw.circle(self.screen, color, pixel_pos, radius)
    
    def add_point_callback(self, x: float, y: float, is_inside: bool):
        """
        Callback pour ajouter un point depuis un thread
        Thread-safe grâce au lock
        
        Args:
            x: Coordonnée x
            y: Coordonnée y
            is_inside: True si le point est dans le quadrant
        """
        with self.lock:
            self.total_points += 1
            if is_inside:
                self.inside_points += 1
        
        # Choix de la couleur
        color = (0, 255, 0) if is_inside else (255, 0, 0)  # Vert ou Rouge
        
        # Dessin du point
        self.draw_point(x, y, color, radius=2)
        
    def reset_statistics(self):
        """
        Réinitialise les statistiques
        """
        with self.lock:
            self.total_points = 0
            self.inside_points = 0
