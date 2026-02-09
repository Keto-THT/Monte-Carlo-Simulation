import sys
import pygame
import logging
from .Simulation import SimulationUI
from .threading_manager import ThreadingManager
from .monte_carlo_simulation import MonteCarloSimulation

def setup_logging(verbosity: int):
    """
    Configure le niveau de logging selon la verbosité
    
    Args:
        verbosity: 0 = WARNING, 1 = INFO, 2+ = DEBUG
    """
    if verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


def write_output(output_file: str, result: str):
    """
    Écrit le résultat dans le fichier de sortie ou stdout
    
    Args:
        output_file: Chemin du fichier ou '-' pour stdout
        result: Résultat à écrire
    """
    if output_file == '-':
        print(result)
    else:
        try:
            with open(output_file, 'w') as f:
                f.write(result + '\n')
            logging.info(f"Résultat écrit dans {output_file}")
        except IOError as e:
            logging.error(f"Erreur lors de l'écriture dans {output_file}: {e}")
            sys.exit(1)


def run_gui_mode(args):
    """
    Exécute la simulation avec interface graphique
    
    Args:
        args: Arguments parsés
    """
    logging.info("Initialisation du mode GUI...")
    
    ui = SimulationUI(
        width=args.width,
        height=args.height,
        bg_color=args.bg_color,
        circle_color=args.circle_color
    )
    
    # Calcul du nombre total de points
    total_draws = args.nb_threads * args.nb_draws
    logging.info(f"Génération de {total_draws} points avec {args.nb_threads} thread(s)")
    
    # Création du gestionnaire de threads
    manager = ThreadingManager(
        nb_threads=args.nb_threads,
        nb_draws_per_thread=args.nb_draws,
        seed=args.seed
    )
    
    # Premier affichage
    ui.update()
    
    # Lancement de la simulation dans un thread séparé
    import threading
    
    def simulation_thread():
        """Thread pour exécuter la simulation sans bloquer la GUI"""
        manager.run_parallel(callback=ui.add_point_callback)
        logging.info("Simulation terminée")
    
    sim_thread = threading.Thread(target=simulation_thread)
    sim_thread.start()
    
    # Boucle principale de la GUI
    running = True
    clock = pygame.time.Clock()
    
    while running:
        running = ui.handle_events()
        ui.update()
        clock.tick(60)  # 60 FPS
        
        # Vérifier si la simulation est terminée
        if not sim_thread.is_alive() and ui.total_points >= total_draws:
            # Petit délai pour voir le résultat final
            pygame.time.wait(100)
    
    # Attendre la fin du thread de simulation
    sim_thread.join()
    
    # Calcul final
    pi_estimate = MonteCarloSimulation.estimate_pi(ui.total_points, ui.inside_points)
    
    # Affichage du résultat
    result = f"π ≈ {pi_estimate:.10f}"
    write_output(args.output, result)
    
    logging.info(f"Points totaux: {ui.total_points}")
    logging.info(f"Points dans le quadrant: {ui.inside_points}")
    logging.info(f"Estimation de π: {pi_estimate:.10f}")
    
    ui.close()


def run_cli_mode(args):
    """
    Exécute la simulation en mode ligne de commande (sans GUI)
    
    Args:
        args: Arguments parsés
    """
    logging.info("Exécution en mode CLI (sans GUI)")
    
    # Calcul du nombre total de points
    total_draws = args.nb_threads * args.nb_draws
    logging.info(f"Génération de {total_draws} points avec {args.nb_threads} thread(s)")
    
    if args.seed is not None:
        logging.info(f"Utilisation de la graine: {args.seed}")
    
    # Création du gestionnaire de threads
    manager = ThreadingManager(
        nb_threads=args.nb_threads,
        nb_draws_per_thread=args.nb_draws,
        seed=args.seed
    )
    
    # Lancement de la simulation
    logging.info("Démarrage de la simulation...")
    total_points, inside_points = manager.run_parallel()
    
    # Calcul de π
    pi_estimate = MonteCarloSimulation.estimate_pi(total_points, inside_points)
    
    # Affichage des résultats
    logging.info(f"Points totaux: {total_points}")
    logging.info(f"Points dans le quadrant: {inside_points}")
    logging.info(f"Ratio: {inside_points/total_points:.6f}")
    logging.info(f"Estimation de π: {pi_estimate:.10f}")
    
    # Écriture du résultat
    result = f"π ≈ {pi_estimate:.10f}"
    write_output(args.output, result)