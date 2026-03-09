import threading
from typing import List, Tuple, Callable, Optional
from .monte_carlo_simulation import PointGenerator

class ThreadResult:
    """
    Classe pour stocker les résultats d'un thread (compteurs uniquement)
    """
    def __init__(self):
        self.total_points = 0
        self.inside_points = 0


class MonteCarloThread(threading.Thread):
    """
    Classe de threading pour exécuter la simulation de Monte Carlo en parallèle
    """

    def __init__(self, thread_id: int, nb_draws: int, seed: int,
                 result_container: ThreadResult, callback: Optional[Callable] = None):
        super().__init__()
        self.thread_id = thread_id
        self.nb_draws = nb_draws
        self.callback = callback
        self.result_container = result_container
        self.seed = (seed + thread_id) if seed is not None else None
        self.generator = PointGenerator(self.seed)

    def run(self):
        if self.callback is not None:
            # Mode GUI : génère les points un par un
            for _ in range(self.nb_draws):
                points, inside = self.generator.generate_points_with_details(1)
                if points:
                    x, y, is_inside = points[0]
                    self.callback(x, y, is_inside)
                    if self.result_container is not None:
                        self.result_container.total_points += 1
                        if is_inside:
                            self.result_container.inside_points += 1
        else:
            # Mode CLI : comptage uniquement, aucun stockage des coordonnées
            total, inside = self.generator.generate_batch(self.nb_draws)
            if self.result_container is not None:
                self.result_container.total_points += total
                self.result_container.inside_points += inside


class ThreadingManager:
    """
    Gestionnaire de threads pour la simulation Monte Carlo
    """

    def __init__(self, nb_threads: int, nb_draws_per_thread: int, seed: int):
        self.nb_threads = nb_threads
        self.nb_draws_per_thread = nb_draws_per_thread
        self.seed = seed
        self.threads: List[MonteCarloThread] = []
        self.results: List[ThreadResult] = []

    def run_parallel(self, callback: Optional[Callable] = None) -> Tuple[int, int]:
        """
        Exécute les threads en parallèle et collecte les résultats.

        Args:
            callback: Fonction de rappel optionnelle pour le mode GUI. Defaults to None.

        Returns:
            Tuple (total_points, inside_points)
        """
        self.threads = []
        self.results = []

        for i in range(self.nb_threads):
            result_container = ThreadResult()
            self.results.append(result_container)

            thread = MonteCarloThread(
                thread_id=i,
                nb_draws=self.nb_draws_per_thread,
                seed=self.seed,
                callback=callback,
                result_container=result_container
            )
            self.threads.append(thread)

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

        total_points = sum(result.total_points for result in self.results)
        inside_points = sum(result.inside_points for result in self.results)

        return total_points, inside_points