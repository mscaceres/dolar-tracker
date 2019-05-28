"""dollar-tracker: review the dollar price history from many sources in a consolidated graphic

Usage:
    dollar-tracker (track|plot) [--path=<path>]

Options:
    -h --help   shows this screen
    --version   shows version
    --path=<path>   specifies a path to save a new data o plot from there. [default: ./]
"""

import datetime
import sys
import os.path
import logging
import logging.config
import json

from docopt import docopt
from dollar_tracker.scrap import scrapped_dolar_points, list_sources
from dollar_tracker import plot
from dollar_tracker.dollar_history import DollarHistory

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator
from prompt_toolkit.formatted_text import HTML

log = logging.getLogger(__name__)

HISTORY_FILE = "dollar_history.pkl"


def config_logs(path=None):
    #TODO figure out way to run it from a local machine
    if path is None:
        path = "/root/.config/dollar-tracker/logs.json"
    with open(path) as f:
        c = f.read()
        config = json.loads(c)
        logging.config.dictConfig(config)


def main():
    try:
        config_logs()
        args = docopt(__doc__, version='1.0.0.dev1')
        history_path = os.path.join(args['--path'], HISTORY_FILE)
        with DollarHistory.from_pickle(history_path) as history:
            if args['track']:
                for source, value in scrapped_dolar_points():
                    history.add_point(source, value)
            elif args['plot']:
                plot.make_dolar_dashboard(history)
    except Exception as e:
        log.exception("An error has occurred while running the program", e)
        return 1


def add_point():
        with DollarHistory.from_pickle(HISTORY_FILE) as history:
            for source, value in scrapped_dolar_points():
                history.add_point(source, value)
        return


commands = {'sources': list_sources,
            'track': add_point,
            'quit': None}


def _valid_cmd(text):
    return text in commands

valid_cmd = Validator.from_callable(_valid_cmd, error_message="Not a valid command")

def show_date():
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    return HTML("<b>{}</b>".format(date))

def format_text(cmd_output):
    formatted = ""
    for line in cmd_output:
        formatted = "<p><ansigreen>{}</ansigreen></p>".format(line)
        yield HTML(formatted)


def new_main():
    cmd_completer = WordCompleter(list(commands.keys()))
    session = PromptSession(completer=cmd_completer,
                            complete_while_typing=True,
                            validator=valid_cmd,
                            bottom_toolbar=show_date)
    while True:
        text = session.prompt("> ")
        cmd  = text.split()[0]
        if cmd == 'quit':
            print_formatted_text('Bye')
            break
        args = text.split()[1:]
        formatted_text = format_text(commands[cmd]())
        for text in formatted_text:
            print_formatted_text(text)


if __name__ == "__main__":
    sys.exit(new_main())
