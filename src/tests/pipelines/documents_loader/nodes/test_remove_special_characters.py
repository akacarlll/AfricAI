import pytest
from src.LawIntelAfrica.pipelines.documents_loader.nodes import remove_characters
import pandas as pd

class Test_remove_characters:
    def test_remove_special_characters(self):
        
        # Arrange
        text = ["Ils dansèrent sous la lune brillante, accompagnés par le doux chant des grillons. 🌳🌕"]
        df = pd.DataFrame(text, columns=["text"])
        
        expected_text = ["Ils danserent sous la lune brillante, accompagnes par le doux chant des grillons. "]
        df_expected = pd.DataFrame(expected_text, columns=["text"])
        
        #Act
        df_cleaned = remove_characters(df)
        print(list(df_cleaned))
        #Assert
        assert df_expected.equals(df_cleaned)
        