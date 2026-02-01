from dash import html, Input, Output
from src.components.base.base_component import BaseComponent
from src.services.map_service import MapService


class DashboardMapComponent(BaseComponent):
    """
    Composant carte du dashboard avec :
    - Carte France métropolitaine (principale)
    - Cartes DROM-COM en bas (Guadeloupe, Martinique, Guyane, Réunion, Mayotte)
    """

    def __init__(self):
        super().__init__(service=MapService())

        self.drom_com = [
            {"name": "Guadeloupe", "id": "971"},
            {"name": "Martinique", "id": "972"},
            {"name": "Guyane", "id": "973"},
            {"name": "La Réunion", "id": "974"},
            {"name": "Mayotte", "id": "976"},
        ]

    def layout(self):
        """Layout de la zone carte"""
        return html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            id=self.cid("map-title"),
                            children="Taux d'occupation des lits en réanimation moyenne",
                            className="map-title",
                        ),
                        html.Div(
                            [
                                html.Iframe(
                                    id=self.cid("main-map"),
                                    srcDoc=self.service.hospitalisations_map_html(
                                        level="region"
                                    ),
                                    style={
                                        "width": "100%",
                                        "height": "100%",
                                        "border": "none",
                                    },
                                )
                            ],
                            className="main-map",
                        ),
                        html.Div(
                            [self._create_drom_card(drom) for drom in self.drom_com],
                            className="drom-com-container",
                        ),
                    ],
                    className="map-wrapper",
                )
            ],
            className="map-container",
        )

    def _create_drom_card(self, drom):
        """
        Créer une carte individuelle pour un DROM-COM

        Args:
            drom (dict): Dictionnaire avec 'name' et 'id' du DROM-COM

        Returns:
            html.Div: Carte du DROM-COM
        """
        return html.Div(
            [
                html.Iframe(
                    id=self.cid(f"drom-{drom['id']}"),
                    srcDoc=self.service.drom_map_html(drom["id"]),
                    style={
                        "width": "100%",
                        "height": "100%",
                        "border": "none",
                    },
                ),
                html.Div(drom["name"], className="drom-label"),
            ],
            className="drom-map",
        )

    def register_callbacks(self, app):
        """
        Enregistrer les callbacks pour mettre à jour les cartes
        en fonction des filtres de la sidebar
        """

        @app.callback(
            Output(self.cid("main-map"), "srcDoc"),
            Output(self.cid("map-title"), "children"),
            Input("SidebarComponent-geo-level", "value"),
            Input("SidebarComponent-region", "value"),
            Input("SidebarComponent-dep", "value"),
            Input("SidebarComponent-stat-type", "value"),
            Input("SidebarComponent-date-range", "start_date"),
            Input("SidebarComponent-date-range", "end_date"),
        )
        def update_main_map(level, region, dep, stat_type, start_date, end_date):
            map_level = "dep" if level == "dep" else "region"

            if stat_type == "deces":
                map_html = self.service.deces_map_html(
                    level=map_level,
                    region=region,
                    dep=dep,
                    start_date=start_date,
                    end_date=end_date,
                )
                title = "Décès hospitaliers totaux"
            elif stat_type == "rea":
                map_html = self.service.reanimations_map_html(
                    level=map_level,
                    region=region,
                    dep=dep,
                    start_date=start_date,
                    end_date=end_date,
                )
                title = "Nombre total de personnes admises en réanimation"
            else:
                map_html = self.service.hospitalisations_map_html(
                    level=map_level,
                    region=region,
                    dep=dep,
                    start_date=start_date,
                    end_date=end_date,
                )
                title = "Hospitalisations totales"

            return map_html, title

        for drom in self.drom_com:

            @app.callback(
                Output(self.cid(f"drom-{drom['id']}"), "srcDoc"),
                Input("SidebarComponent-stat-type", "value"),
            )
            def update_drom_map(stat_type, drom_id=drom["id"]):
                if stat_type == "deces":
                    return self.service.drom_map_html(drom_id, metric="deces")
                else:
                    return self.service.drom_map_html(drom_id, metric="hosp")
