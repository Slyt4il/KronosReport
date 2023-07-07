import streamlit as st
import utils.calc as calc
import utils.helper as helper
import random


def def_position(args):
    student, pos = args
    label = '{} {}\'s WR%'.format(helper.convert_readable(pos), helper.convert_readable(student))
    value, delta, count = calc.def_positional_winrate(student, pos)
    value = str(value) + '%'
    delta = str(delta) + '%'
    delta_color = 'normal'
    help = '{} {}\'s winrate compared to the mean of her other defense positions. She appeared {} times here.'.format(helper.convert_readable(pos), helper.convert_readable(student), count)
    card = st.container()
    with card:
        col1, col2 = st.columns([1,1.5])
        with col1:
            st.image('images/card/card_{}.png'.format(student))
        with col2:
            st.metric(label, value, delta=delta, delta_color=delta_color, help=help, label_visibility="visible")
    return card

def strongest_duo(args):
    student = args
    label = '{}\'s Strongest Duo'.format(helper.convert_readable(student))
    value, delta, wr, apps = calc.strongest_specials_duo(student)
    value = helper.convert_readable(value)
    delta = str(delta) + 'pts'
    delta_color = 'off'
    help = '{}\'s is most effective when paired with {}. They appeared {} times together and have a {}% winrate.'.format(helper.convert_readable(student), value, apps, wr)
    card = st.container()
    with card:
        col1, col2 = st.columns([1,1.5])
        with col1:
            st.image('images/card/card_{}.png'.format(student))
        with col2:
            st.metric(label, value, delta=delta, delta_color=delta_color, help=help, label_visibility="visible")
    return card

#################################################################

all_cards = [
    (def_position, ['shun', 'd1']),
    (def_position, ['shun', 'd2']),
    (def_position, ['shun', 'd3']),
    (def_position, ['shun', 'd4']),
    (def_position, ['tsubaki', 'd1']),
    (def_position, ['tsubaki', 'd2']),
    (def_position, ['tsubaki', 'd3']),
    (def_position, ['tsubaki', 'd4']),
    (def_position, ['marina', 'd1']),
    (def_position, ['marina', 'd2']),
    (def_position, ['marina', 'd3']),
    (def_position, ['marina', 'd4']),
    (def_position, ['yuuka', 'd1']),
    (def_position, ['yuuka', 'd2']),
    (def_position, ['yuuka', 'd3']),
    (def_position, ['yuuka', 'd4']),
    (def_position, ['iori', 'd1']),
    (def_position, ['iori', 'd2']),
    (def_position, ['iori', 'd3']),
    (def_position, ['iori', 'd4']),
    (def_position, ['haruna', 'd1']),
    (def_position, ['haruna', 'd2']),
    (def_position, ['haruna', 'd3']),
    (def_position, ['haruna', 'd4']),
    (strongest_duo, 'ayane_(swimsuit)'),
    (strongest_duo, 'mashiro_(swimsuit)'),
    (strongest_duo, 'iroha'),
    (strongest_duo, 'utaha'),
    (strongest_duo, 'serina'),
    (strongest_duo, 'nodoka_(hot_spring)'),
]

cards = all_cards.copy()

def refresh_cards():
    global cards
    cards = all_cards.copy()

def get_random_card():
    if cards:
        card, args = random.choice(cards)
        cards.remove((card, args))
    else:
        return None
    return card(args)