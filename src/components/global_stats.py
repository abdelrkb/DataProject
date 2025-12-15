from dash import html

stats_component = html.Div(
    [
        html.Div(
            [
                html.Div("67M", className="stat-number"),
                html.Div("Habitants en France", className="stat-text"),
            ],
            className="stat-box",
        ),

        html.Div(
            [
                html.Div("40+", className="stat-number"),
                html.Div("Millions de cas cumulés", className="stat-text"),
            ],
            className="stat-box",
        ),

        html.Div(
            [
                html.Div("160k", className="stat-number"),
                html.Div("Décès liés au Covid-19", className="stat-text"),
            ],
            className="stat-box",
        ),
    ],
    className="stats-container",
)
