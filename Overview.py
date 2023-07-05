import streamlit as st
import utils.helper as helper
import utils.cardgen as cardgen
import random

st.set_page_config(
    page_title="Kronos PVP Report",
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
                    overflow-x: clip;
                }
            .css-1oe5cao {
                    max-height: 66vh;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
st.sidebar.subheader("PVP Season: 4 🏙️ (Urban)")

st.write("# Kronos PVP Report")
st.write(
        f'<hr style="background-color: #00c0f2; margin-top: 0;'
        ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )

st.subheader("A data-driven analysis of Blue Archive Tactical Challenge")

st.write("")
st.write("")
st.write("")
st.write("")

with st.container():
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        cardgen.get_random_card()
        cardgen.get_random_card()
        cardgen.get_random_card()
    with col2:
        cardgen.get_random_card()
        cardgen.get_random_card()
        cardgen.get_random_card()
    with col3:
        cardgen.get_random_card()
        cardgen.get_random_card()
        cardgen.get_random_card()

    helper.style_metric_cards(border_left_color='#' + ''.join(random.choices('0123456789ABCDEF', k=6)))