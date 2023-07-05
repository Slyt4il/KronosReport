import streamlit as st
import pandas as pd
import re
import studentinfo
import helper

st.set_page_config(
    page_title="Tier List - Kronos PVP Report",
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

file_name = 'ss4_urban'
data = pd.read_csv('datasets/' + file_name + '.csv')
df = pd.DataFrame(data)

def calculate_ratings(df):
    ratings = []

    total_students = df.shape[0] * 2
    all_students = studentinfo.get_list_all()
    df_atk, df_def = split_df(df)
    for student in all_students:
        escaped_student = re.escape(student)
        literal_student = rf'(?<!\S){escaped_student}(?!\S)'

        pick_count = df.stack().str.count(literal_student).sum()
        pick_rate = round(pick_count / total_students, 4)

        atk_wins = df_atk[(df_atk['attacker_won'] == 1)].stack().str.count(literal_student).sum()
        def_wins = df_def[(df_def['attacker_won'] == 0)].stack().str.count(literal_student).sum()
        win_count = int(atk_wins + def_wins)
        win_rate = round(win_count / pick_count, 4)

        rating = int((500 * pick_rate) + (1000 * win_rate * pick_rate))
        ratings.append([student, pick_count, pick_rate, win_count, win_rate, rating])
    return ratings

def split_df(df):
    df_atk = df.iloc[:, :6]
    df_def = df.iloc[:, 6:12]
    attacker_won = df['attacker_won']
    df_atk = pd.concat([df_atk, attacker_won], axis=1)
    df_def = pd.concat([df_def, attacker_won], axis=1)
    return df_atk, df_def

def get_grade(value):
    return ':violet[SS]' if value >= 900 else ':green[S]' if value >= 580 else ':blue[A]' if value >= 280 else ':blue[B]' if value >= 130 else ':orange[C]' if value >= 30 else ':red[D]'

s = st.selectbox('Sort by', ['Rating', 'Battles', 'Wins', 'WR%'])
st.markdown('---')

ratings = calculate_ratings(df)
ratings.sort(key=lambda x: x[-1 if s == 'Rating' else 1 if s == 'Battles' else 3 if s == 'Wins' else 4], reverse=True)
img_dir = 'images/'
for i in range(len(ratings)):
    student_name, battles, pr, wins, wr, rating = ratings[i][0], ratings[i][1], ratings[i][2], ratings[i][3], ratings[i][4], ratings[i][5]
    col1, sep1, col2 = st.columns([1,1.5,10])
    with col1:
        st.image(img_dir + student_name + '.png', width=120)
    with col2:
        subcol1, subsep1, subcol2 = st.columns([5,1,1])
        with subcol1:
            st.subheader(helper.convert_readable(ratings[i][0]))
            st.caption('**Battles: {} | Pick Rate: {}%**'.format(int(battles), round(pr * 100, 2)))
            st.caption('**Wins: {} | Win Rate: {}%**'.format(wins, round(wr * 100, 2)))
        with subcol2:
            st.subheader('**{}**'.format(get_grade(rating)))
    st.divider()

with st.expander("**How are ratings calculated?**"):
    st.write('The scoring formula is *(500 \* pr%) + (1000 \* wr% \* pr%)*')
    st.write('At 100% pick rate and 50% win rate, a student would receive the full 1,000 points.')
    st.caption('SS >900 | S 580-899 | A 280-579 | B 130-279 | C 30-129 | D <30')