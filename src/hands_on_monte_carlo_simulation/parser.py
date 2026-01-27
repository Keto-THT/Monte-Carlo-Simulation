import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Monte Carlo Simulation Parameters")
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
