"""dollar-tracker: review the dollar price history from many sources in a consolidated graphic

Usage:
    dollar-tracker (track|plot) [--path=<path>]

Options:
    -h --help   shows this screen
    --version   shows version
    --path=<path>   specifies a path to save a new data o plot from there. [default: ./]
"""

import sys
import os.path
import logging
import logging.config
import json
from docopt import docopt
from dollar_tracker import scraping
from dollar_tracker import plot
from dollar_tracker import persitence

log = logging.getLogger(__name__)


def conifg_logs(path=None):
    #TODO figure out way to run it from a local machine
    if path is None:
        path = "/root/.config/dollar-tracker/logs.json"
    with open(path) as f:
        c = f.read()
        config = json.loads(c)
        logging.config.dictConfig(config)


def log_indicators(history):
    buy_indicators, sell_indicators = history.get_indicators_by_date()
    log.info("""
    Compra
    =======
    Precio Promedio: {0}
    Variacion del dia: {1}
    Vaiacion del mes: {2}

    Venta
    ======
    Precio Promedio: {3}
    Variacion del dia: {4}
    Vaiacion del mes: {5}
    """.format(*buy_indicators, *sell_indicators))

def main():
    try:
        conifg_logs()
        args = docopt(__doc__, version='1.0.0.dev1')
        history_path = os.path.join(args['--path'], persitence.HISTORY_FILE)
        history = persitence.load_history(history_path)
        if args['track']:
            for source, scrap_page_func in scraping.get_scrap_functions():
                history.add_point(source, scrap_page_func())
            log_indicators(history)
        elif args['plot']:
            plot.make_dolar_dashboard(history)
        persitence.save_history(history, history_path)
    except Exception as e:
        log.exception("An error has ocurred while runing the program", e.__cause__)
        return 1

if __name__ == "__main__":
    sys.exit(main())
