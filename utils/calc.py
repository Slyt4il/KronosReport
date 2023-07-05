import pandas as pd
import utils.studentinfo as studentinfo
import re

file_name = 'ss4_urban'
data = pd.read_csv('datasets/' + file_name + '.csv')
df = pd.DataFrame(data)

def update(data, df):
    data = pd.read_csv('datasets/' + file_name + '.csv')
    df = pd.DataFrame(data)

def split_df(df):
    df_atk = df.iloc[:, :6]
    df_def = df.iloc[:, 6:12]
    attacker_won = df['attacker_won']
    df_atk = pd.concat([df_atk, attacker_won], axis=1)
    df_def = pd.concat([df_def, attacker_won], axis=1)
    return df_atk, df_def

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

def recalculate():
    update(data, df)
    calculate_ratings(df)

student_ratings = calculate_ratings(df)
def get_ratings():
    return student_ratings

############################################################################################

def positional_winrate(student, pos):
    normal_winrate = [sub_arr for sub_arr in student_ratings if len(sub_arr) > 0 and sub_arr[0] == student][0][4]
    count = (df[pos].str.contains(student)).sum()
    wins = ((df[pos].str.contains(student)) & (df['attacker_won'] == 0)).sum()
    wr = round((wins / count) * 100, 2)
    delta = round(wr - (normal_winrate * 100), 2)
    return wr, delta