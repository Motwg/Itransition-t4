from functools import partial
from itertools import combinations

import networkx as nx
import pandas as pd


def is_dup(first: pd.Series, second: pd.Series, diff_threshold: int) -> bool:
    return len(first.compare(second)) <= diff_threshold


def compute_aliases(user: pd.Series, aliases: pd.DataFrame) -> pd.Series:
    is_alias = partial(is_dup, second=user, diff_threshold=1)
    return aliases[aliases.apply(is_alias, axis=1)]


def divide_users(users: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    combs = combinations(users.columns, len(users.columns) - 1)
    dup_mask = pd.Series()
    for comb in combs:
        dup_mask = users.duplicated(subset=comb, keep=False) | dup_mask
    users_with_aliases = users.loc[dup_mask]
    unique_users = users.loc[~dup_mask]
    return users_with_aliases, unique_users


class AliasNetwork:
    network: nx.Graph
    aliases: pd.DataFrame

    def __init__(self, users_with_aliases: pd.DataFrame) -> None:
        self.network = nx.Graph()
        self.aliases = users_with_aliases
        for user_id, user in users_with_aliases.iterrows():
            for neigbour_id in compute_aliases(user, users_with_aliases).index:
                self.network.add_edge(user_id, neigbour_id)

    def get_user_aliases(self, user_id: int) -> pd.DataFrame | None:
        try:
            idx = [*nx.descendants(self.network, user_id), user_id]
            return self.aliases.loc[idx]
        except nx.exception.NetworkXError:
            return None

    def get_unique_users(self) -> pd.Series:
        return pd.Series(next(iter(group)) for group in nx.connected_components(self.network))

    def get_lookup(self) -> dict[int, int]:
        lookup = {}
        for group in nx.connected_components(self.network):
            unique = next(iter(group))
            lookup.update(dict.fromkeys(group, unique))
        return lookup
