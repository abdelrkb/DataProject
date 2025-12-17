from src.services.base.base_service import BaseService


class HospitalisationService(BaseService):
    def __init__(self):
        super().__init__()

    def available_regions(self):
        return sorted(self.df["lib_reg"].dropna().unique())

    def hospitalisations_by_region(self, region):
        filtered_df = self.df[self.df["lib_reg"] == region]

        return filtered_df.groupby("date", as_index=False)[["hosp"]].sum()
