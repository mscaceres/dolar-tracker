from pathlib import Path
from dollar_history import DollarHistory


def to_json(path):
    """Migrate data from pickle file to json"""
    migrated = None
    with DollarHistory.pkl_context(path) as pkl:
        migrated = pkl

    new_path = Path(path).with_suffix(".json")
    with DollarHistory.json_context(new_path) as json:
        # json dict keys can only be strings and there is no hook to enable a convertion,
        # so we need to pre-process it before
        for dicts in ('_points', '_max_points', '_min_points', '_avg_points'):
            for price in ('buy_prices', 'sell_prices'):
                price_obj = getattr(migrated, price)
                dict_obj = getattr(price_obj, dicts)
                for d in list(dict_obj):
                    dict_obj[d.isoformat()] = dict_obj[d]
                    dict_obj.pop(d)

        json.buy_prices = migrated.buy_prices
        json.sell_prices = migrated.sell_prices


def to_pickle(path):
    """Migrate data from json file to pkl"""
    migrated = None
    with DollarHistory.json_context(path) as json:
        migrated = json

    new_path = Path(path).with_suffix(".pkl")
    with DollarHistory.pkl_context(new_path) as pkl:
        pkl.buy_prices = migrated.buy_prices
        pkl.sell_prices = migrated.sell_prices
