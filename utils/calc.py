import pandas as pd
import duckdb
import utils.studentinfo as studentinfo
import utils.helper as helper

file_name = 'ss4_urban'
data = pd.read_csv('datasets/' + file_name + '.csv')

def split_df(df):
    df_atk = df.iloc[:, :6]
    df_def = df.iloc[:, 6:12]
    attacker_won = df['attacker_won']
    df_atk = pd.concat([df_atk, attacker_won], axis=1)
    df_def = pd.concat([df_def, attacker_won], axis=1)
    return df_atk, df_def

df = pd.DataFrame(data)
df_atk, df_def = split_df(df)

def update(data, df):
    data = pd.read_csv('datasets/' + file_name + '.csv')
    df = pd.DataFrame(data)


def calculate_ratings(df):
    ratings = []

    total_students = df.shape[0] * 2
    all_students = studentinfo.get_list_all()
    for student in all_students:
        escaped_student = helper.escape_student(student)

        atk_count = df_atk.stack().str.count(escaped_student).sum()
        atk_wins = df_atk[(df_atk['attacker_won'] == 1)].stack().str.count(escaped_student).sum()
        atk_win_rate = round(atk_wins / atk_count, 4) if atk_count > 0 else 0
        def_count = df_def.stack().str.count(escaped_student).sum()
        def_wins = df_def[(df_def['attacker_won'] == 0)].stack().str.count(escaped_student).sum()
        def_win_rate = round(def_wins / def_count, 4) if def_count > 0 else 0
        pick_count = int(atk_count + def_count)
        pick_rate = round(pick_count / total_students, 4)
        win_count = int(atk_wins + def_wins)
        win_rate = round(win_count / pick_count, 4)

        rating = int((500 * pick_rate) + (1000 * win_rate * pick_rate))
        ratings.append([student, pick_count, pick_rate, win_count, win_rate, atk_count, atk_win_rate, def_count, def_win_rate, rating])
    return ratings

def recalculate():
    update(data, df)
    calculate_ratings(df)

student_ratings = calculate_ratings(df)
def get_ratings():
    return student_ratings

############################################################################################


def def_positional_winrate(student, pos):
    student = helper.escape_student(student)
    d1_wr = round((((df_def['d1'].str.contains(student)) & (df_def['attacker_won'] == 0)).sum() / (df_def['d1'].str.contains(student)).sum()) * 100, 2)
    d2_wr = round((((df_def['d2'].str.contains(student)) & (df_def['attacker_won'] == 0)).sum() / (df_def['d2'].str.contains(student)).sum()) * 100, 2)
    d3_wr = round((((df_def['d3'].str.contains(student)) & (df_def['attacker_won'] == 0)).sum() / (df_def['d3'].str.contains(student)).sum()) * 100, 2)
    d4_wr = round((((df_def['d4'].str.contains(student)) & (df_def['attacker_won'] == 0)).sum() / (df_def['d4'].str.contains(student)).sum()) * 100, 2)
    wr = [d1_wr, d2_wr, d3_wr, d4_wr]
    target = wr[int(pos[-1])-1]
    wr.remove(target)
    delta = round(target - (sum(wr) / len(wr)), 2)
    count = df_def[pos].str.count(student).sum()
    return target , delta, count

def strongest_specials_duo(student):
    candidates = list(studentinfo.get_keys_specials())
    candidates.remove(student)
    strongest_candidate = 'None'
    strongest_candidate_wr = 0
    matches = 0
    for candidate in candidates:
        global df_atk, df_def
        d_atk = df_atk.drop(['a1', 'a2', 'a3', 'a4'], axis=1)
        d_def = df_def.drop(['d1', 'd2', 'd3', 'd4'], axis=1)
        atk_count = duckdb.sql(f"SELECT COUNT(*) FROM d_atk WHERE (a5 = '{student}' OR a6 = '{student}') AND (a5 = '{candidate}' OR a6 = '{candidate}');").fetchone()[0]
        atk_wins = duckdb.sql(f"SELECT COUNT(*) FROM d_atk WHERE (a5 = '{student}' OR a6 = '{student}') AND (a5 = '{candidate}' OR a6 = '{candidate}') AND attacker_won = 1;").fetchone()[0]
        def_count = duckdb.sql(f"SELECT COUNT(*) FROM d_def WHERE (d5 = '{student}' OR d6 = '{student}') AND (d5 = '{candidate}' OR d6 = '{candidate}');").fetchone()[0]
        def_wins = duckdb.sql(f"SELECT COUNT(*) FROM d_def WHERE (d5 = '{student}' OR d6 = '{student}') AND (d5 = '{candidate}' OR d6 = '{candidate}') AND attacker_won = 0;").fetchone()[0]
        wr = round(((atk_wins + def_wins) / (atk_count + def_count)) * 100, 2) if (atk_count + def_count) > 0 else 0
        if wr > strongest_candidate_wr:
            strongest_candidate_wr = wr
            strongest_candidate = candidate
            apps = atk_count + def_count
    return strongest_candidate, strongest_candidate_wr, apps