import pytest
import pandas as pd
from src.LawIntelAfrica.pipelines.documents_loader.nodes import extract_metadata


class Test_metadata_extraction :
    def test_extract_metadata(self):
        #Arrange
        data = pd.DataFrame({
            "source": [
                r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\cmr\pdfs\code\ACTE_OHADA.pdf",
                r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\cmr\pdfs\decret\LOI_FINANCES.pdf",
                r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\cmr\pdfs\autres\Cameroun-Loi-2002-04-charte-des-investissements.pdf",
                r"C:\Users\carlf\Documents\GitHub\LawIntelAfrica\data\01_raw\cmr\pdfs\loi\LOI_N°_2017_009_DU_12_JUILLET_2017.pdf",
            ],
            "page": [92, 5, 0, 67,],
        })
        data_expected = pd.DataFrame({
            "page_title": [
                "ACTE_OHADA", 
                "LOI_FINANCES",
                "Cameroun-Loi-2002-04-charte-des-investissements",
                "LOI_N°_2017_009_DU_12_JUILLET_2017"
                
            ]
        }
        )
        #Act
        df = extract_metadata(data)
        #Assert
        
        pd.testing.assert_frame_equal(df, data_expected, check_dtype=False)
            