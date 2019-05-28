
__all__ = ["scrapped_dolar_points", "list_sources"]

def scrapped_dolar_points():
    from .scrappers import DollarScrapper
    import logging
    log = logging.getLogger(__name__)
    for scrap_class in DollarScrapper.scrappers():
        scrapper = scrap_class()
        try:
            yield (scrapper.source, scrapper.scrap())
        except Exception as e:
            log.warn("%s is not working, %s", scrapper.source, e)


def list_sources():
    from .scrappers import DollarScrapper
    return list(DollarScrapper.scrappers_names())
