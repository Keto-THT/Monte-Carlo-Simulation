import random
import math 
from typing import Tuple, List


class MonteCarloSimulation: 
    """
    Classe pour effectuer les calculs Monte Carlo pour l'approximation de pi
    """

    def __init__(self, seed: int = None):
        """
        Initialise la classe MonteCarloSimulation

        Args:
            seed (int, optional): La graine pour le générateur de nombres aléatoires. Defaults to None.
        """
        if seed is not None:
            random.seed(seed)
        
    
    @staticmethod
    def generate_random_points() -> Tuple [float, float]:
        """
        Génère un point aléatoire dans le carrée de côté 1
        """
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        return x, y

    @staticmethod
    def is_in_quadrant(x: float, y: float) -> bool:
        """
        Vérifie si un point (x, y) est dans le quadrant du cercle

        Args:
            x (float): La coordonnée x du point
            y (float): La coordonnée y du point

        Returns:
            bool: True si le point est dans le quadrant, False sinon
        """
        return (x * x + y * y) <= 1
    
    def generate_point(self, n: int) -> Tuple[List[Tuple[float, float]], int]:
        """
        Génère n points aléatoires dans le carré de côté 1 et compte ceux qui sont dans le quadrant

        Args:
            n (int): Le nombre de points à générer

        Returns:
            Tuple qui contient la liste des points avec leur statut, et le nombre de points dans le quadrant
            Format : ([x1, y1, is_inside), ...], count_inside)])
        """
        points = []
        count_inside = 0

        for _ in range(n):
            x, y = self.generate_random_points()
            is_inside = self.is_in_quadrant(x, y)
            points.append((x, y, is_inside))

            if is_inside:
                count_inside += 1

        return points, count_inside
    
    @staticmethod
    def calculate_pi(total_points: int, count_inside: int,) -> float:
        """
        Calcule l'approximation de pi à partir du nombre total de points et du nombre de points dans le quadrant

        Args:
            total_points (int): Le nombre total de points générés
            count_inside (int): Le nombre de points qui sont dans le quadrant

        Returns:
            float: L'approximation de pi
        """
        if total_points == 0:
            return 0.0
        
        ratio = count_inside / total_points
        return 4.0 * ratio


    