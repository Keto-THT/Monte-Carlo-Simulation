import pygame
from .parser import parse_arguments
from .quadrant_circle import draw_quadrant_circle

def main() -> None:
    args = parse_arguments()
    print(f"Parsed arguments: {args}")

    #on vérifie si on active le mode GUI avec l'argument -x
    if args.gui:
        print("Initializing GUI...")
        pygame.init()

        #Création de la fenêtre
        screen = pygame.display.set_mode((args.width, args.height))
        pygame.display.set_caption("Monte Carlo Simulation")

        #Configuration des couleurs et variables
        bg_color = args.bg_color
        circle_color = args.circle_color
        line_width = args.line_width
        running = True

        
        while running:
           
            for event in pygame.event.get():

                #Fermer la fenêtre
                if event.type == pygame.QUIT:
                    running = False
            

            screen.fill(bg_color)                 
            draw_quadrant_circle(screen, circle_color, line_width) 
            
            # Rafraîchissement de l'écran
            pygame.display.flip()

        # Fermeture de Pygame
        pygame.quit()

    else:
        print("Hello from hands-on-monte-carlo-simulation!")
        print("Mode CLI activé (pas de fenêtre graphique). Utilisez -x pour le GUI.")

