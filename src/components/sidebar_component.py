from dash import html, dcc, Input, Output
import plotly.graph_objects as go
from src.components.base.base_component import BaseComponent
from src.services.graphs_service import GraphService
from src.services.histogram_service import HistogramService


class SidebarComponent(BaseComponent):
    """ """

    def __init__(self):
        super().__init__()
        self.graph_service = GraphService()
        self.histogram_service = HistogramService()

        self.stat_types = {
            "hosp": {
                "label": "Taux d'occupation des lits",
                "graph_method": self.graph_service.hospitalisations,
                "hist_method": self.histogram_service.nouvelles_hosp_par_mois,
                "graph_col": "hosp",
                "hist_col": "hosp",
                "unit": "lits",
            },
            "rea": {
                "label": "Taux de réanimation",
                "graph_method": self.graph_service.reanimations_mensuelles,
                "hist_method": self.histogram_service.nouvelles_hosp_par_mois,
                "graph_col": "rea",
                "hist_col": "hosp",
                "unit": "patients",
            },
            "deces": {
                "label": "Décès hospitaliers",
                "graph_method": self.graph_service.hospitalisations,
                "hist_method": self.histogram_service.deces_par_mois,
                "graph_col": "hosp",
                "hist_col": "incid_dchosp",
                "unit": "décès",
            },
        }

    def layout(self):
        """Layout de la sidebar"""
        return html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("🇫🇷", className="country-flag"),
                                html.Div("France", className="country-name"),
                            ],
                            className="sidebar-country",
                        ),
                        html.Div(
                            "COVID-19 dans les hopitaux en France",
                            className="sidebar-title",
                        ),
                        html.Div(
                            id=self.cid("main-label"),
                            children="Taux d'occupation des lits en réanimation",
                            className="sidebar-label",
                        ),
                    ],
                    className="sidebar-header",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "Niveau géographique", className="filter-label"
                                ),
                                dcc.Dropdown(
                                    id=self.cid("geo-level"),
                                    options=[
                                        {"label": "France entière", "value": "fr"},
                                        {"label": "Région", "value": "region"},
                                        {"label": "Département", "value": "dep"},
                                    ],
                                    value="fr",
                                    clearable=False,
                                ),
                            ],
                            className="filter-group",
                        ),
                        html.Div(
                            [
                                html.Label("Région", className="filter-label"),
                                dcc.Dropdown(
                                    id=self.cid("region"),
                                    options=[
                                        {"label": r, "value": r} for r in self.regions
                                    ],
                                    placeholder="Sélectionner une région",
                                    disabled=True,
                                ),
                            ],
                            className="filter-group",
                        ),
                        html.Div(
                            [
                                html.Label("Département", className="filter-label"),
                                dcc.Dropdown(
                                    id=self.cid("dep"),
                                    options=[
                                        {"label": d, "value": d}
                                        for d in self.departements
                                    ],
                                    placeholder="Sélectionner un département",
                                    disabled=True,
                                ),
                            ],
                            className="filter-group",
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Type de statistique", className="filter-label"
                                ),
                                dcc.Dropdown(
                                    id=self.cid("stat-type"),
                                    options=[
                                        {"label": v["label"], "value": k}
                                        for k, v in self.stat_types.items()
                                    ],
                                    value="hosp",
                                    clearable=False,
                                ),
                            ],
                            className="filter-group",
                        ),
                    ],
                    className="sidebar-filters",
                ),
                html.Div(
                    [
                        html.Div(
                            "Taux d'occupation",
                            className="graph-title",
                            id=self.cid("graph-title"),
                        ),
                        dcc.Graph(
                            id=self.cid("time-graph"),
                            config={"displayModeBar": False},
                            style={"height": "200px"},
                        ),
                    ],
                    className="sidebar-graph",
                ),
                html.Div(
                    [
                        html.Div(
                            "Taux d'incidence",
                            className="graph-title",
                            id=self.cid("hist-title"),
                        ),
                        dcc.Graph(
                            id=self.cid("histogram"),
                            config={"displayModeBar": False},
                            style={"height": "200px"},
                        ),
                    ],
                    className="sidebar-graph",
                ),
            ],
            className="sidebar",
        )

    def register_callbacks(self, app):
        """Enregistrer les callbacks pour la sidebar"""

        @app.callback(
            Output(self.cid("region"), "disabled"),
            Output(self.cid("dep"), "disabled"),
            Output(self.cid("region"), "value"),
            Output(self.cid("dep"), "value"),
            Input(self.cid("geo-level"), "value"),
        )
        def toggle_geo_dropdowns(level):
            if level == "region":
                return False, True, None, None
            elif level == "dep":
                return True, False, None, None
            else:
                return True, True, None, None

        @app.callback(
            Output(self.cid("time-graph"), "figure"),
            Output(self.cid("graph-title"), "children"),
            Input(self.cid("geo-level"), "value"),
            Input(self.cid("region"), "value"),
            Input(self.cid("dep"), "value"),
            Input(self.cid("stat-type"), "value"),
        )
        def update_time_graph(level, region, dep, stat_type):
            config = self.stat_types[stat_type]

            if level == "region" and region:
                df = config["graph_method"](region=region)
                title = f"{config['label']}"
            elif level == "dep" and dep:
                df = config["graph_method"](dep=dep)
                title = f"{config['label']}"
            else:
                df = config["graph_method"]()
                title = f"{config['label']}"

            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=df["date"],
                        y=df[config["graph_col"]],
                        mode="lines",
                        line=dict(color="#3b82f6", width=2),
                        fill="tozeroy",
                        fillcolor="rgba(59, 130, 246, 0.1)",
                    )
                ]
            )

            fig.update_layout(
                margin=dict(l=40, r=20, t=10, b=30),
                xaxis=dict(
                    showgrid=False,
                    showline=True,
                    linecolor="#e5e7eb",
                    tickfont=dict(size=10),
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#f3f4f6",
                    showline=False,
                    tickfont=dict(size=10),
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                hovermode="x unified",
            )

            return fig, title

        @app.callback(
            Output(self.cid("histogram"), "figure"),
            Output(self.cid("hist-title"), "children"),
            Input(self.cid("geo-level"), "value"),
            Input(self.cid("region"), "value"),
            Input(self.cid("dep"), "value"),
            Input(self.cid("stat-type"), "value"),
        )
        def update_histogram(level, region, dep, stat_type):
            config = self.stat_types[stat_type]

            if level == "region" and region:
                df = config["hist_method"](region=region)
                title = "Taux d'incidence"
            elif level == "dep" and dep:
                df = config["hist_method"](dep=dep)
                title = "Taux d'incidence"
            else:
                df = config["hist_method"]()
                title = "Taux d'incidence"

            fig = go.Figure(
                data=[
                    go.Bar(
                        x=df.get("mois", df.index),
                        y=df[config["hist_col"]],
                        marker_color="#ef4444",
                    )
                ]
            )

            fig.update_layout(
                margin=dict(l=40, r=20, t=10, b=30),
                xaxis=dict(
                    showgrid=False,
                    showline=True,
                    linecolor="#e5e7eb",
                    tickfont=dict(size=9),
                    tickangle=-45,
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#f3f4f6",
                    showline=False,
                    tickfont=dict(size=10),
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                bargap=0.2,
            )

            return fig, title
