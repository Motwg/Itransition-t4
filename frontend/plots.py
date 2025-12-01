import base64
import io

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from dash import html
from matplotlib.figure import Figure


def fig_to_buffer(fig: Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    fig_data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return f'data:image/png;base64,{fig_data}'


def smooth(scalars: list[float], weight: float) -> list[float]:
    last, smoothed = scalars[0], []
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point
        smoothed.append(smoothed_val)
        last = smoothed_val
    return smoothed


def fill_missing_idx_dates(date_idx: pd.Series, fill_with: int = 0) -> pd.Series:
    date_idx.index = pd.DatetimeIndex(date_idx.index)
    idx = pd.date_range(date_idx.index.min(), date_idx.index.max())
    return date_idx.reindex(idx, fill_value=fill_with)


def plot_revenue(daily_revenue: pd.Series) -> html.Img:
    daily_revenue = fill_missing_idx_dates(daily_revenue)
    x, y = daily_revenue.index, daily_revenue['paid_price'].apply(lambda x: x / 100)

    fig, ax = plt.subplots()
    fig.set_figheight(3)
    fig.set_figwidth(12)
    _ = ax.set(ylabel='Revenue [$]', title='Daily revenue')
    _ = ax.plot(x, smooth(y, 0.9))
    _ = ax.plot(x, y, 'b.', markersize=3)
    _ = ax.set_ylim(ymin=0)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.grid(True)
    return html.Img(id='line-plot', src=fig_to_buffer(fig))
