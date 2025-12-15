from dash import html
from src.components.graphs.hospitalisations import hospitalisation_component
from src.components.header import header_component
from src.components.global_stats import stats_component

layout = html.Div([
    header_component,
    stats_component,
    hospitalisation_component
],
className="container" 
)
