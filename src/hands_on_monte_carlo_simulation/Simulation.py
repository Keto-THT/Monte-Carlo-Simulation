import pygame
import threading
import math


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
        self.lock = threading.Lock()

        # ✅ CORRECTION : initialisé ici (était commenté → crash dans draw_all_points)
        self.points_to_draw = []  # Liste de (x, y, color)

        # Initialisation Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height + 100))
        pygame.display.set_caption("Monte-Carlo Simulation - Approximation de π")

        # Police pour le texte
        self.font = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw_quadrant_circle(self, line_width: int = 3):
        width = self.width
        height = self.height
        radius = min(width, height)
        center_x = 0
        center_y = height

        num_segments = 100
        points = []
        for i in range(num_segments + 1):
            angle = -math.pi / 2 + (i / num_segments) * (math.pi / 2)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))

        if len(points) > 1:
            pygame.draw.lines(self.screen, self.circle_color, False, points, line_width)

        pygame.draw.line(self.screen, self.circle_color,
                         (center_x, center_y), (center_x, center_y - radius),
                         width=line_width)
        pygame.draw.line(self.screen, self.circle_color,
                         (center_x, center_y), (center_x + radius, center_y),
                         width=line_width)

    def draw_statistics(self):
        stats_y = self.height + 10
        if self.total_points > 0:
            pi_estimate = 4.0 * self.inside_points / self.total_points
        else:
            pi_estimate = 0.0

        with self.lock:
            points_text = self.font_small.render(
                f"Points totaux: {self.total_points}", True, (0, 0, 0))
            inside_text = self.font_small.render(
                f"Points dans le quadrant: {self.inside_points}", True, (0, 128, 0))
            pi_text = self.font.render(
                f"Approximation de π: {pi_estimate:.6f}", True, (0, 0, 255))

        self.screen.blit(points_text, (10, stats_y))
        self.screen.blit(inside_text, (10, stats_y + 25))
        self.screen.blit(pi_text, (10, stats_y + 50))

    def draw_all_points(self):
        with self.lock:
            for x, y, color in self.points_to_draw:
                pixel_pos = self.math_to_screen(x, y)
                pygame.draw.circle(self.screen, color, pixel_pos, 2)

    def update(self):
        self.screen.fill(self.bg_color)
        self.draw_quadrant_circle(line_width=3)
        self.draw_all_points()
        self.draw_statistics()
        pygame.display.flip()

    def close(self):
        pygame.quit()

    def math_to_screen(self, x: float, y: float):
        scale = min(self.width, self.height)
        screen_x = int(x * scale)
        screen_y = int(self.height - (y * scale))
        return (screen_x, screen_y)

    def draw_point(self, x: float, y: float, color: str, radius: int = 2):
        pixel_pos = self.math_to_screen(x, y)
        pygame.draw.circle(self.screen, color, pixel_pos, radius)

    def add_point_callback(self, x: float, y: float, is_inside: bool):
        color = (0, 255, 0) if is_inside else (255, 0, 0)
        with self.lock:
            self.total_points += 1
            if is_inside:
                self.inside_points += 1
            self.points_to_draw.append((x, y, color))

    def reset_statistics(self):
        with self.lock:
            self.total_points = 0
            self.inside_points = 0
            self.points_to_draw = []
