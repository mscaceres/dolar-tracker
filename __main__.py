import sys
import pickle
import scraping
import plot
import dolar_history


HISTORY_FILE = "dolar_history.pkl"


def save_history(history, path):
    with open(path, 'wb') as output:
        pickle.dump(history, output)


def load_history(path):
    history_obj = None
    try:
        with open(path, 'rb') as input:
            history_obj = pickle.load(input)
    except IOError:
        history_obj = dolar_history.DolarHistory()
    return history_obj


def main():
    history = load_history(HISTORY_FILE)
    for source, scrap_page in scraping.get_scrap_functions():
        history.add_point(source, scrap_page())
    plot.make_dolar_dashboard(history)
    save_history(history, HISTORY_FILE)

if __name__ == "__main__":
    sys.exit(main())
