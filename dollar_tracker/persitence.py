import pickle
import logging
import dollar_tracker.dollar_history

log = logging.getLogger(__name__)

HISTORY_FILE = "dollar_history.pkl"


def save_history(history, path):
    with open(path, 'wb') as output:
        pickle.dump(history, output)
        log.info("Saving History to {}".format(path))


def load_history(path):
    history_obj = None
    try:
        with open(path, 'rb') as input:
            history_obj = pickle.load(input)
    except IOError:
        log.warning("Path {} not found. Creating a new History instance".format(path))
        history_obj = dollar_tracker.dollar_history.DolarHistory()
    return history_obj