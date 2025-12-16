from dash import html
from src.components.header import header_component
from src.components.stats_component import StatsComponent
from src.components.hospitalisations_component import HospitalisationsComponent
from src.pages.base_page import BasePage

class HomePage(BasePage): 
    
    stats_component = StatsComponent()
    hospitalisations_component = HospitalisationsComponent()

    layout = html.Div([
        header_component,
        stats_component.layout(),
        hospitalisations_component.layout()
    ],
    className="container" 
    )

    def register_callbacks(app):
        stats = StatsComponent()
        hospitalisations = HospitalisationsComponent()

        stats.register_callbacks(app)
        hospitalisations.register_callbacks(app)
