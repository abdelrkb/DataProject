from dash import html, dcc, Input, Output
import plotly.express as px

from src.components.base.base_component import BaseComponent
from src.services.histogram_service import HistogramService


class HistogramComponent(BaseComponent):
    def __init__(self):
        super().__init__(service=HistogramService())
        self.regions = self.reference_service.available_regions()
        self.departements = self.reference_service.available_dep()

        self.histogram_methods = {
            "hosp": {
                "label": "Hospitalisation",
                "column": "hosp",
                "method": self.service.hosp_distribution,
            },
            "taux_mortalite": {
                "label": "Taux de mortalité (%)",
                "column": "taux_mortalite",
                "method": self.service.taux_mortalite_distribution,
            },
        }

    def layout(self):
        return html.Div(
            [
                html.H3(
                    "Histogramme indicateur du COVID-19", style={"textAlign": "center"}
                ),
                html.Div(
                    [
                        self._histogram_card(key, config)
                        for key, config in self.histogram_methods.items()
                    ],
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(420px, 1fr))",
                        "gap": "20px",
                        "marginTop": "20px",
                    },
                ),
            ]
        )

    def _histogram_card(self, key, config):
        return html.Div(
            [
                html.H4(config["label"], style={"textAlign": "center"}),
                dcc.Dropdown(
                    id=self.cid(f"{key}-scope"),
                    options=[
                        {"label": "France entière", "value": "fr"},
                        {"label": "Région", "value": "region"},
                        {"label": "Département", "value": "dep"},
                    ],
                    value="fr",
                    clearable=False,
                ),
                dcc.Dropdown(
                    id=self.cid(f"{key}-region"),
                    options=[{"label": r, "value": r} for r in self.regions],
                    placeholder="Région",
                    disabled=True,
                ),
                dcc.Dropdown(
                    id=self.cid(f"{key}-dep"),
                    options=[{"label": d, "value": d} for d in self.departements],
                    placeholder="Département",
                    disabled=True,
                ),
                dcc.Graph(
                    id=self.cid(f"{key}-graph"),
                    style={"height": "350px"},
                ),
            ],
            style={
                "padding": "15px",
                "boxSizing": "border-box",
                "border": "1px solid #e0e0e0",
                "borderRadius": "10px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.05)",
            },
        )

    def register_callbacks(self, app):
        for key, config in self.histogram_methods.items():

            @app.callback(
                Output(self.cid(f"{key}-region"), "disabled"),
                Output(self.cid(f"{key}-dep"), "disabled"),
                Input(self.cid(f"{key}-scope"), "value"),
            )
            def toggle_dropdowns(scope):
                return scope != "region", scope != "dep"

            @app.callback(
                Output(self.cid(f"{key}-graph"), "figure"),
                Input(self.cid(f"{key}-scope"), "value"),
                Input(self.cid(f"{key}-region"), "value"),
                Input(self.cid(f"{key}-dep"), "value"),
            )
            def update_histogram(scope, region, dep, _config=config):
                if scope == "region":
                    df = _config["method"](region=region)
                    label = region or "Région"
                elif scope == "dep":
                    df = _config["method"](dep=dep)
                    label = dep or "Département"
                else:
                    df = _config["method"]()
                    label = "France entière"

                fig = px.histogram(
                    df,
                    x=_config["column"],
                    nbins=30,
                    title=f"{_config['label']} — {label}",
                )
                fig.update_layout(title_x=0.5)

                return fig
