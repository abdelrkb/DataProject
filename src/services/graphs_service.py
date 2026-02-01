from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo, filter_by_date


class GraphService(BaseService):
    """
    Service dédié a la gestion des graphs
    """

    def __init__(self):
        super().__init__()

    def hospitalisations(
        self,
        region: str | None = None,
        dep: str | None = None,
        start_date=None,
        end_date=None,
    ):
        """
         Nouvelles hospitalisations par mois

        Args :
            region (str | None): region
            dep (str | None): departement
            start_date: date debut
            end_date: date fin
        Returns:
            pandas.DataFrame: DataFrame des hospitalisations
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        df = df.copy()
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

        grouped = df.groupby("month", as_index=False)[["incid_hosp"]].sum()
        grouped = grouped.rename(columns={"month": "date", "incid_hosp": "hosp"})

        return grouped[["date", "hosp"]].dropna()

    def deces_temporel(
        self,
        region: str | None = None,
        dep: str | None = None,
        start_date=None,
        end_date=None,
    ):
        """
        deces

        Args :
            region (str | None): region
            dep (str | None): departement
            start_date: date debut
            end_date: date fin
        Returns:
            pandas.DataFrame: DataFrame des deces
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        df = df.copy()
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

        grouped = df.groupby("month", as_index=False)[["incid_dchosp"]].sum()
        grouped = grouped.rename(columns={"month": "date", "incid_dchosp": "dchosp"})

        return grouped[["date", "dchosp"]].dropna()

    def reanimations_mensuelles(
        self,
        region: str | None = None,
        dep: str | None = None,
        start_date=None,
        end_date=None,
    ):
        """
        Nouvelles entrées en réanimation par mois

        Args :
            region (str | None): region
            dep (str | None): departement
            start_date: date debut
            end_date: date fin
        Returns:
            pandas.DataFrame: DataFrame des reanimations
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        df = df.copy()
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

        grouped = df.groupby("month", as_index=False)[["incid_rea"]].sum()
        grouped = grouped.rename(columns={"month": "date", "incid_rea": "rea"})

        return grouped[["date", "rea"]].dropna()

    def retours_domicile_mensuels(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Nouveaux retours a domicile par mois

        Args :
            region (str | None): region
            dep (str | None): departement
            start_date: date debut
            end_date: date fin
        Returns:
            pandas.DataFrame: DataFrame des retour a domicile
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        df = df.copy()
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

        grouped = df.groupby("month", as_index=False)[["incid_rad"]].sum()
        grouped = grouped.rename(columns={"month": "date", "incid_rad": "rad"})

        return grouped[["date", "rad"]].dropna()
