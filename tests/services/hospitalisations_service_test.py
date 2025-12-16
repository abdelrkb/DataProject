import pandas as pd
import pytest

from src.services.hospitalisations_service import HospitalisationService


@pytest.fixture
def sample_dataframe():
    """DataFrame de test simulant les données hospitalières."""
    return pd.DataFrame(
        {
            "lib_reg": [
                "Île-de-France",
                "Île-de-France",
                "Occitanie",
                None,
            ],
            "date": [
                "2024-01-01",
                "2024-01-01",
                "2024-01-01",
                "2024-01-01",
            ],
            "hosp": [10, 5, 7, 3],
        }
    )


@pytest.fixture
def service(sample_dataframe):
    """Service avec un DataFrame injecté."""
    service = HospitalisationService()
    service.df = sample_dataframe
    return service


def test_available_regions_returns_sorted_unique_regions(service):
    regions = service.available_regions()

    assert regions == ["Occitanie", "Île-de-France"]
