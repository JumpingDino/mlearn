import sys
sys.path.append('../')

from artifacts.google_langs import LANG_DICT, LANG_LIST

import streamlit as st
st.set_page_config(
    page_title="Text-To-Vocab",
    page_icon="📓",
)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

@st.cache_data(ttl=600, show_spinner="Processing the Text", max_entries=100)
def feat_text_to_vocab(text, dest_language='en'):
    st.write(f"You wrote {len(text)} characters.")

    from src.text_utils import custom_pos, trennbare_workaround, google_translate

    dest_language=dest_language
    out_df = custom_pos(text)
    out_df = trennbare_workaround(out_df, verbose=False)

    only_important = out_df['norm_token'] != ""

    filt_df = out_df[only_important]

    #group by token and normalized token and bring all sentences
    de_df = filt_df.groupby(['token', 'norm_token'], as_index=False)['sentence'].apply(list)
    #Minimum position of the normalized token
    tok_pos_df = filt_df.groupby('norm_token').min()['position']
    grouped = filt_df.groupby('norm_token')['token'].apply(list).rename('tokens')
    #create dataset in german
    
    de_df = de_df.merge(tok_pos_df, on='norm_token').sort_values(by='position').drop(columns='position')
    de_df = de_df.merge(grouped, on='norm_token')
    de_df.drop_duplicates(subset = ['norm_token'], inplace=True)

    de_df['token_target'] = google_translate(de_df['norm_token'].to_list(), dest_language=dest_language)
    de_df['sentence_target'] = [google_translate(sents, dest_language=dest_language) for sents in de_df['sentence']]

    #just fixing the final dataset
    renaming = {
        'tokens': 'tokens_raw', 
        'norm_token': 'token_de', 
        'sentence': 'sentences_de', 
        'token_target': f'token_{dest_language}',
        'sentence_target': f'sentences_{dest_language}'
    }

    col_order = [
        'token_de', 'sentences_de',
        f'token_{dest_language}', f'sentences_{dest_language}',
        'tokens_raw']
    
    output = de_df.rename(columns=renaming)
    output = output[col_order]
    return output

def save_data():
    pass

st.write("# Welcome to Text To Vocab 📓")

st.markdown(
    """
    This feature is responsible to generate well data :sparkles: for your future german studies.
    """)

lang_code = st.selectbox(
    label="What is the target Language?",
    options=LANG_LIST,
    index=21
)
dest_language=LANG_DICT[lang_code]

text = st.text_area(
        "Enter some text 👇",
        value="""Es war einmal ein kleiner Hund namens Max. Max lebte in einer kleinen Stadt und liebte es, durch den Park zu laufen. Jeden Tag spielte er mit seinen Freunden, den anderen Hunden. Eines Tages fand Max einen verlorenen Ball im Gras. Er nahm den Ball und suchte nach dem Besitzer. Nach einer Weile traf er ein kleines Mädchen, das weinte. Der Ball gehörte ihr! Max gab ihr den Ball zurück, und das Mädchen war sehr glücklich. Sie spielte den ganzen Nachmittag mit Max. Am Ende des Tages wurden sie beste Freunde. Max war stolz und glücklich.""",
        height=400
    )

# https://docs.streamlit.io/develop/concepts/design/buttons

st.button("Detect Words!", type='primary', on_click=click_button)

if st.session_state.clicked:
    output = feat_text_to_vocab(text, dest_language=dest_language)
    
    edited_df = st.data_editor(
        output,
        num_rows="dynamic",
        # column_config={
        #     "is_right": st.column_config.CheckboxColumn(
        #     "is_right?",
        #     help="Select the right Tokens",
        #     default=True,
        # )
        #},
        disabled=['token'],
        hide_index=True)

    if st.button("Save Cards", type='primary', on_click=save_data):
        edited_df.to_csv('data/cards.csv', mode='a', index=False)