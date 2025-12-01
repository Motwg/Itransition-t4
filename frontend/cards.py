import dash_bootstrap_components as dbc
from dash import html


def card_content(header: str, title: str, body: str) -> list[dbc.CardHeader | dbc.CardBody]:
    return [
        dbc.CardHeader(header),
        dbc.CardBody(
            [
                html.H5(title, className='card-title'),
                html.P(
                    body,
                    className='card-text',
                ),
            ],
        ),
    ]
