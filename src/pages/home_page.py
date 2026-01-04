from dash import html
from src.components.header import header_component
from src.components.stats_component import StatsComponent
from src.components.graphs_component import GraphsComponent
from src.pages.base.base_page import BasePage
from src.components.histogram_component import HistogramComponent


class HomePage(BasePage):
    def __init__(self):
        self.stats_component = StatsComponent()
        self.graphs_component = GraphsComponent()
        self.histogram_component = HistogramComponent()

    def layout(self):
        return html.Div(
            [
                header_component,
                self.stats_component.layout(),
                self.graphs_component.layout(),
                self.histogram_component.layout(),
            ],
            className="container",
        )

    def register_callbacks(self, app):
        self.graphs_component.register_callbacks(app)
        self.histogram_component.register_callbacks(app)
