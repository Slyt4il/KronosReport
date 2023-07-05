import streamlit as st
import pandas as pd
import datasets.model_builder as model_builder
import helper

st.set_page_config(
    page_title="Dataset - Kronos PVP Report",
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
                }
            .css-1oe5cao {
                    max-height: 66vh;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.sidebar.subheader("PVP Season: 4 🏙️ (Urban)")


st.header("Dataset")

file_name = 'ss4_urban'
data = pd.read_csv('datasets/' + file_name + '.csv')
size = st.info('Sample size: ' + str(len(data)), icon='📊')
dataframe = st.dataframe(data, height=410)

@st.cache_data(ttl=600)
def fetch_and_train():
    model_builder.fetch()

if st.button(":green[Fetch Data]"):
    st.cache_data.clear()
    fetch_and_train()