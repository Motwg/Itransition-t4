import dash_ag_grid as dag
import pandas as pd


def render_authors(most_popular_authors: pd.DataFrame) -> dag.AgGrid:
    most_popular_authors['author'] = most_popular_authors.index
    return dag.AgGrid(
        rowData=most_popular_authors.to_dict('records'),
        columnDefs=[{'field': i} for i in most_popular_authors.columns],
        style={'height': 90},
    )


def render_best_client(best_client: pd.DataFrame) -> dag.AgGrid:
    return dag.AgGrid(
        rowData=best_client.to_dict('records'),
        columnDefs=[{'field': i} for i in best_client.columns],
        style={'height': 200},
    )


def render_revenue(best_revenues: pd.DataFrame) -> dag.AgGrid:
    best_revenues['day'] = best_revenues.index
    return dag.AgGrid(
        rowData=best_revenues.to_dict('records'),
        columnDefs=[
            {
                'field': 'day',
                'headerName': 'Day',
            },
            {
                'field': 'paid_price',
                'headerName': 'Revenue',
                'type': 'rightAligned',
                'valueFormatter': {
                    'function': "d3.format('($,.2f')(params.value ? params.value/100 : 0 )",
                },
            },
        ],
        style={'height': 350},
    )
