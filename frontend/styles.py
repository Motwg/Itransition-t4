def get_style(style_name: str) -> dict[str, str | int]:
    return {
        'sidebar': {
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'bottom': 0,
            'width': '16rem',
            'padding': '2rem 1rem',
            'background-color': '#DFE0E1',
        },
        'content': {
            'margin-left': '18rem',
            'margin-right': '2rem',
            'padding': '2rem 1rem',
        },
    }.get(style_name)
