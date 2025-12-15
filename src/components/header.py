from dash import html

header_component = html.Div(
    [   html.H1("COVID-19 en France", style={'textAlign': 'left', 'fontWeight': 300}),
        html.H2("Visualisation de données relatives au Covid 19 en France", style={"margin": "0", 'textAlign': 'left', 'fontWeight': 200}),
        html.P("Plus qu’un simple outil de visualisation, ce tableau de bord aide à comprendre comment l’épidémie n’affecte pas tous les Français de la même manière, en mettant en perspective les données de Santé publique France selon l’âge, le sexe et le territoire.", style={'textAlign': 'left'})
    ],
)