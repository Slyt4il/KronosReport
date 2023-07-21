import streamlit as st
import pandas as pd
import numpy as np
import pickle
import utils.helper as helper
import utils.studentinfo as studentinfo

st.set_page_config(
    page_title="Auto Draft - Kronos PVP Report",
    page_icon=helper.get_icon(),
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            button[title="View fullscreen"] {visibility: hidden;}
            .block-container {
                    padding-top: 2rem;
                    padding-bottom: 2rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                    overflow-x: clip;
                }
            .css-1oe5cao {
                    max-height: 66vh;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.sidebar.subheader("PVP Season: 4 🏙️ (Urban)")

st.write('🚧 Under Construction')
st.header("Team Auto Draft")
st.subheader("Input defenders to find the best team to attack with")
st.info('**This is a statistical prediction not a simulation.** There are many unpredictable factors that can affect the result of pvp matches.', icon="ℹ️")

def user_input_features():
    strikers_options = list(studentinfo.get_keys_strikers())
    specials_options = list(studentinfo.get_keys_specials())
    
    col1, col2 = st.columns(2)

    with col1:
        d1 = st.selectbox('Position D1', strikers_options, index = 33, format_func=helper.convert_readable)
        d2 = st.selectbox('Position D2', strikers_options, index = 29, format_func=helper.convert_readable)
        d3 = st.selectbox('Position D3', strikers_options, index = 21, format_func=helper.convert_readable)
        d4 = st.selectbox('Position D4', strikers_options, index = 28, format_func=helper.convert_readable)
        
    with col2:
        d5 = st.selectbox('Special D1', specials_options, index = 6, format_func=helper.convert_readable)
        d6 = st.selectbox('Special D2', specials_options, index = 13, format_func=helper.convert_readable)
        st.write('')
        st.write('')
        global exclude
        exclude = st.checkbox('Exclude teams with small sample size', help='Teams that appear less than 3 times in the dataset will be excluded.', value=True)
        
    data = {'d1': d1, 'd2': d2, 'd3': d3, 'd4': d4, 'd5': d5, 'd6': d6}

    features = pd.DataFrame(data, index=[0])

    has_duplicates = (features.loc[0, features.columns[0:6]].duplicated().sum() > 0) or (features.loc[0, features.columns[6:12]].duplicated().sum() > 0)
    if has_duplicates:
        st.error("Invalid team composition.", icon='⚠️')
        return None

    return features

input_df = user_input_features()

file_name = 'ss4_urban'
students_raw = pd.read_csv('datasets/' + file_name + '.csv')
students = students_raw.drop(columns=['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'attacker_won'])

invalid = False
if input_df is None:
    input_df = df = pd.DataFrame({'d1': 'shun', 'd2': 'tsubaki', 'd3': 'yuuka', 'd4': 'marina', 'd5': 'iroha', 'd6': 'utaha'}, index=[0])
    invalid = True
input_df = pd.concat([input_df] * len(students), ignore_index=True)
df = pd.concat([students, input_df], axis=1)

df['a5'] = np.where(df['a5'] < df['a6'], df['a5'] + '+' + df['a6'], df['a6'] + '+' + df['a5'])
df['d5'] = np.where(df['d5'] < df['d6'], df['d5'] + '+' + df['d6'], df['d6'] + '+' + df['d5'])

columns_to_drop = ['a6', 'd6']
df = df.drop(columns_to_drop, axis=1)

if exclude:
    freq = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0: 'count'})
    filter = freq[freq['count'] < 3].drop('count', axis=1)
    merged = df.merge(filter, how='left', indicator=True)
    df = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1).dropna()
    filtered_students = students.loc[students.index.intersection(df.index)].reset_index(drop=True)
else:
    filtered_students = students

model = pickle.load(open('datasets/' + file_name + '_clf.pkl', 'rb'))

pred = model.predict(df)
prob = pd.DataFrame(model.predict_proba(df))
prob.columns = prob.columns.astype(str)

st.subheader('Best teams to break the formation')

if not invalid:
    results = pd.concat([filtered_students.applymap(helper.convert_readable), prob.applymap(lambda num: "{:.2%}".format(num))], axis=1).drop('0', axis=1)
    sorted_df = results.sort_values(by='1', ascending=False).drop_duplicates()
    top = sorted_df.head(5)
    st.table(top)