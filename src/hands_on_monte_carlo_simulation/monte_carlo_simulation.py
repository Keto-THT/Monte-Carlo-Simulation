import random
from typing import Tuple, List


class MonteCarloSimulation: 
    """
    Classe pour effectuer les calculs Monte Carlo pour l'approximation de pi
    """

    def __init__(self, seed: int):
        """
        Initialise la classe MonteCarloSimulation

        Args:
            seed (int, optional): La graine pour le générateur de nombres aléatoires. Defaults to None.
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        
    
    @staticmethod
    def generate_random_points() -> Tuple[float, float]:
        """
        Génère un point aléatoire dans le carré de côté 1
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
    
    def generate_point(self, n: int) -> Tuple[List[Tuple[float, float, bool]], int]:
        """
        Génère n points aléatoires dans le carré de côté 1 et compte ceux qui sont dans le quadrant

        Args:
            n (int): Le nombre de points à générer

        Returns:
            Tuple qui contient la liste des points avec leur statut, et le nombre de points dans le quadrant
            Format : ([(x1, y1, is_inside), ...], count_inside)
        """
        points = []
        count_inside = 0

        for _ in range(n):
            x, y = self.generate_random_points()
            is_inside = self.is_in_quadrant(x, y)
            points.append((x, y, is_inside))

            if is_inside:
                count_inside += 1

        return (points, count_inside)
    
    @staticmethod
    def estimate_pi(total_points: int, count_inside: int) -> float:
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


class PointGenerator: 
    """
    Classe pour générer les points en utilisant le threading
    """

    def __init__(self, seed: int):
        """
        Initialise le générateur

        Args : 
            seed (int, optional): La graine pour le générateur de nombres aléatoires. Defaults to None.
        """
        if seed is not None:
            random.seed(seed)
        
        self.calculator = MonteCarloSimulation(seed)
    
    def generate_batch(self, n: int) -> Tuple[int, int]:
        """
        Génère un échantillon de n points et retourne les statistiques

        Args:
            n (int): Nombre de points à générer
        
        Returns:
            Tuple de la forme (total_points, inside_points)
        """

        points, inside_points = self.calculator.generate_point(n)

        return (n, inside_points)
    
    def generate_points_with_details(self, n: int) -> Tuple[List[Tuple[float, float, bool]], int]:
        """
        Génère un échantillon de n points et retourne les détails de chaque point pour l'affichage GUI

        Args:
            n (int): Nombre de points à générer
        
        Returns:
            Tuple de la forme ([(x1, y1, is_inside), ...], inside_points)
        """
        return self.calculator.generate_point(n)
