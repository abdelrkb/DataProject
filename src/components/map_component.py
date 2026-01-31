from dash import html, dcc, Input, Output
from src.components.base.base_component import BaseComponent
from src.services.map_service import MapService


class MapComponent(BaseComponent):
    def __init__(self):
        super().__init__(service=MapService())
        self.map_methods = {
            "hospitalisations_map": {
                "label": "Carte des décès totaux",
                "method": self.service.deces_map_html,
            },
            "reanimations_map": {
                "label": "Carte des hospitalisations totales",
                "method": self.service.hospitalisations_map_html,
            },
        }

    def layout(self):
        return html.Div(
            [
                html.H3(
                    "Cartes indicateurs du COVID-19", style={"textAlign": "center"}
                ),
                html.Div(
                    [
                        self.map_card(key, config)
                        for key, config in self.map_methods.items()
                    ],
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(420px, 1fr))",
                        "gap": "20px",
                        "marginTop": "20px",
                        "height": "550px",
                    },
                ),
            ]
        )

    def map_card(self, key, config):
        initial_map = config["method"](level="region", start_date=None, end_date=None)

        return html.Div(
            [
                html.H4(config["label"], style={"textAlign": "center"}),
                dcc.Dropdown(
                    id=self.cid(f"{key}-level"),
                    options=[
                        {"label": "Régions", "value": "region"},
                        {"label": "Départements", "value": "dep"},
                    ],
                    value="region",
                    clearable=False,
                    style={"marginBottom": "10px"},
                ),
                dcc.DatePickerRange(
                    id=self.cid(f"{key}-dates"),
                    display_format="YYYY-MM-DD",
                    style={"marginBottom": "10px"},
                    min_date_allowed="2020-04-01",
                    max_date_allowed="2023-06-30",
                    start_date="2020-04-01",
                    end_date="2023-06-30",
                ),
                html.Iframe(
                    id=self.cid(f"{key}-map"),
                    srcDoc=initial_map,
                    style={
                        "width": "100%",
                        "height": "600px",
                        "border": "none",
                        "pointerEvents": "auto",
                    },
                ),
            ],
            style={
                "padding": "15px",
                "boxSizing": "border-box",
                "border": "1px solid #e0e0e0",
                "borderRadius": "10px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.05)",
                "overflow": "hidden",
            },
        )

    def register_callbacks(self, app):
        for key, config in self.map_methods.items():

            @app.callback(
                Output(self.cid(f"{key}-map"), "srcDoc"),
                Input(self.cid(f"{key}-level"), "value"),
                Input(self.cid(f"{key}-dates"), "start_date"),
                Input(self.cid(f"{key}-dates"), "end_date"),
            )
            def update_map(level, start_date, end_date, conf=config):
                return conf["method"](
                    level=level,
                    start_date=start_date,
                    end_date=end_date,
                )
