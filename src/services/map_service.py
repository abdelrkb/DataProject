from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo, filter_by_date
from src.services.base.datastore import DataStore
import folium
import json


class MapService(BaseService):
    def __init__(self):
        super().__init__()
        self.geojson_dep, self.geojson_reg = DataStore.load_geojson()

    def _attach_properties(self, geojson, df, name_col, columns):
        # Deep copy to avoid mutating shared geojson across calls
        geojson_copy = json.loads(json.dumps(geojson))
        values = df.set_index(name_col)[columns].to_dict(orient="index")

        for feature in geojson_copy.get("features", []):
            name = feature.get("properties", {}).get("nom")
            props = values.get(name, {})
            for col in columns:
                feature.setdefault("properties", {})[col] = props.get(col)

        return geojson_copy

    def deces_map_html(
        self,
        level: str = "region",
        region: str | None = None,
        dep: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        # filtrage
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        metrics_cols = ["incid_dchosp", "incid_hosp"]


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
        labels = {
            "incid_dchosp": "Total décès",
            "incid_hosp": "Total hosp.",
            "letalite": "Létalité (%)",
        }

        geojson = self._attach_properties(geojson, df, name_col, agg_cols)
        tooltip_fields = ["nom"] + agg_cols
        tooltip_aliases = ["Zone"] + [labels.get(c, c) for c in agg_cols]

        FRANCE_BOUNDS = [[41.0, -5.5], [51.5, 9.5]]
        # carte Folium
        m = folium.Map(
            location=[46.6, 2.5],
            zoom_start=7,
            tiles="cartodbpositron",
            scrollWheelZoom=False,
        )
        m.fit_bounds(FRANCE_BOUNDS)
        choropleth = folium.Choropleth(
            geo_data=geojson,
            data=df,
            columns=columns,
            key_on=key_on,
            fill_color="Reds",
            fill_opacity=0.8,
            line_opacity=0.2,
            legend_name="Total décès",
        ).add_to(m)
        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True,
                sticky=True,
            )
        )
        choropleth.geojson.add_child(
            folium.features.GeoJsonPopup(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True,
            )
        )

        return m._repr_html_()

    def hospitalisations_map_html(
        self,
        level: str = "region",
        region: str | None = None,
        dep: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        # filtrage
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        labels = {
            "incid_hosp": "Total hosp.",
            "incid_dchosp": "Total décès",
            "letalite": "Létalité (%)",
        }
        metrics_cols = [
            "incid_hosp",
            "incid_dchosp",
        ]

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
        df[agg_cols] = df[agg_cols].round(2)
        columns = [name_col, "incid_hosp"]
        df["letalite"] = (df["incid_dchosp"] / (df["incid_hosp"] + 1) * 100).round(1)
        agg_cols.append("letalite")

        geojson = self._attach_properties(geojson, df, name_col, agg_cols)
        tooltip_fields = ["nom"] + agg_cols
        tooltip_aliases = ["Zone"] + [labels.get(c, c) for c in agg_cols]

        FRANCE_BOUNDS = [[41.0, -5.5], [51.5, 9.5]]
        # carte Folium
        m = folium.Map(
            location=[46.6, 2.5],
            zoom_start=7,
            tiles="cartodbpositron",
            scrollWheelZoom=False,
        )
        m.fit_bounds(FRANCE_BOUNDS)
        choropleth = folium.Choropleth(
            geo_data=geojson,
            data=df,
            columns=columns,
            key_on=key_on,
            fill_color="Blues",
            fill_opacity=0.8,
            line_opacity=0.2,
            legend_name="Total hospitalisations",
        ).add_to(m)
        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True,
                sticky=True,
            )
        )
        choropleth.geojson.add_child(
            folium.features.GeoJsonPopup(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                localize=True,
            )
        )

        return m._repr_html_()
