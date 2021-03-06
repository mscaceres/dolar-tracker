import calendar
import plotly.graph_objs
import plotly.tools
import plotly.offline


def to_day_str(dates):
    return [d.strftime("%Y-%m-%d") for d in dates]


def make_dolar_dashboard(dolar_history):
    fig = plotly.tools.make_subplots(2, 2,
                                     subplot_titles=("Precio de Compra",
                                                     "Precio de Venta",
                                                     "Acumulado Mensual Compra",
                                                     "Acumulado Mensual Venta"),
                                     shared_yaxes=True)
    # plot max, min and avg buy price
    dates, max_buy_prices = zip(*dolar_history.buy_prices.max_points)
    _, min_buy_prices = zip(*dolar_history.buy_prices.min_points)
    _, avg_buy_prices = zip(*dolar_history.buy_prices.avg_points)
    dates = to_day_str(dates)
    max_line = plotly.graph_objs.Scatter(x=dates,
                                         y=max_buy_prices,
                                         mode="lines+markers",
                                         name="Maximo",
                                         line=dict(dash="dot"),
                                         connectgaps=True)
    min_line = plotly.graph_objs.Scatter(x=dates,
                                         y=min_buy_prices,
                                         mode="lines+markers",
                                         name="Minimo",
                                         line=dict(dash="dot"),
                                         connectgaps=True)
    avg_line = plotly.graph_objs.Scatter(x=dates,
                                         y=avg_buy_prices,
                                         mode="lines+markers",
                                         name="Promedio",
                                         line=dict(dash="solid"),
                                         connectgaps=True)

    fig.append_trace(max_line, 1, 1)
    fig.append_trace(min_line, 1, 1)
    fig.append_trace(avg_line, 1, 1)
    # plot %variation per day
    if dolar_history.buy_prices.day_variations:
        dates, variations = zip(*dolar_history.buy_prices.day_variations)
        dates = to_day_str(dates)
        var_line = plotly.graph_objs.Bar(x=dates,
                                         y=variations,
                                         name="% Variacion")
        fig.append_trace(var_line, 1, 1)

    # plot max, min, and avg sell price
    dates, max_sell_prices = zip(*dolar_history.sell_prices.max_points)
    _, min_sell_prices = zip(*dolar_history.sell_prices.min_points)
    _, avg_sell_prices = zip(*dolar_history.sell_prices.avg_points)
    dates = to_day_str(dates)
    max_line = plotly.graph_objs.Scatter(x=dates,
                                         y=max_sell_prices,
                                         mode="lines+markers",
                                         name="Maximo",
                                         line=dict(dash="dot"),
                                         connectgaps=True)
    min_line = plotly.graph_objs.Scatter(x=dates,
                                         y=min_sell_prices,
                                         mode="lines+markers",
                                         name="Minimo",
                                         line=dict( dash="dot"),
                                         connectgaps=True)
    avg_line = plotly.graph_objs.Scatter(x=dates,
                                         y=avg_sell_prices,
                                         mode="lines+markers",
                                         name="Promedio",
                                         line=dict(dash="solid"),
                                         connectgaps=True)
    fig.append_trace(max_line, 1, 2)
    fig.append_trace(min_line, 1, 2)
    fig.append_trace(avg_line, 1, 2)
    # plot %variation per day
    if dolar_history.sell_prices.day_variations:
        dates, variations = zip(*dolar_history.sell_prices.day_variations)
        dates = to_day_str(dates)

        var_line = plotly.graph_objs.Bar(x=dates,
                                             y=variations,
                                             name="% Variacion")
        fig.append_trace(var_line, 1, 2)


    # plot %variation accumulated per month
    if dolar_history.buy_prices.month_variations:
        months, variations = zip(*dolar_history.buy_prices.month_variations)
        var_line = plotly.graph_objs.Bar(x=list(map(lambda x: calendar.month_name[x], months)),
                                         y=variations,
                                         name="% Variacion")
        fig.append_trace(var_line, 2, 1)
    if dolar_history.sell_prices.month_variations:
        months, variations = zip(*dolar_history.sell_prices.month_variations)
        var_line = plotly.graph_objs.Bar(x=list(map(lambda x: calendar.month_name[x], months)),
                                         y=variations,
                                         name="% Variacion")
        fig.append_trace(var_line, 2, 2)

    # plot %variation accumulated per year
    plotly.offline.plot(fig)