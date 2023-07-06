from PIL import Image
import streamlit as st
import re

def get_icon():
    return Image.open('favicon.png')

def convert_readable(input_string):
    return ' '.join(word.title() for word in input_string.split('_'))

def escape_student(student):
    escaped_student = re.escape(student)
    literal_student = rf'(?<!\S){escaped_student}(?!\S)'
    return literal_student

def style_metric_cards(
    background_color: str = "#FFF",
    border_size_px: int = 1,
    border_color: str = "#CCC",
    border_radius_px: int = 5,
    border_left_color: str = "#9AD8E1",
    box_shadow: bool = True,
):

    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-testid="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                {box_shadow_str}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
