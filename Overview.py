import streamlit as st
import pandas as pd
import helper

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
                    overflow-x: hidden;
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

st.markdown(
    """
    The goal is to analyze recorded pvp matches and provide insight to the meta of Blue Archive arena.
"""
)
