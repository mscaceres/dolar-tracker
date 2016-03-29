"""dollar-tracker: review the dollar price history from many sources in a consolidated

Usage:
    dollar-tracker (track|plot) [--path=<path>]

Options:
    -h --help   shows this screen
    --version   shows version
    --path=<path>   specifies a path to save a new data o plot from there. [default: ./]
"""

import sys
import os.path
from docopt import docopt
from dollar_tracker import scraping
from dollar_tracker import plot
from dollar_tracker import persitence



def main():
    args = docopt(__doc__,version='0.1')
    history = persitence.load_history(os.path.join(args['--path'],persitence.HISTORY_FILE))
    if  args['track']:
        for source, scrap_page in scraping.get_scrap_functions():
            history.add_point(source, scrap_page())
    elif args['plot']:
        plot.make_dolar_dashboard(history)
    persitence.save_history(history, persitence.HISTORY_FILE)

if __name__ == "__main__":
    sys.exit(main())
