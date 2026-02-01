from src.services.base.base_service import BaseService
from src.utils.data_filter import filter_by_geo, filter_by_date
import pandas as pd
import numpy as np


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
        Histogramme : distribution des nouvelles hospitalisations avec bins.
        Axe X : intervalles de nouvelles hospitalisations
        Axe Y : nombre de jours dans chaque intervalle

        :param region: string
        :param dep: string
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)
        df = df.copy()
        
        df = df.dropna(subset=['incid_hosp'])
        
        if dep is None:
            df = df.groupby('date', as_index=False)['incid_hosp'].sum()
        
        if region is None and dep is None:
            bins = [0, 100, 500, 1000, 2000, 5000, 10000, np.inf]
            labels = ['0-100', '100-500', '500-1000', '1000-2000', '2000-5000', '5000-10000', '10000+']
        elif region is not None and dep is None:
            bins = [0, 20, 50, 100, 200, 500, 1000, np.inf]
            labels = ['0-20', '20-50', '50-100', '100-200', '200-500', '500-1000', '1000+']
        else:
            bins = [0, 5, 10, 20, 50, 100, 200, np.inf]
            labels = ['0-5', '5-10', '10-20', '20-50', '50-100', '100-200', '200+']
        
        df['hosp_bin'] = pd.cut(df['incid_hosp'], bins=bins, labels=labels, include_lowest=True)
        
        result = df['hosp_bin'].value_counts().reset_index()
        result.columns = ['hosp', 'count']
        result = result.sort_values('hosp')
        
        return result

    def deces_par_mois(self, region=None, dep=None, start_date=None, end_date=None):
        """
        Histogramme : distribution des nouveaux décès avec bins.
        Axe X : intervalles de nouveaux décès
        Axe Y : nombre de jours dans chaque intervalle

        :param region: string
        :param dep: string
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)
        df = df.copy()
        
        df = df.dropna(subset=['incid_dchosp'])
        
        if dep is None:
            df = df.groupby('date', as_index=False)['incid_dchosp'].sum()
        
        if region is None and dep is None:
            bins = [0, 10, 50, 100, 200, 500, 1000, np.inf]
            labels = ['0-10', '10-50', '50-100', '100-200', '200-500', '500-1000', '1000+']
        elif region is not None and dep is None:
            bins = [0, 2, 5, 10, 20, 50, 100, np.inf]
            labels = ['0-2', '2-5', '5-10', '10-20', '20-50', '50-100', '100+']
        else:
            bins = [0, 1, 2, 5, 10, 20, 50, np.inf]
            labels = ['0-1', '1-2', '2-5', '5-10', '10-20', '20-50', '50+']
        
        df['dchosp_bin'] = pd.cut(df['incid_dchosp'], bins=bins, labels=labels, include_lowest=True)
        
        result = df['dchosp_bin'].value_counts().reset_index()
        result.columns = ['incid_dchosp', 'count']
        result = result.sort_values('incid_dchosp')
        
        return result

    def reanimations_par_mois(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Histogramme : distribution des nouvelles entrées en réanimation avec bins.
        Axe X : intervalles de nouvelles entrées en réa
        Axe Y : nombre de jours dans chaque intervalle

        :param region: string
        :param dep: string
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)
        df = df.copy()

        df = df.dropna(subset=['incid_rea'])
        
        if dep is None:
            df = df.groupby('date', as_index=False)['incid_rea'].sum()
        
        if region is None and dep is None:
            bins = [0, 50, 100, 200, 500, 1000, 2000, np.inf]
            labels = ['0-50', '50-100', '100-200', '200-500', '500-1000', '1000-2000', '2000+']
        elif region is not None and dep is None:
            bins = [0, 10, 20, 50, 100, 200, 500, np.inf]
            labels = ['0-10', '10-20', '20-50', '50-100', '100-200', '200-500', '500+']
        else:
            bins = [0, 2, 5, 10, 20, 50, np.inf]
            labels = ['0-2', '2-5', '5-10', '10-20', '20-50', '50+']
        
        df['rea_bin'] = pd.cut(df['incid_rea'], bins=bins, labels=labels, include_lowest=True)
        
        result = df['rea_bin'].value_counts().reset_index()
        result.columns = ['rea', 'count']
        result = result.sort_values('rea')
        
        return result

    def retours_domicile_par_mois(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Histogramme : distribution des nouveaux retours à domicile avec bins.
        Axe X : intervalles de nouveaux retours
        Axe Y : nombre de jours dans chaque intervalle

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

        df = df.dropna(subset=['incid_rad'])
        
        if dep is None:
            df = df.groupby('date', as_index=False)['incid_rad'].sum()
        
        if region is None and dep is None:
            bins = [0, 100, 500, 1000, 2000, 5000, 10000, np.inf]
            labels = ['0-100', '100-500', '500-1000', '1000-2000', '2000-5000', '5000-10000', '10000+']
        elif region is not None and dep is None:
            bins = [0, 20, 50, 100, 200, 500, 1000, np.inf]
            labels = ['0-20', '20-50', '50-100', '100-200', '200-500', '500-1000', '1000+']
        else:
            bins = [0, 5, 10, 20, 50, 100, 200, np.inf]
            labels = ['0-5', '5-10', '10-20', '20-50', '50-100', '100-200', '200+']
        
        df['rad_bin'] = pd.cut(df['incid_rad'], bins=bins, labels=labels, include_lowest=True)
        
        result = df['rad_bin'].value_counts().reset_index()
        result.columns = ['retours', 'count']
        result = result.sort_values('retours')
        
        return result

    def hosp_actuelles_par_mois(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Nombre moyen de patients hospitalisés par mois (stock).

        Args :
            region (str | None): region
            dep (str | None): departement
            start_date: date debut
            end_date: date fin
        Returns:
            pandas.DataFrame: DataFrame des hospitalisations actuelles
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        df = df.copy()
        df["mois"] = df["date"].dt.to_period("M").astype(str)

        return df.groupby("mois", as_index=False)[["hosp"]].mean()

    def rea_actuelles_par_mois(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Nombre moyen de patients en réanimation par mois (stock).

        Args :
            region (str | None): region
            dep (str | None): departement
            start_date: date debut
            end_date: date fin
        Returns:
            pandas.DataFrame: DataFrame des réanimations actuelles
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        df = df.copy()
        df["mois"] = df["date"].dt.to_period("M").astype(str)

        return df.groupby("mois", as_index=False)[["rea"]].mean()

    def deces_cumules_par_mois(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Décès cumulés par mois (dernière valeur du mois).

        Args :
            region (str | None): region
            dep (str | None): departement
            start_date: date debut
            end_date: date fin
        Returns:
            pandas.DataFrame: DataFrame des décès cumulés
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        df = df.copy()
        df["mois"] = df["date"].dt.to_period("M").astype(str)

        result = df.sort_values("date").groupby("mois", as_index=False).last()[["mois", "dchosp"]]
        
        return result

    def retours_cumules_par_mois(
        self, region=None, dep=None, start_date=None, end_date=None
    ):
        """
        Retours à domicile cumulés par mois (dernière valeur du mois).

        Args :
            region (str | None): region
            dep (str | None): departement
            start_date: date debut
            end_date: date fin
        Returns:
            pandas.DataFrame: DataFrame des retours cumulés
        """
        df = filter_by_geo(self.df, region=region, dep=dep)
        df = filter_by_date(df, start_date=start_date, end_date=end_date)

        df = df.copy()
        df["mois"] = df["date"].dt.to_period("M").astype(str)

        result = df.sort_values("date").groupby("mois", as_index=False).last()[["mois", "rad"]]
        result = result.rename(columns={"rad": "retours"})
        
        return result
