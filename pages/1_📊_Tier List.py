import streamlit as st
import utils.calc as calc
import utils.helper as helper

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
                    overflow-x: clip;
                }
            .css-1oe5cao {
                    max-height: 66vh;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.sidebar.subheader("PVP Season: 4 🏙️ (Urban)")

def get_grade(value):
    return ':violet[SS]' if value >= 900 else ':green[S]' if value >= 580 else ':blue[A]' if value >= 280 else ':blue[B]' if value >= 130 else ':orange[C]' if value >= 30 else ':red[D]'

s = st.selectbox('Sort by', ['Rating', 'Battles', 'Wins', 'WR%'])
st.markdown('---')

ratings = calc.get_ratings()
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