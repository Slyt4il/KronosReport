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

def update():
    global data, df, df_atk, df_def
    data = pd.read_csv('datasets/' + file_name + '.csv')
    df = pd.DataFrame(data)
    df_atk, df_def = split_df(df)


def calculate_ratings(df):
    ratings = []

    total_teams = df.shape[0] * 2
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
        pick_rate = round(pick_count / total_teams, 4)
        win_count = int(atk_wins + def_wins)
        win_rate = round(win_count / pick_count, 4)

        rating = int((500 * pick_rate) + (1000 * win_rate * pick_rate))
        ratings.append([student, pick_count, pick_rate, win_count, win_rate, atk_count, atk_win_rate, def_count, def_win_rate, rating])
    return ratings

def recalculate():
    update()
    calculate_ratings(df)

student_ratings = calculate_ratings(df)
def get_ratings():
    return student_ratings

############################################################################################


def def_positional_winrate(student, pos):
    d1_wr = round(duckdb.sql(f"SELECT (COUNT(CASE WHEN d1 = '{student}' AND attacker_won = 0 THEN 1 END) * 100.0) / COUNT(CASE WHEN d1 = '{student}' THEN 1 END) FROM df_def;").fetchone()[0], 2)
    d2_wr = round(duckdb.sql(f"SELECT (COUNT(CASE WHEN d2 = '{student}' AND attacker_won = 0 THEN 1 END) * 100.0) / COUNT(CASE WHEN d2 = '{student}' THEN 1 END) FROM df_def;").fetchone()[0], 2)
    d3_wr = round(duckdb.sql(f"SELECT (COUNT(CASE WHEN d3 = '{student}' AND attacker_won = 0 THEN 1 END) * 100.0) / COUNT(CASE WHEN d3 = '{student}' THEN 1 END) FROM df_def;").fetchone()[0], 2)
    d4_wr = round(duckdb.sql(f"SELECT (COUNT(CASE WHEN d4 = '{student}' AND attacker_won = 0 THEN 1 END) * 100.0) / COUNT(CASE WHEN d4 = '{student}' THEN 1 END) FROM df_def;").fetchone()[0], 2)
    wr = [d1_wr, d2_wr, d3_wr, d4_wr]
    target = wr[int(pos[-1])-1]
    wr.remove(target)
    delta = round(target - (sum(wr) / len(wr)), 2)
    count = duckdb.sql(f"SELECT COUNT({pos}) FROM df_def WHERE {pos} = '{student}';").fetchone()[0]
    return target , delta, count

def strongest_specials_duo(student):
    candidates = list(studentinfo.get_keys_specials())
    candidates.remove(student)
    strongest_candidate = 'None'
    strongest_candidate_wr = 0
    strongest_candidate_score = 0
    apps = 0
    for candidate in candidates:
        atk_ex_count = duckdb.sql(f"SELECT COUNT(*) FROM df_atk WHERE (a5 = '{student}' OR a6 = '{student}');").fetchone()[0]
        def_ex_count = duckdb.sql(f"SELECT COUNT(*) FROM df_def WHERE (d5 = '{student}' OR d6 = '{student}');").fetchone()[0]
        atk_count = duckdb.sql(f"SELECT COUNT(*) FROM df_atk WHERE (a5 = '{student}' OR a6 = '{student}') AND (a5 = '{candidate}' OR a6 = '{candidate}');").fetchone()[0]
        atk_wins = duckdb.sql(f"SELECT COUNT(*) FROM df_atk WHERE (a5 = '{student}' OR a6 = '{student}') AND (a5 = '{candidate}' OR a6 = '{candidate}') AND attacker_won = 1;").fetchone()[0]
        def_count = duckdb.sql(f"SELECT COUNT(*) FROM df_def WHERE (d5 = '{student}' OR d6 = '{student}') AND (d5 = '{candidate}' OR d6 = '{candidate}');").fetchone()[0]
        def_wins = duckdb.sql(f"SELECT COUNT(*) FROM df_def WHERE (d5 = '{student}' OR d6 = '{student}') AND (d5 = '{candidate}' OR d6 = '{candidate}') AND attacker_won = 0;").fetchone()[0]
        count = atk_count + def_count
        ex_count = atk_ex_count + def_ex_count
        wr = round((atk_wins + def_wins) / (count), 4) if (count) > 0 else 0
        pr = round(count / ex_count, 2)
        score = int(2000 * wr * pr)
        if score > strongest_candidate_score:
            strongest_candidate_wr = round(wr * 100, 2)
            strongest_candidate_score = score
            strongest_candidate = candidate
            apps = count
            
    return strongest_candidate, strongest_candidate_score, strongest_candidate_wr, apps