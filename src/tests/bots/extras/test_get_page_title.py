import pytest
import pandas as pd
from scraping_bots.cmr_bots.extras.scraping_function import get_page_title


@pytest.fixture
def sample_dataframe():
    """Fixture to provide a sample DataFrame for testing law document titles."""
    data = {
        "title": [
            "Loi n° 2023-001 du 15 janvier 2023 portant réforme--du Code pénal au Cameroun.",
            "Décret présidentiel n°2023/045 du 10 mars 2023 fixant les modalités d'application de la loi foncière.",
            "Arrêté \ministériel du 5 avril 2023 : modification des taxes douanières.",
            "Ordonnance n°2023 en Août portant révision du régime fiscal des entreprises.",
        ],
        "expected_title": [
            "Loi_n_2023_001_du_15_janvier_2023_portant_reforme_du_Code_penal_au_Cameroun",
            "Decret_presidentiel_n_2023_045_du_10_mars_2023_fixant_les_modalites_d_application_de_la_loi_fonciere",
            "Arrete_ministeriel_du_5_avril_2023_modification_des_taxes_douanieres",
            "Ordonnance_n_2023_en_Aout_portant_revision_du_regime_fiscal_des_entreprises",
        ],
    }
    return pd.DataFrame(data)


class TestFileNameGeneration:
    def test_page_title(self, sample_dataframe):
        """Test applying generate_file_name to a DataFrame column."""
        df = sample_dataframe.copy()

        df["clean_title"] = df["title"].apply(get_page_title)
        assert df["clean_title"].tolist() == df["expected_title"].tolist()

        for val in df["clean_title"]:
            assert len(val) <= 150
