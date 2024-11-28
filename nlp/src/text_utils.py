import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)

from german_nouns.lookup import Nouns # https://github.com/gambolputty/german-nouns 

from googletrans import Translator
from tqdm import tqdm

import spacy


def trennbare_workaround(df, verbose=False):
    """Combines separable verbs in a dataframe.

    This function identifies separable verbs in a dataframe and combines them into a single token.
    It assumes the dataframe has columns named 'tag', 'position', 'pos', 'norm_token', and 'token'.

    Args:
        df (pandas.DataFrame): A dataframe containing tokenized text data.

    Returns:
        pandas.DataFrame: A copy of the input dataframe with separable verbs combined.

    Example:
        >>> df = pd.DataFrame({'tag': ['PTKVZ', 'VVFIN'], 'position': [1, 2], 'pos': ['VERB', 'VERB'], 'norm_token': ['ab', 'gehen'], 'token': ['ab', 'gehen']})
        >>> trennbare_workaround(df)
           tag  position   pos norm_token token
        0  PTKVZ         1  VERB   abgehen    ab
        1  VVFIN         2  VERB     gehen  gehen
    """
        
    new_df = df.copy()
    tb_pos1 = new_df[new_df['tag'] ==  'PTKVZ']['position'].astype(int).to_numpy()
    tb_pos2 = new_df[(df['pos'] ==  'VERB') & (new_df['tag'] ==  'VVFIN')]['position'].astype(int).to_numpy()

    cross_join = {x: y for x in tb_pos1 for y in tb_pos2 if x > y}

    for preffix, verb in cross_join.items():
        
        if verbose:
            print(verb, preffix)
            print(new_df.loc[verb,'norm_token'])
            print(new_df.loc[preffix,'token'] + new_df.loc[verb,'norm_token'])
            print()
        
        new_df.loc[verb,'norm_token'] = new_df.loc[preffix,'token'] + new_df.loc[verb,'norm_token']
    
    return new_df

def google_translate(texts, dest_language='en', src_language='de'):
    """Translates a list of text strings using Google Translate.

    Args:
        texts (list): A list of text strings to translate.
        dest_language (str, optional): The destination language code (e.g., 'en' for English). 
                                        Defaults to 'en'.
        src_language (str, optional): The source language code (e.g., 'es' for Spanish). 
                                        Defaults to 'auto', which attempts to auto-detect the source language.

    Returns:
        list: A list of translated text strings.

    Raises:
        ValueError: If the input is not a list or if the list is empty.

    Example:
        >>> google_translate(['Hola', 'mundo'], dest_language='en')
        ['Hello', 'world']
    """

    if not isinstance(texts, list) or not texts:
        raise ValueError("Input must be a non-empty list of strings.")

    translator = Translator()
    output = []
    for text in tqdm(texts, desc=f"Translating to {dest_language}"):
        translation = translator.translate(text, dest=dest_language, src=src_language)
        output.append(translation.text)

    return output

def custom_pos(text):
    """Performs POS tagging and normalization on German text using spaCy.

    This function processes a given German text string, performs Part-of-Speech (POS) tagging
    using the `de_core_news_md` spaCy model, and applies custom normalization rules to nouns,
    adjectives, verbs, and adverbs.

    Args:
        text (str): The German text string to process.

    Returns:
        pandas.DataFrame: A DataFrame containing the tokenized text and linguistic information,
                           including normalized forms for nouns, adjectives, verbs, and adverbs.

    Example:
        >>> text = "Die grüne Wiese ist schön."
        >>> custom_pos(text)
           position    token sentence    lemma   pos   tag   ...  degree  mood  number  person  tense verbform  norm_token
        0         0      Die  Die grüne...     die   DET   ART  ...     NaN   NaN     NaN     NaN    NaN      NaN        die 
        1         1   grüne  Die grüne...   grün   ADJ   ADJA  ...     NaN   NaN     NaN     NaN    NaN      NaN      grüne
        2         2    Wiese  Die grüne...   Wiese  NOUN   NN  ...     NaN   NaN     Sg      NaN    NaN      NaN   die Wiese
        3         3      ist  Die grüne...    sein  AUX   VBZ  ...     NaN   Ind     Sg      3     Pres      Fin        sein
        4         4   schön  Die grüne...   schön   ADJ   ADJD  ...     NaN   NaN     NaN     NaN    NaN      NaN      schön
        5         5       .  Die grüne...       .  PUNCT  $.  ...     NaN   NaN     NaN     NaN    NaN      NaN           .

    """

    # Load the German spaCy model
    nlp = spacy.load('de_core_news_md')

    # Clean the text by removing newline characters
    clean_text = text.replace('\n', '')

    # Process the text with spaCy
    doc = nlp(clean_text)

    # Create a DataFrame from the spaCy Doc object
    df_doc = pd.DataFrame(
        [(_, token.text, token.sent, token.lemma_, token.pos_, token.tag_, token.morph) for _, token in enumerate(doc)],
        columns=['position', 'token', 'sentence', 'lemma', 'pos', 'tag', 'morph']
    )

    # Extract morphological features into a separate DataFrame
    morph_df = pd.DataFrame([m.to_dict() for m in df_doc['morph']])
    morph_df = morph_df[np.sort(morph_df.columns)]

    # Combine the main DataFrame with the morphological features
    df_doc.drop(columns=['morph'], inplace=True)
    out_df = pd.concat([df_doc, morph_df], axis=1)

    # Define a dictionary for gender-specific articles
    gender_article = {
        'Fem': 'die ', 'Neut': 'das ', 'Masc': 'der ',
    }

    # Normalize nouns by adding the appropriate article based on gender
    out_df['norm_noun'] = np.where(
        out_df['pos'] == 'NOUN',
        out_df['Gender'].replace(gender_article) + out_df['lemma'].astype(str),
        np.nan
    )

    # Normalize adjectives, verbs, and adverbs by using their lemmas
    informative_pos = ["ADJ", "VERB", "ADV"]
    for pos in informative_pos:
        out_df[f'norm_{pos.lower()}'] = np.where(
            out_df['pos'] == pos,
            out_df['lemma'],
            np.nan
        )

    # Clean up the DataFrame
    out_df.columns = [col.lower() for col in out_df.columns]
    norm_cols = [col for col in out_df.columns if col[:5] == 'norm_']
    out_df = out_df.fillna('').astype(str)

    # Combine normalized forms into a single 'norm_token' column
    out_df['norm_token'] = out_df[norm_cols].sum(axis=1)

    return out_df

def singular(noun : str):
    """A function that outputs the singular of a noun

    Args:
        noun (_type_): _description_

    Returns:
        _type_: _description_
    """

    Worterbuch = Nouns()
    out = Worterbuch[noun]

    article = {
        'm': 'der',
        'f': 'die',
        'n': 'das'
    }

    try:
        out = out[0]
        out = article.get(out.get('genus')) + ' ' + out.get('flexion').get('nominativ singular')
    except:
        out = 'none'

    return out
