import streamlit as st
import pandas as pd
import numpy as np
import pickle
import studentinfo
import helper

st.set_page_config(
    page_title="Prediction - Kronos PVP Report",
    page_icon=helper.get_icon(),
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .block-container {
                    padding-top: 2rem;
                    padding-bottom: 2rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                    overflow-x: hidden;
                }
            .css-1oe5cao {
                    max-height: 66vh;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.sidebar.subheader("PVP Season: 4 🏙️ (Urban)")

st.header("PVP Result Prediction")
st.info('**This is a statistical prediction and not a simulation.** There are many factors that affect the result of pvp matches.', icon="ℹ️")

def user_input_features():
    strikers_options = list(studentinfo.get_keys_strikers())
    specials_options = list(studentinfo.get_keys_specials())
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        a1 = st.selectbox('Position A1', strikers_options, index = 22, format_func=helper.convert_readable)
        a2 = st.selectbox('Position A2', strikers_options, index = 23, format_func=helper.convert_readable)
        a3 = st.selectbox('Position A3', strikers_options, index = 8, format_func=helper.convert_readable)
        a4 = st.selectbox('Position A4', strikers_options, index = 27, format_func=helper.convert_readable)
    with col2:
        a5 = st.selectbox('Special A1', specials_options, index = 3, format_func=helper.convert_readable)
        a6 = st.selectbox('Special A2', specials_options, index = 9, format_func=helper.convert_readable)

    with col3:
        d1 = st.selectbox('Position D1', strikers_options, index = 27, format_func=helper.convert_readable)
        d2 = st.selectbox('Position D2', strikers_options, index = 23, format_func=helper.convert_readable)
        d3 = st.selectbox('Position D3', strikers_options, index = 17, format_func=helper.convert_readable)
        d4 = st.selectbox('Position D4', strikers_options, index = 22, format_func=helper.convert_readable)
        
    with col4:
        d5 = st.selectbox('Special D1', specials_options, index = 3, format_func=helper.convert_readable)
        d6 = st.selectbox('Special D2', specials_options, index = 9, format_func=helper.convert_readable)
        
    data = {'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'a6': a6,
            'd1': d1, 'd2': d2, 'd3': d3, 'd4': d4, 'd5': d5, 'd6': d6}

    features = pd.DataFrame(data, index=[0])

    has_duplicates = (features.loc[0, features.columns[0:6]].duplicated().sum() > 0) or (features.loc[0, features.columns[6:12]].duplicated().sum() > 0)
    if has_duplicates:
        st.error("Invalid team composition.", icon='⚠️')
        return None

    return features

input_df = user_input_features()

file_name = 'ss4_urban'
students_raw = pd.read_csv('datasets/' + file_name + '.csv')
students = students_raw.drop(columns=['attacker_won'])
df = pd.concat([input_df, students], axis = 0)
df = df[:1]

df['a5'] = np.where(df['a5'] < df['a6'], df['a5'] + '+' + df['a6'], df['a6'] + '+' + df['a5'])
df['d5'] = np.where(df['d5'] < df['d6'], df['d5'] + '+' + df['d6'], df['d6'] + '+' + df['d5'])

columns_to_drop = ['a6', 'd6']
df = df.drop(columns_to_drop, axis=1)

model = pickle.load(open('datasets/' + file_name + '_clf.pkl', 'rb'))

pred = model.predict(df)
prob = model.predict_proba(df)

st.subheader('Prediction result')
if input_df is not None:
    if pred == 1:
        st.write('⚔️ **Attackers** would win ', round(prob[0][1] * 100, 2), '% of the time!')
    else:
        st.write('🛡️ **Defenders** would win', round(prob[0][0] * 100, 2), '% of the time!')