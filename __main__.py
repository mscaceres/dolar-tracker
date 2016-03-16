import sys
import scraping
import plot
import persitence


def main():
    history = persitence.load_history(persitence.HISTORY_FILE)
    for source, scrap_page in scraping.get_scrap_functions():
        history.add_point(source, scrap_page())
    plot.make_dolar_dashboard(history)
    persitence.save_history(history, persitence.HISTORY_FILE)

if __name__ == "__main__":
    sys.exit(main())
