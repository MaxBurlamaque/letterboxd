import pandas as pd
import users, middlewares

# Funcao retorna os 5 usuarios com mais alta compatibilidade de notas baseados em notas por categorias
# levando em consideração a média geral
def getTwin(user):
    usersstats = pd.read_csv("datasets/userstats3.csv", index_col=0)
    user_info = usersstats[usersstats["user"] == user]

    # Validando se o usuario esta na base de dados ou se não, puxar as informações dele
    if len(user_info) < 2:
        new_user = middlewares.getUserStats(users.getUserInfo(user), user)
        user_info.loc[len(user_info)] = new_user[0]
        user_info.loc[len(user_info)] = new_user[1]
        user_info.loc[len(user_info)] = new_user[2]

    # Pegando as categorias com maior nota do usuario
    possible = []
    for column in user_info:
        if column not in ('Unnamed: 0', 'user', 'tipo', 'geral') and user_info[column].iloc[1] > 10:
            possible.append([column, user_info[column].iloc[2]])
    finalist = sorted(possible, key=lambda x: float(x[1]), reverse=True)[:5]
    finalist = list(map(lambda x: [x[0], round(x[1] - user_info["geral"].iloc[2], 2)], finalist))

    # Iterando sobre os usuarios no banco de dados e selecionando os mais parecidos
    users_gp = usersstats.groupby("user")
    candidatos = []
    for user, data in users_gp:
        print(finalist)
        if data.iloc[1][finalist[0][0]] > 6 and data.iloc[1][finalist[1][0]] > 6 and data.iloc[1][finalist[2][0]] > 6 and \
                data.iloc[1][finalist[3][0]] > 6 and data.iloc[1][finalist[4][0]] > 6:
            diff = abs((data.iloc[2][finalist[0][0]] - data.iloc[2]["geral"]) - finalist[0][1])
            diff += abs((data.iloc[2][finalist[1][0]] - data.iloc[2]["geral"]) - finalist[1][1])
            diff += abs((data.iloc[2][finalist[2][0]] - data.iloc[2]["geral"]) - finalist[2][1])
            diff += abs((data.iloc[2][finalist[3][0]] - data.iloc[2]["geral"]) - finalist[3][1])
            diff += abs((data.iloc[2][finalist[4][0]] - data.iloc[2]["geral"]) - finalist[4][1])
            candidatos.append([user, diff])

    # Retorna os 5 candidatos mais bem posicionados
    return sorted(candidatos, key=lambda x: float(x[1]), reverse=False)[:5]

# TO-DO Funcao retorna a relaçao das notas entre 2 usuarios
def compareTwo(user1, user2):
    return "r"