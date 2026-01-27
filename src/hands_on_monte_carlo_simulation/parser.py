import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Monte Carlo Simulation Parameters",
                                     add_help=False)
    #paramètres pour GUI 
    parser.add_argument('--line_width', type=int, default=5,
                        help='The line width for the GUI window. Default is 5 pixels.')
    parser.add_argument('--width', type=int, default=800,
                        help='The width of the GUI window. Default is 800 pixels.')
    parser.add_argument('--height', type=int, default=600,
                        help='The height of the GUI window. Default is 600 pixels.')
    parser.add_argument('--bg-color', type=str, default='white',
                        help='The background color of the GUI window. Default is white.')
    parser.add_argument('--circle-color', type=str, default='black',
                        help='The color of the quadrant circle in the GUI. Default is black.')
    parser.add_argument('--screen', type=str, default='main',
                        help='The screen to display the quadrant circle on. Default is "main".')

    #Command line arguments
    parser.add_argument('-h', '--help', action='help',
                        help='Show an help message with all command line arguments and their descriptions, and exit.')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='Increase verbosity level. -v for information, -vv for debug. By default only warning and error log messages are printed.')
    parser.add_argument('-o', '--output', type=str, default='-',
                        help='The output file in which to write the result. - is the default and means to print on stdout.')
    parser.add_argument('-n', '--nb-threads', type=int, default=1,
                        help='The number of threads to run.')
    parser.add_argument('-N', '--nb-draws', type=int, default=1000,
                        help='The number of random draws for each thread.')
    parser.add_argument('-x', '--gui', action='store_true',
                        help='Enable GUI display. By default, no GUI window is opened.')
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help='An optional seed for the random number generator to ensure reproducibility.'
                        )
    
    return parser.parse_args()
