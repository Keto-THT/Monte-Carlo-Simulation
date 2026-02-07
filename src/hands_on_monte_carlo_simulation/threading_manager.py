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

class MonteCarloThread(threading.Thread):
    """
    Classe de threading pour exécuter la simulation de Monte Carlo en parallèle
    """

    def __init__(self, thread_id: int, nb_draws: int, seed: int = None, callback: callable = None, result_container: ThreadingResult = None):
        """
        Initialise le thread

        Args:
            thread_id (int): L'identifiant du thread
            nb_draws (int): Le nombre de tirages à effectuer dans ce thread
            seed (int, optional): La graine pour le générateur de nombres aléatoires. Defaults to None.
            callback (callable, optional): Une fonction de rappel à appeler avec les résultats du thread pour l'affichage GUI. Defaults to None.
            result_container (ThreadResult, optional): Un conteneur pour stocker les résultats du thread. Defaults to None.
        """
        super().__init__()
        self.thread_id = thread_id
        self.nb_draws = nb_draws
        self.seed = seed
        self.callback = callback
        self.result_container = result_container

        #génération d'une graine unique pour ce thread
        if seed is not None:
            self.seed = seed + thread_id
        else:
            self.seed = None
        
        self.generator = PointGenerator(self.seed)

        def run(self):
            """
            Exécute la génération de points pour ce thread et stocke les résultats 
            """

            # Mode GUI : génère les points un par un et utilise le callback pour l'affichage
            if self.callback is not None:
                for _ in range(self.nb_draws):
                    points, inside = self.generator.generate_points_with_details(1)  # Génère un point à la fois pour le GUI
                    if points : 
                        x, y, is_inside = points[0]
                        self.callback(x, y, is_inside)

                        if self.result_container is not None:
                            self.result_container.total_points += 1
                            if is_inside: 
                                self.result_container.inside_points += 1
            
            # Mode non-GUI : génère tous les points en batch en une fois et stocke les résultats dans le conteneur
            else:
                points, inside = self.generator.generate_points_with_details(self.nb_draws)

                if self.result_container is not None:
                    self.result_container.add_points_data(points)
    
class ThreadingManager:
    """
    Gestionnaire de threads pour la simulation Monte Carlo
    """

    def __init__(self, nb_threads: int, nb_draws: int, seed: int = None):
        """
        Initialise le gestionnaire de threads

        Args:
            nb_threads (int): Le nombre de threads à exécuter
            nb_draws (int): Le nombre de tirages à effectuer pour chaque thread
            seed (int, optional): La graine pour le générateur de nombres aléatoires - pour la reproductibilité. Defaults to None.
        """
        self.nb_threads = nb_threads
        self.nb_draws = nb_draws
        self.seed = seed
        self.threads: List[MonteCarloThread] = []
        self.results: List[ThreadResult] = []

    def run_parallel(self, callback: callable = None):
        """
        Exécute les threads en parallèle et collecte les résultats

        Args:
            callback (callable, optional): Une fonction de rappel à appeler avec les résultats de chaque thread pour l'affichage GUI. Defaults to None.
        
        Returns:
            Tuple (total_points, inside_points) 
        """
        self.threads = []
        self.results = []

        #Création des threads
        for i in range(self.nb_threads):
            result_container = ThreadResult()
            self.results.append(result_container)

            thread = MonteCarloThread(
                thread_id=i, 
                nb_draws= self.nb_draws,
                seed=self.seed,
                callback=callback,
                result_container=result_container
                )
            self.threads.append(thread)

            #Démarrage des threads
            for thread in self.threads:
                thread.start()

            #Attente de la fin de tous les threads
            for thread in self.threads:
                thread.join()

            #Calcul des résultats totaux
            total_points = sum(result.total_points for result in self.results)
            inside_points = sum(result.inside_points for result in self.results)

            return total_points, inside_points

    def get_points_data(self) -> List[Tuple[float, float, bool]]:
        """
        Récupère les détails de tous les points générés par tous les threads pour l'affichage GUI

        Returns:
            List[Tuple[float, float, bool]]: Liste de tuples contenant les coordonnées et si le point est à l'intérieur du cercle
        """
        all_points_data = []
        for result in self.results:
            all_points_data.extend(result.points_data)
        
        return all_points_data
