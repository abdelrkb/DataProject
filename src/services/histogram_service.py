from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo


class HistogramService(BaseService):
    """
    Servicé dédié à la gestions des Histogrammes.
    """

    def __init__(self):
        super().__init__()

    def hosp_distribution(self, region=None, dep=None):
        """
        Docstring pour hosp_distribution

        :param region: string
        :param dep: string
        """
        hosp_df = filter_by_geo(self.df, region=region, dep=dep)
        return hosp_df.groupby("date", as_index=False)[["hosp"]].sum()

    def taux_mortalite_distribution(self, region=None, dep=None):
        """
        Docstring pour taux_mortalite_distribution

        :param region: string
        :param dep: string
        """
        df = filter_by_geo(self.df, region, dep)
        return df[["taux_mortalite"]].dropna()
