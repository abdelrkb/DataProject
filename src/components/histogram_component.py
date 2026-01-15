from dash import html, dcc, Input, Output
import plotly.express as px

from src.components.base.base_component import BaseComponent
from src.services.histogram_service import HistogramService


class HistogramComponent(BaseComponent):
    """
    Crée un composant Dash pour afficher des histogrammes des indicateurs COVID-19
    """

    def __init__(self):
        super().__init__(service=HistogramService())
        # Dictionnaire des méthodes d'histogramme, utilisé pour générer les callbacks et layouts
        self.histogram_methods = {
            "hosp": {
                "label": "Hospitalisations moyennes par mois",
                "column": "hosp",
                "x_column": "mois",
                "method": self.service.hosp_par_mois,
                "chart_type": "bar",
            },
            "deces": {
                "label": "Décès hospitaliers par mois",
                "column": "incid_dchosp",
                "x_column": "mois",
                "method": self.service.deces_par_mois,
                "chart_type": "bar",
            },
        }

    def layout(self):
        """
        Layout HTML du composant Histogramme
        """
        return html.Div(
            [
                html.H3(
                    "Histogramme indicateur du COVID-19", style={"textAlign": "center"}
                ),
                html.Div(
                    [
                        self.histogram_card(key, config)
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

    def histogram_card(self, key, config):
        """
        Carte HTML pour un histogramme spécifique

         :param key: clé dans le dict histogram_methods
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

                chart_type = conf.get("chart_type", "histogram")

                if chart_type == "bar":
                    x_col = conf.get("x_column", "mois")
                    fig = px.bar(
                        df,
                        x=x_col,
                        y=conf["column"],
                        title=f"{conf['label']} — {label}",
                        labels={
                            conf["column"]: conf["label"],
                            x_col: "Mois",
                        },
                    )
                    fig.update_layout(
                        title_x=0.5,
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                    )
                else:
                    fig = px.histogram(
                        df,
                        x=conf["column"],
                        nbins=30,
                        title=f"{conf['label']} — {label}",
                        labels={
                            conf["column"]: conf["label"],
                            "count": "Nombre de jours",
                        },
                    )
                    fig.update_layout(
                        title_x=0.5,
                        yaxis_title="Nombre de jours",
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                    )

                return fig
