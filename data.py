from typing import Literal

import pandas as pd

from aliases import AliasNetwork, divide_users
from parsers.books import get_books
from parsers.orders import get_orders
from parsers.users import get_users


class TabData:
    books: pd.DataFrame
    orders: pd.DataFrame
    users: pd.DataFrame
    aliases: AliasNetwork

    def __init__(self, catalog: Literal['DATA1', 'DATA2', 'DATA3']):
        self.books, orders, users = get_books(catalog), get_orders(catalog), get_users(catalog)
        users_with_aliases, unique_users = divide_users(users)
        self.aliases = AliasNetwork(users_with_aliases)
        orders['user_id'] = orders['user_id'].replace(self.aliases.get_lookup())
        self.orders = orders
        unique_users_with_aliases = users.loc[self.aliases.get_unique_users()]
        self.users = pd.concat([unique_users, unique_users_with_aliases])

    def daily_revenue(self) -> pd.Series:
        return self.orders.groupby('date').agg({'paid_price': 'sum'})

    def most_popular_authors(self) -> pd.Series:
        return (
            self.orders[['book_id', 'quantity']]
            .join(self.books['author'], on='book_id')
            .groupby('author')
            .agg({'quantity': 'sum'})
            .nlargest(1, 'quantity')
        )

    def best_client(self) -> pd.DataFrame:
        user = (
            self.orders[['user_id', 'paid_price']]
            .join(self.users, on='user_id')
            .groupby('user_id')
            .agg({'paid_price': 'sum'})
            .nlargest(1, 'paid_price')
        )
        user_aliases = self.aliases.get_user_aliases(int(user.first_valid_index()))
        if user_aliases is not None:
            return user_aliases
        return pd.DataFrame(self.users.loc[user.index[0]].to_dict(), index=[0])
