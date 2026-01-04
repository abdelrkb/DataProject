from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo


class GraphService(BaseService):
    def __init__(self):
        super().__init__()

    def hospitalisations(self, region: str | None = None, dep: str | None = None):
        hosp_df = filter_by_geo(self.df, region=region, dep=dep)
        return hosp_df.groupby("date", as_index=False)[["hosp"]].sum()

    def taux_mortalite(self, region: str | None = None, dep: str | None = None):
        df = filter_by_geo(self.df, region, dep)
        return df[["date", "taux_mortalite"]].dropna()
