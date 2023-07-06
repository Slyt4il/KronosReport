import streamlit as st
import utils.calc as calc
import utils.helper as helper
import numpy as np

def get_random_card():
    student = np.random.choice(['shun', 'iori', 'tsubaki', 'haruna', 'yuuka', 'marina']) 
    pos = np.random.choice(['d1', 'd2', 'd3', 'd4'])
    label = '{} {} Win%'.format(helper.convert_readable(pos), helper.convert_readable(student))
    value, delta = calc.positional_winrate(student, pos)
    value = str(value) + '%'
    delta = str(delta) + '%'
    delta_color = 'normal'
    help = '{} {}\'s winrates compared to her nominal value.'.format(helper.convert_readable(pos), helper.convert_readable(student))
    card = st.container()
    with card:
        col1, col2 = st.columns([1,1.5])
        with col1:
            st.image('images/card/card_shun.png')
        with col2:
            st.metric(label, value, delta=delta, delta_color=delta_color, help=help, label_visibility="visible")
        st.write('')
    return card