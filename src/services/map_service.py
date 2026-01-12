from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo, filter_by_date
from src.services.base.datastore import DataStore
import folium


class MapService(BaseService):
    def __init__(self):
        super().__init__()
        self.geojson_dep, self.geojson_reg = DataStore.load_geojson()

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

        if level == "dep":
            geojson = self.geojson_dep
            df = df.groupby("lib_dep", as_index=False)[["hosp"]].mean()
            key_on = "feature.properties.nom"
            columns = ["lib_dep", "hosp"]
        else:
            geojson = self.geojson_reg
            df = df.groupby("lib_reg", as_index=False)[["hosp"]].mean()
            key_on = "feature.properties.nom"
            columns = ["lib_reg", "hosp"]

        FRANCE_BOUNDS = [[41.0, -5.5], [51.5, 9.5]]
        # carte Folium
        m = folium.Map(
            location=[46.6, 2.5],
            zoom_start=7,
            tiles="cartodbpositron",
            crollWheelZoom=False,
        )
        m.fit_bounds(FRANCE_BOUNDS)
        folium.Choropleth(
            geo_data=geojson,
            data=df,
            columns=columns,
            key_on=key_on,
            fill_color="Reds",
            fill_opacity=0.8,
            line_opacity=0.2,
            legend_name="Hospitalisations",
        ).add_to(m)

        return m._repr_html_()

    def taux_mortalite_map_html(
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

        if level == "dep":
            geojson = self.geojson_dep
            df = df.groupby("lib_dep", as_index=False)[["taux_mortalite"]].mean()
            key_on = "feature.properties.nom"
            columns = ["lib_dep", "taux_mortalite"]
        else:
            geojson = self.geojson_reg
            df = df.groupby("lib_reg", as_index=False)[["taux_mortalite"]].mean()
            key_on = "feature.properties.nom"
            columns = ["lib_reg", "taux_mortalite"]

        FRANCE_BOUNDS = [[41.0, -5.5], [51.5, 9.5]]
        # carte Folium
        m = folium.Map(
            location=[46.6, 2.5],
            zoom_start=7,
            tiles="cartodbpositron",
            scrollWheelZoom=False,
        )
        m.fit_bounds(FRANCE_BOUNDS)
        folium.Choropleth(
            geo_data=geojson,
            data=df,
            columns=columns,
            key_on=key_on,
            fill_color="Blues",
            fill_opacity=0.8,
            line_opacity=0.2,
            legend_name="Taux de mortalité",
        ).add_to(m)

        return m._repr_html_()
