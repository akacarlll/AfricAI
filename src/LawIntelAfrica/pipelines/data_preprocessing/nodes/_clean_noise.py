import re
import pandas as pd

def clean_noise(df: pd.DataFrame): 
    # Expression régulière pour capturer les motifs entre 'X.' et 'p.YY'
    pattern = r'''
    (?<!Art\.\s)       # Negative lookbehind pour exclure "Art. "
    \b\d+\.            # Chiffre suivi d'un point (ex: "2.")
    \s*                # Espaces optionnels
    (.*?)              # Contenu à supprimer (non gourmand)
    \s*p\.\s*\d+       # Référence de page (ex: "p.55" ou "p. 55")
    '''

    df['text'] = df['text'].str.replace(
        pattern,
        '', 
        flags=re.VERBOSE|re.IGNORECASE|re.DOTALL, 
        regex=True
    )

    return df