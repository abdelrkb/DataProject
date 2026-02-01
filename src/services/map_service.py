from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo, filter_by_date
from src.services.base.datastore import DataStore
import folium
import json
import os
from config import CONFIG


class MapService(BaseService):
    def __init__(self):
        super().__init__()
        self.geojson_dep, self.geojson_reg = DataStore.load_geojson()

        self.drom_coords = {
            "971": {
                "center": [16.25, -61.58],
                "zoom": 10,
                "name": "Guadeloupe",
                "bounds": [[15.8, -61.9], [16.6, -61.0]],
            },
            "972": {
                "center": [14.64, -61.02],
                "zoom": 10,
                "name": "Martinique",
                "bounds": [[14.3, -61.3], [14.9, -60.7]],
            },
            "973": {
                "center": [4.0, -53.0],
                "zoom": 7,
                "name": "Guyane",
                "bounds": [[2.0, -55.0], [6.0, -51.0]],
            },
            "974": {
                "center": [-21.13, 55.53],
                "zoom": 9,
                "name": "La Réunion",
                "bounds": [[-21.4, 55.2], [-20.8, 55.9]],
            },
            "976": {
                "center": [-12.83, 45.14],
                "zoom": 10,
                "name": "Mayotte",
                "bounds": [[-13.0, 45.0], [-12.6, 45.3]],
            },
        }

    def _load_drom_geojson(self, drom_id):
        """
        Charger le GeoJSON d'un DROM-COM spécifique

        Args:
            drom_id (str): Code département (971, 972, 973, 974, 976)
        Returns:
            dict | None: GeoJSON du DROM-COM ou None si non trouvé
        """
        geojson_paths = {
            "971": CONFIG["GEOJSON_PATH"].get("GUADELOUPE"),
            "972": CONFIG["GEOJSON_PATH"].get("MARTINIQUE"),
            "973": CONFIG["GEOJSON_PATH"].get("GUYANE"),
            "974": CONFIG["GEOJSON_PATH"].get("REUNION"),
            "976": CONFIG["GEOJSON_PATH"].get("MAYOTTE"),
        }

        path = geojson_paths.get(drom_id)
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        return None

    def _attach_properties(self, geojson, df, name_col, columns):
        """
        Attache les données aux features GeoJSON

        Args:
            geojson (dict): GeoJSON des zones géographiques
            df (pandas.DataFrame): DataFrame avec les données agrégées
            name_col (str): Nom de la colonne dans df correspondant au nom dans GeoJSON
            columns (list[str]): Liste des colonnes à attacher comme propriétés
        Returns:
            dict: GeoJSON avec les propriétés attachées
        """
        geojson_copy = json.loads(json.dumps(geojson))
        values = df.set_index(name_col)[columns].to_dict(orient="index")

        for feature in geojson_copy.get("features", []):
            name = feature.get("properties", {}).get("nom")
            props = values.get(name, {})
            for col in columns:
                feature.setdefault("properties", {})[col] = props.get(col, 0)

        return geojson_copy

    def _create_base_map(
        self, center, zoom, bounds=None, scroll_zoom=False, dragging=False
    ):
        """
        Créer une carte Folium de base avec des paramètres standards

        Args:
            center (list[float]): Coordonnées [lat, lon] du centre de la carte
            zoom (int): Niveau de zoom initial
            bounds (list[list[float]] | None): Limites de la carte [[lat_min
            , lon_min], [lat_max, lon_max]]
            scroll_zoom (bool): Activer/désactiver le zoom par défilement
            dragging (bool): Activer/désactiver le glissement de la carte
        Returns:
            folium.Map: Instance de la carte Folium
        """
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles="cartodbpositron",
            scrollWheelZoom=scroll_zoom,
            dragging=dragging,
            zoomControl=False,
            attributionControl=False,
        )

        if bounds:
            m.fit_bounds(bounds)

        return m

    def hospitalisations_map_html(
        self,
        level: str = "region",
        region: str | None = None,
        dep: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """
        Carte des hospitalisations pour France métropolitaine

        Args:
            level (str): "region" ou "dep" pour le niveau géographique
            region (str | None): Filtrer par région spécifique
            dep (str | None): Filtrer par département spécifique
            start_date (str | None): Date de début pour le filtrage
            end_date (str | None): Date de fin pour le filtrage
        Returns:
            str: HTML de la carte Folium
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        metrics_cols = ["incid_hosp", "incid_dchosp"]
        labels = {
            "incid_hosp": "Total hosp.",
            "incid_dchosp": "Total décès",
            "letalite": "Létalité (%)",
        }

        if level == "dep":
            geojson = self.geojson_dep
            name_col = "lib_dep"
            key_on = "feature.properties.nom"
        else:
            geojson = self.geojson_reg
            name_col = "lib_reg"
            key_on = "feature.properties.nom"

        agg_cols = [c for c in metrics_cols if c in df.columns]
        df = df.groupby(name_col, as_index=False)[agg_cols].sum()
        df["letalite"] = (df["incid_dchosp"] / (df["incid_hosp"] + 1) * 100).round(1)
        agg_cols.append("letalite")

        columns = [name_col, "incid_hosp"]

        geojson = self._attach_properties(geojson, df, name_col, agg_cols)
        tooltip_fields = ["nom"] + agg_cols
        tooltip_aliases = ["Zone"] + [labels.get(c, c) for c in agg_cols]

        FRANCE_BOUNDS = [[41.0, -5.5], [51.5, 9.5]]
        m = self._create_base_map(
            center=[46.6, 2.5], zoom=6, bounds=FRANCE_BOUNDS, scroll_zoom=False
        )

        choropleth = folium.Choropleth(
            geo_data=geojson,
            data=df,
            columns=columns,
            key_on=key_on,
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.3,
            legend_name="Hospitalisations",
        ).add_to(m)

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True,
                sticky=True,
            )
        )

        return m._repr_html_()

    def deces_map_html(
        self,
        level: str = "region",
        region: str | None = None,
        dep: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """
        Carte des décès pour France métropolitaine

        Args:
            level (str): "region" ou "dep" pour le niveau géographique
            region (str | None): Filtrer par région spécifique
            dep (str | None): Filtrer par département spécifique
            start_date (str | None): Date de début pour le filtrage
            end_date (str | None): Date de fin pour le filtrage
        Returns:
            str: HTML de la carte Folium
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        metrics_cols = ["incid_dchosp", "incid_hosp"]
        labels = {
            "incid_dchosp": "Total décès",
            "incid_hosp": "Total hosp.",
            "letalite": "Létalité (%)",
        }

        if level == "dep":
            geojson = self.geojson_dep
            name_col = "lib_dep"
            key_on = "feature.properties.nom"
        else:
            geojson = self.geojson_reg
            name_col = "lib_reg"
            key_on = "feature.properties.nom"

        agg_cols = [c for c in metrics_cols if c in df.columns]
        df = df.groupby(name_col, as_index=False)[agg_cols].sum()
        df["letalite"] = (df["incid_dchosp"] / (df["incid_hosp"] + 1) * 100).round(1)
        agg_cols.append("letalite")

        columns = [name_col, "incid_dchosp"]

        geojson = self._attach_properties(geojson, df, name_col, agg_cols)
        tooltip_fields = ["nom"] + agg_cols
        tooltip_aliases = ["Zone"] + [labels.get(c, c) for c in agg_cols]

        FRANCE_BOUNDS = [[41.0, -5.5], [51.5, 9.5]]
        m = self._create_base_map(
            center=[46.6, 2.5], zoom=6, bounds=FRANCE_BOUNDS, scroll_zoom=False
        )

        choropleth = folium.Choropleth(
            geo_data=geojson,
            data=df,
            columns=columns,
            key_on=key_on,
            fill_color="Reds",
            fill_opacity=0.7,
            line_opacity=0.3,
            legend_name="Décès",
        ).add_to(m)

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True,
                sticky=True,
            )
        )

        return m._repr_html_()

    def reanimations_map_html(
        self,
        level: str = "region",
        region: str | None = None,
        dep: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """
        Carte des réanimations pour France métropolitaine


        Args:
            level (str): "region" ou "dep" pour le niveau géographique
            region (str | None): Filtrer par région spécifique
            dep (str | None): Filtrer par département spécifique
            start_date (str | None): Date de début pour le filtrage
            end_date (str | None): Date de fin pour le filtrage
        Returns:
            str: HTML de la carte Folium
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        metrics_cols = ["incid_rea"] if "incid_rea" in df.columns else ["rea"]
        labels = {
            "rea": "Patients en réa",
            "incid_rea": "Total entrées en réa",
        }

        if level == "dep":
            geojson = self.geojson_dep
            name_col = "lib_dep"
            key_on = "feature.properties.nom"
        else:
            geojson = self.geojson_reg
            name_col = "lib_reg"
            key_on = "feature.properties.nom"

        agg_cols = [c for c in metrics_cols if c in df.columns]
        df = df.groupby(name_col, as_index=False)[agg_cols].sum()

        if "incid_rea" in df.columns:
            df = df.rename(columns={"incid_rea": "rea"})
            agg_cols = ["rea"]

        columns = [name_col, "rea"]

        geojson = self._attach_properties(geojson, df, name_col, agg_cols)
        tooltip_fields = ["nom"] + agg_cols
        tooltip_aliases = ["Zone"] + [labels.get(c, c) for c in agg_cols]

        FRANCE_BOUNDS = [[41.0, -5.5], [51.5, 9.5]]
        m = self._create_base_map(
            center=[46.6, 2.5], zoom=6, bounds=FRANCE_BOUNDS, scroll_zoom=False
        )

        choropleth = folium.Choropleth(
            geo_data=geojson,
            data=df,
            columns=columns,
            key_on=key_on,
            fill_color="Purples",
            fill_opacity=0.7,
            line_opacity=0.3,
            legend_name="Réanimations",
        ).add_to(m)

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True,
                sticky=True,
            )
        )

        return m._repr_html_()

    def retours_domicile_map_html(
        self,
        level: str = "region",
        region: str | None = None,
        dep: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """Carte des retours à domicile (sorties hospitalières)"""

        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        metrics_cols = ["incid_rad", "incid_hosp"]
        labels = {
            "incid_rad": "Total retours",
            "incid_hosp": "Total hosp.",
            "taux_retour": "Taux de retour (%)",
        }

        if level == "dep":
            geojson = self.geojson_dep
            name_col = "lib_dep"
            key_on = "feature.properties.nom"
        else:
            geojson = self.geojson_reg
            name_col = "lib_reg"
            key_on = "feature.properties.nom"

        agg_cols = [c for c in metrics_cols if c in df.columns]
        df = df.groupby(name_col, as_index=False)[agg_cols].sum()

        df["taux_retour"] = (df["incid_rad"] / (df["incid_hosp"] + 1) * 100).round(1)
        agg_cols.append("taux_retour")

        columns = [name_col, "incid_rad"]

        geojson = self._attach_properties(geojson, df, name_col, agg_cols)
        tooltip_fields = ["nom"] + agg_cols
        tooltip_aliases = ["Zone"] + [labels.get(c, c) for c in agg_cols]

        FRANCE_BOUNDS = [[41.0, -5.5], [51.5, 9.5]]
        m = self._create_base_map(
            center=[46.6, 2.5],
            zoom=6,
            bounds=FRANCE_BOUNDS,
            scroll_zoom=False,
        )

        choropleth = folium.Choropleth(
            geo_data=geojson,
            data=df,
            columns=columns,
            key_on=key_on,
            fill_color="Greens",
            fill_opacity=0.7,
            line_opacity=0.3,
            legend_name="Retours à domicile",
        ).add_to(m)

        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True,
                sticky=True,
            )
        )

        return m._repr_html_()

    def drom_map_html(
        self,
        drom_id: str,
        metric: str = "hosp",
        start_date: str | None = None,
        end_date: str | None = None,
        use_choropleth: bool = True,
    ) -> str:
        """
        Créer une carte pour un DROM-COM spécifique

        Args:
            drom_id (str): Code département (971, 972, 973, 974, 976)
            metric (str): 'hosp', 'rea', 'deces' ou 'rad'
            start_date (str | None): Date de début pour le filtrage
            end_date (str | None): Date de fin pour le filtrage
            use_choropleth (bool): Utiliser choropleth si GeoJSON disponible

        Returns:
            str: HTML de la carte Folium
        """
        drom_id = str(drom_id)
        if drom_id not in self.drom_coords:
            return "<p>Carte non disponible</p>"

        drom_info = self.drom_coords[drom_id]
        df_drom = self.df[self.df["dep"] == drom_id].copy()
        df_drom = filter_by_date(df_drom, start_date=start_date, end_date=end_date)

        m = self._create_base_map(
            center=drom_info["center"],
            zoom=drom_info["zoom"],
            bounds=drom_info.get("bounds"),
            scroll_zoom=False,
            dragging=False,
        )

        if df_drom.empty:
            return m._repr_html_()

        drom_geojson = self._load_drom_geojson(drom_id) if use_choropleth else None

        if drom_geojson and use_choropleth:
            if metric == "deces":
                cols = ["incid_dchosp", "incid_hosp"]
                color = "#fca5a5"
            elif metric == "rea":
                cols = ["incid_rea"] if "incid_rea" in df_drom.columns else ["rea"]
                color = "#c4b5fd"
            elif metric == "rad":
                cols = ["incid_rad", "incid_hosp"]
                color = "#86efac"
            else:
                cols = ["incid_hosp", "incid_dchosp"]
                color = "#fed7aa"

            df_map = df_drom.groupby("lib_dep", as_index=False)[cols].sum()
            df_map = df_map.reset_index(drop=True)

            if "incid_dchosp" in df_map.columns and "incid_hosp" in df_map.columns:
                df_map["letalite"] = (
                    (df_map["incid_dchosp"] / (df_map["incid_hosp"] + 1)) * 100
                ).round(1)

            if "incid_rad" in df_map.columns and "incid_hosp" in df_map.columns:
                df_map["taux_retour"] = (
                    (df_map["incid_rad"] / (df_map["incid_hosp"] + 1)) * 100
                ).round(1)

            values_to_inject = {}
            for col in df_map.columns:
                if col != "lib_dep":
                    values_to_inject[col] = float(df_map[col].iloc[0])

            geojson_copy = json.loads(json.dumps(drom_geojson))

            tooltip_lines = [f"<b>{drom_info['name']}</b>"]

            if "incid_hosp" in values_to_inject:
                tooltip_lines.append(
                    f"<b>Total hosp.:</b> {values_to_inject['incid_hosp']:,.0f}"
                )

            if "incid_dchosp" in values_to_inject:
                tooltip_lines.append(
                    f"<b>Total décès:</b> {values_to_inject['incid_dchosp']:,.0f}"
                )

            if "incid_rea" in values_to_inject:
                tooltip_lines.append(
                    f"<b>Total réa:</b> {values_to_inject['incid_rea']:,.0f}"
                )

            if "rea" in values_to_inject and "incid_rea" not in values_to_inject:
                tooltip_lines.append(
                    f"<b>Patients en réa:</b> {values_to_inject['rea']:,.0f}"
                )

            if "incid_rad" in values_to_inject:
                tooltip_lines.append(
                    f"<b>Total retours:</b> {values_to_inject['incid_rad']:,.0f}"
                )

            if "letalite" in values_to_inject:
                tooltip_lines.append(
                    f"<b>Létalité:</b> {values_to_inject['letalite']:.1f}%"
                )

            if "taux_retour" in values_to_inject:
                tooltip_lines.append(
                    f"<b>Taux retour:</b> {values_to_inject['taux_retour']:.1f}%"
                )

            tooltip_html = "<br>".join(tooltip_lines)

            geojson_layer = folium.GeoJson(
                geojson_copy,
                style_function=lambda x: {
                    "fillColor": color,
                    "color": "#999",
                    "weight": 1,
                    "fillOpacity": 0.6,
                },
                tooltip=folium.Tooltip(tooltip_html),
            )
            geojson_layer.add_to(m)

        else:
            if metric == "deces":
                total = df_drom["incid_dchosp"].sum()
                color = "red"
                label = "décès"
            elif metric == "rea":
                total = (
                    df_drom["incid_rea"].sum()
                    if "incid_rea" in df_drom.columns
                    else df_drom["rea"].sum()
                    if "rea" in df_drom.columns
                    else 0
                )
                color = "purple"
                label = "réa"
            elif metric == "rad":
                total = (
                    df_drom["incid_rad"].sum() if "incid_rad" in df_drom.columns else 0
                )
                color = "green"
                label = "retours"
            else:
                total = df_drom["incid_hosp"].sum()
                color = "orange"
                label = "hosp."

            folium.Marker(
                location=drom_info["center"],
                popup=f"<b>{drom_info['name']}</b><br>{total:,.0f} {label}",
                icon=folium.Icon(color=color, icon="info-sign"),
            ).add_to(m)

        return m._repr_html_()
