from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo, filter_by_date


class HistogramService(BaseService):
    """
    Servicé dédié à la gestions des Histogrammes.
    """

    def __init__(self):
        super().__init__()

    def nouvelles_hosp_par_mois(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Hospitalisations moyennes par mois.

        :param region: string
        :param dep: string
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)
        df = df.copy()
        df["mois"] = df["date"].dt.to_period("M").astype(str)

        result = df.groupby("mois", as_index=False)[["incid_hosp"]].sum()

        result = result.rename(columns={"incid_hosp": "hosp"})
        return result

    def deces_par_mois(self, region=None, dep=None, start_date=None, end_date=None):
        """
        Décès hospitaliers par mois.

        :param region: string
        :param dep: string
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)
        df = df.copy()
        df["mois"] = df["date"].dt.to_period("M").astype(str)

        return df.groupby("mois", as_index=False)[["incid_dchosp"]].sum()

    def reanimations_par_mois(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Entrées en réanimation par mois.

        :param region: string
        :param dep: string
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)
        df = df.copy()

        df["mois"] = df["date"].dt.to_period("M").astype(str)

        return (
            df.groupby("mois", as_index=False)[["incid_rea"]]
            .sum()
            .rename(columns={"incid_rea": "rea"})
        )

    def retours_domicile_par_mois(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Retours à domicile par mois.

        Args :
            region (str | None): region
            dep (str | None): departement
            start_date: date debut
            end_date: date fin
        Returns:
            pandas.DataFrame: DataFrame des retours a domicile
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        df = df.copy()
        df["mois"] = df["date"].dt.to_period("M").astype(str)

        return (
            df.groupby("mois", as_index=False)[["incid_rad"]]
            .sum()
            .rename(columns={"incid_rad": "retours"})
        )
