from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo


class HistogramService(BaseService):
    """
    Servicé dédié à la gestions des Histogrammes.
    """

    def __init__(self):
        super().__init__()

    def nouvelles_hosp_par_mois(self, region=None, dep=None):
        """
        Hospitalisations moyennes par mois.

        :param region: string
        :param dep: string
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = df.copy()
        df["mois"] = df["date"].dt.to_period("M").astype(str)

        result = df.groupby("mois", as_index=False)[["incid_hosp"]].sum()

        result = result.rename(columns={"incid_hosp": "hosp"})
        return result

    def deces_par_mois(self, region=None, dep=None):
        """
        Décès hospitaliers par mois.

        :param region: string
        :param dep: string
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = df.copy()
        df["mois"] = df["date"].dt.to_period("M").astype(str)

        return df.groupby("mois", as_index=False)[["incid_dchosp"]].sum()
