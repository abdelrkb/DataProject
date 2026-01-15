from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo


class GraphService(BaseService):
    def __init__(self):
        super().__init__()

    def hospitalisations(self, region: str | None = None, dep: str | None = None):
        hosp_df = filter_by_geo(self.df, region=region, dep=dep)
        return hosp_df.groupby("date", as_index=False)[["hosp"]].sum()

    def reanimations_mensuelles(self, region: str | None = None, dep: str | None = None):
        df = filter_by_geo(self.df, region, dep)
        df = df.copy()
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
        if "incid_rea" in df.columns:
            grouped = df.groupby("month", as_index=False)[["incid_rea"]].sum()
            grouped = grouped.rename(columns={"month": "date", "incid_rea": "rea"})
            return grouped[["date", "rea"]].dropna()

        # Fallback: rea est un stock -> approx mensuelle via moyenne journalière
        grouped = df.groupby("month", as_index=False)[["rea"]].mean()
        grouped = grouped.rename(columns={"month": "date"})
        return grouped[["date", "rea"]].dropna()
