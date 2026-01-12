from src.services.base.base_service import BaseService


class ReferenceService(BaseService):
    """
    Service fournissant des références de données (régions, départements...)
    """

    def __init__(self):
        super().__init__()

    def available_regions(self):
        return sorted(self.df["lib_reg"].dropna().unique())

    def available_dep(self):
        return sorted(self.df["lib_dep"].dropna().unique())

    def departements_by_region(self, region):
        return sorted(
            self.df[self.df["lib_reg"] == region]["lib_dep"].dropna().unique()
        )
