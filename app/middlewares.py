from ast import literal_eval
import pandas as pd
import moviesMain

def getUserStats(userdata, username):
    # Carregando dados e setando arrays de resultados
    userdata = userdata.astype({"rating": float})
    movies = pd.read_csv("datasets/merged_movies_v1.csv", index_col=0)
    userstats = pd.read_csv("datasets/userstats3.csv", index_col=0)
    categories = userstats.columns.to_list()[2:]
    ratings = [username, 1]
    ratings.extend([0] * (len(userstats.columns)-3))
    count = [username, 2]
    count.extend([0] * (len(userstats.columns)-3))
    mean = [username, 3]
    for index, row in userdata.iterrows():
        # Caso o filme nao existe na DB, faz o scrape dele e salva as categorias do filme atual
        if len(movies[movies["movie"] == row.movie]) == 0:
            movie_properties = moviesMain.getMovieInfo([row.movie]).iloc[0]
            current_categories = list(movie_properties.genre)
            current_categories.extend(list(movie_properties.theme))
            current_categories.extend(list(movie_properties.mini_theme))
        else:
            movie_properties = movies[movies["movie"] == row.movie].iloc[0]
            current_categories = literal_eval(movie_properties.genre)
            current_categories.extend(literal_eval(movie_properties.theme))
            current_categories.extend(literal_eval(movie_properties.mini_theme))
        # Salva por categoria a nota do usuario
        for category in categories:
            if category in current_categories:
                if float(row.rating) > 0.5:
                    ratings[categories.index(category)+2] += row.rating
                    count[categories.index(category)+2] += 1
    # Adiciona a coluna de linha de media de cada categoria
    for i in range(2,len(userstats.columns.to_list())-1):
        if count[i] == 0:
            mean.append(0)
        else:
            mean.append(round(ratings[i] / count[i], 2))
    rated_movies_ratings = userdata.query('rating > 0.5')["rating"]
    # Adiciona colunas gerais, de contagem de filmes, soma de notas e media
    ratings.append(round(sum(rated_movies_ratings),2))
    count.append(round(len(rated_movies_ratings),2))
    if len(rated_movies_ratings) == 0: mean.append(0)
    else: mean.append(round(sum(rated_movies_ratings)/len(rated_movies_ratings),2))
    # Retorna listas das estatisticas do usuario parametrizado
    return [ratings, count, mean]