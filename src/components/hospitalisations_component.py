from dash import html, dcc, Input, Output
import plotly.express as px
from src.components.base.base_component import BaseComponent
from src.services.hospitalisations_service import HospitalisationService


class HospitalisationsComponent(BaseComponent):
    def __init__(self):
        super().__init__(HospitalisationService())

    def layout(self):
        regions = self.service.available_regions()

        return html.Div(
            [
                html.H3(
                    "Évolution des hospitalisations COVID-19 par région",
                    style={"textAlign": "center"},
                ),
                dcc.Dropdown(
                    id="region-dropdown",
                    options=[{"label": r, "value": r} for r in regions],
                    value="Île-de-France",
                    clearable=False,
                    style={"width": "60%", "margin": "auto"},
                ),
                dcc.Graph(id="hospitalisation-graph"),
            ]
        )

    def register_callbacks(self, app):
        @app.callback(
            Output("hospitalisation-graph", "figure"),
            Input("region-dropdown", "value"),
        )
        def update_hospitalisation_graph(selected_region):
            df = self.service.hospitalisations_by_region(selected_region)

            fig = px.line(
                df,
                x="date",
                y="hosp",
                title=f"Hospitalisations COVID-19 — {selected_region}",
                labels={
                    "hosp": "Patients hospitalisés",
                    "date": "Date",
                },
                template="plotly",
            )
            fig.update_layout(title_x=0.5)

            return fig
