from dash import html, dcc, Input, Output
import plotly.express as px
from src.components.base.base_component import BaseComponent
from src.services.graphs_service import GraphService


class GraphsComponent(BaseComponent):
    """
    Crée un composant Dash pour afficher des graphs des indicateurs COVID-19
    """

    def __init__(self):
        super().__init__(GraphService())

        self.graphs_methods = {
            "hospitalisations": {
                "label": "Hospitalisations COVID-19",
                "column": "hosp",
                "method": self.service.hospitalisations,
            },
            "taux_mortalite": {
                "label": "Taux de mortalité COVID-19 (%)",
                "column": "taux_mortalite",
                "method": self.service.taux_mortalite,
            },
        }

    def layout(self):
        """
        Composant HTML pour les graphs des hospitalisations COVID-19
        """
        return html.Div(
            [
                html.H3(
                    "Graphiques indicateurs du COVID-19", style={"textAlign": "center"}
                ),
                html.Div(
                    [
                        self.graph_card(key, config)
                        for key, config in self.graphs_methods.items()
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

    def graph_card(self, key, config):
        """
        Docstring pour graph_card

        :param key: clé dans le dict graphs_methods
        :param config: config dans le dict key

        :return: html.Div
        """
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
        for key, config in self.graphs_methods.items():

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
            def update_histogram(scope, region, dep, conf=config):
                if scope == "region":
                    df = conf["method"](region=region)
                    label = region or "Région"
                elif scope == "dep":
                    df = conf["method"](dep=dep)
                    label = dep or "Département"
                else:
                    df = conf["method"]()
                    label = "France entière"

                fig = px.line(
                    df,
                    x="date",
                    y=conf["column"],
                    title=f"{conf['label']} — {label}",
                    labels={conf["column"]: conf["label"], "date": "Date"},
                    template="plotly_white",
                )
                fig.update_layout(title_x=0.5)

                return fig
