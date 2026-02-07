import threading
import random 
from typing import List, Tuple 
from .monte_carlo_simulation import MonteCarloSimulation

class ThreadResult:
    """
    Classe pour stocker les résultats d'un thread
    """
    def __init__(self, total_points: int, inside_points: int):
        self.total_points = total_points
        self.inside_points = inside_points
        self.points_data = []  # Pour stocker les détails des points pour le GUI

    def add_points_data(self, points: List[Tuple[float, float, bool]]):
        """
        Ajoute les détails des points générés pour le GUI

        Args:
            points (List[Tuple[float, float, bool]]): Liste de tuples contenant les coordonnées et si le point est à l'intérieur du cercle
        """
        self.points_data.extend(points)
        self.total_points += len(points)
        self.inside_points += sum(1 for _, _, is_inside in points if is_inside)



