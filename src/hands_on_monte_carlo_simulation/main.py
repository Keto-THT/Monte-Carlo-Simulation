from .parser import parse_arguments
from .Simulation import SimulationUI

def main() -> None:
    args = parse_arguments()

    # Vérification du mode GUI
    if args.gui:
        print("Initializing GUI...")
        
        ui = SimulationUI(
            width=args.width, 
            height=args.height, 
            bg_color=args.bg_color, 
            circle_color=args.circle_color
        )

        running = True
        while running:
            running = ui.handle_events()
            ui.update()

        ui.close()

    else:
        print("Running in CLI mode (No GUI). Use -x to see the circle.")
