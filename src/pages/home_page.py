from dash import html
from src.pages.base.base_page import BasePage
from src.components.sidebar_component import SidebarComponent
from src.components.dashboard_map_component import DashboardMapComponent


class HomePage(BasePage):
    """
    Page principale du dashboard COVID-19
    Layout en deux colonnes : sidebar (gauche) + carte (droite)
    """

    def __init__(self):
        self.sidebar = SidebarComponent()
        self.map_component = DashboardMapComponent()

    def layout(self):
        """
        Layout principal avec structure sidebar + carte
        """
        return html.Div(
            [
                self.sidebar.layout(),
                self.map_component.layout(),
            ],
            className="dashboard-layout",
        )

    def register_callbacks(self, app):
        """
        Enregistrer tous les callbacks des composants
        """
        self.sidebar.register_callbacks(app)
        self.map_component.register_callbacks(app)
