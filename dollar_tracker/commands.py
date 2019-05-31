from abc import ABC, abstractmethod
import sys

from dollar_tracker.dollar_history import DollarHistory
from dollar_tracker.scrap import scrapped_dolar_points, list_sources

from docopt import docopt


def today_avg_values():
    with DollarHistory.from_pickle() as history:
        return history.today_avg_values()

# this could be done using decorators.. maybe the interface is cleaner than this
class Command(ABC):
    VALID_COMMANDS = {}
    CMD_NAME = None

    def __init_subclass__(cls):
        name = cls.CMD_NAME or cls.__name__.lower()
        Command.VALID_COMMANDS[name] = cls()

    @classmethod
    def is_valid(cls, cmd):
        return cmd.split()[0] in cls.VALID_COMMANDS

    @classmethod
    def all_commands(cls):
        return cls.VALID_COMMANDS.values()

    def __call__(self, *args, **kwargs):
        try:
            args = docopt(self.__doc__, argv=args)
        except SystemExit:
            return []
        return self.body(**args)

    @abstractmethod
    def body(self, **kwargs):
        raise NotImplemented


class quit(Command):
    """
Quits dollar tracker REPL
Usage:
    q
    """
    CMD_NAME = 'q'

    def body(self, **args):
        raise sys.exit(0)


class fetch(Command):
    """
Fetch dollar information from scrapped pages
Usage:
    fetch
    """

    def body(self, **kwargs):
        values = []
        with DollarHistory.from_pickle() as history:
            for source, value in scrapped_dolar_points():
                history.add_point(source, value)
                values.append((source, value.date, value.buy_price, value.sell_price))
        return values


class list(Command):
    """
List the sources from where dollar information will be fetched
Usage:
    ls
    """
    CMD_NAME = "ls"

    def body(self, **kwargs):
        return list_sources()
