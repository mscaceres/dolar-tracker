import pickle
import dollar_tracker.dollar_history

HISTORY_FILE = "dollar_history.pkl"


def save_history(history, path):
    with open(path, 'wb') as output:
        pickle.dump(history, output)


def load_history(path):
    history_obj = None
    try:
        with open(path, 'rb') as input:
            history_obj = pickle.load(input)
    except IOError:
        history_obj = dollar_tracker.dollar_history.DolarHistory()
    return history_obj