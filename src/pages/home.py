from dash import html
from src.components.graphs.hospitalisations import hospitalisation_component

layout = html.Div([
    html.H1("Dashboard COVID-19 France", style={'textAlign': 'center'}),
    hospitalisation_component
])
