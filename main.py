import re

import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

from data import TabData
from frontend.aggrids import render_authors, render_best_client, render_revenue
from frontend.cards import card_content
from frontend.plots import plot_revenue
from frontend.styles import get_style

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

DIRS = ['DATA1', 'DATA2', 'DATA3']
data = {i: TabData(directory) for i, directory in enumerate(DIRS)}

sidebar = html.Div(
    [
        html.H2('Itransition', className='display-6'),
        html.Hr(),
        html.P('Dashboard', className='lead'),
        dbc.Nav(
            [dbc.NavLink(f'Data {k + 1}', href=f'/page/{k + 1}', active='exact') for k in data],
            vertical=True,
            pills=True,
        ),
    ],
    style=get_style('sidebar'),
)

content = html.Div(id='page-content', style=get_style('content'))

app.layout = html.Div([dcc.Location(id='url'), sidebar, content])


@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def render_page_content(pathname: str) -> html.Div:
    if re.match(r'/page/[123]', pathname):
        return page_content(int(pathname[-1]) - 1)
    return html.Div(
        [
            html.H1('404: Not found', className='text-danger'),
            html.Hr(),
            html.P(f'The pathname {pathname} was not recognised...'),
        ],
        className='p-3 bg-light rounded-3',
    )


def page_content(page_id: int) -> html.Div:
    daily_revenue = data[page_id].daily_revenue()
    no_unique_users = len(data[page_id].users)
    no_unique_authors = len(data[page_id].books['author'].unique())
    best_revenues = daily_revenue.nlargest(5, 'paid_price')
    most_popular_authors = data[page_id].most_popular_authors()
    best_client = data[page_id].best_client()
    return html.Div(
        id='page',
        children=[
            html.H1(f'Data {page_id + 1}', className='text-primary'),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Stack(
                            [
                                dbc.Card(
                                    card_content('Unique users', '', no_unique_users),
                                    color='primary',
                                    inverse=True,
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        card_content('Unique authors', '', no_unique_authors),
                                        color='secondary',
                                        inverse=True,
                                    ),
                                ),
                            ],
                            gap=4,
                        ),
                        align='center',
                        width=2,
                    ),
                    dbc.Col(
                        dbc.Spinner(plot_revenue(daily_revenue), color='primary'),
                        align='left',
                        width=10,
                    ),
                ],
                justify='evenly',
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3('Best revenues', className='text-primary'),
                            render_revenue(best_revenues),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Stack(
                            [
                                html.H3('Most popular authors set', className='text-primary'),
                                render_authors(most_popular_authors),
                                html.Hr(),
                                html.H3('Best client', className='text-primary'),
                                render_best_client(best_client),
                            ],
                            gap=2,
                        ),
                        width=8,
                    ),
                ],
            ),
        ],
        className='p-3 bg-light rounded-3',
    )


if __name__ == '__main__':
    app.run(debug=True)
