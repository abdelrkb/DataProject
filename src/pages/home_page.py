from dash import html
from src.components.header import header_component
from src.components.stats_component import StatsComponent
from src.components.hospitalisations_component import HospitalisationsComponent
from src.pages.base.base_page import BasePage


class HomePage(BasePage):
    def __init__(self):
        self.stats_component = StatsComponent()
        self.hospitalisations_component = HospitalisationsComponent()

    def layout(self):
        return html.Div(
            [
                header_component,
                self.stats_component.layout(),
                self.hospitalisations_component.layout(),
            ],
            className="container",
        )

    def register_callbacks(self, app):
        self.hospitalisations_component.register_callbacks(app)
