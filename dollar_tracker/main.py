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
from dollar_tracker import plot
from dollar_tracker.dollar_history import DollarHistory
from dollar_tracker.commands import Command, today_avg_values

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


valid_cmd = Validator.from_callable(Command.is_valid, error_message="Not a valid command")

def toolbar_info():
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    buy, sell = today_avg_values()
    return HTML("<b>{} <ansigreen> Compra: {:.2f} </ansigreen>  <ansired> Venta: {:.2f} </ansired></b>".format(date, buy or 0.0, sell or 0.0))


# Each funcion we suppor in the REPL shall have a formatter for its output
def format_text(cmd_output):
    formatted = ""
    for line in cmd_output:
        formatted = "<p><ansigreen>{}</ansigreen></p>".format(line)
        yield HTML(formatted)


def new_main():
    cmd_completer = WordCompleter(list(Command.VALID_COMMANDS.keys()))
    session = PromptSession(completer=cmd_completer,
                            complete_while_typing=True,
                            validator=valid_cmd,
                            bottom_toolbar=toolbar_info,
                            validate_while_typing=False)
    while True:
        try:
            text = session.prompt("--> ")
            cmd  = text.split()[0]
            args = text.split()[1:]
            cmd_to_execute = Command.VALID_COMMANDS[cmd]
            formatted_text = format_text(cmd_to_execute(*args))
            for text in formatted_text:
                print_formatted_text(text)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    sys.exit(new_main())
