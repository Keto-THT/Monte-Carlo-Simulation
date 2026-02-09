import sys
import logging
from .parser import parse_arguments
from .Simulation import SimulationUI
from .threading_manager import ThreadingManager
from .monte_carlo import MonteCarloCalculator





def main() -> None:
    """
    Point d'entrée principal du programme
    """
    args = parse_arguments()
    
    # Configuration du logging
    setup_logging(args.verbose)
    
    # Affichage des paramètres
    logging.debug(f"Paramètres: {args}")
    
    # Vérification des arguments
    if args.nb_threads < 1:
        logging.error("Le nombre de threads doit être >= 1")
        sys.exit(1)
    
    if args.nb_draws < 1:
        logging.error("Le nombre de tirages doit être >= 1")
        sys.exit(1)
    
    # Exécution selon le mode
    try:
        if args.gui:
            # Import pygame seulement si nécessaire
            import pygame
            run_gui_mode(args)
        else:
            run_cli_mode(args)
    
    except KeyboardInterrupt:
        logging.info("\nSimulation interrompue par l'utilisateur")
        sys.exit(0)
    
    except Exception as e:
        logging.error(f"Erreur lors de l'exécution: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
