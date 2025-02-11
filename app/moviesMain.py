from bs4 import BeautifulSoup
import pandas as pd
import requests

# Recebe uma lista filmes e retorna dataframe com seus dados
def getMovieInfo(data):
    # Carregando DB e declarando variaveis para salvar os dados
    movies_db = pd.read_csv("datasets/merged_movies_v1.csv")
    current_movies = movies_db.movie.tolist()

    movie = []
    avg = []
    movie_length = []
    director = []
    studio = []
    country = []
    language = []
    genre = []
    theme = []
    mini_theme = []
    for movie_name in data:
        # Caso o filme ja esteja na DB passar para o proximo
        if movie_name in current_movies:
            continue
        # Variaveis para cada filme
        current_director = []
        current_studio = []
        current_country = []
        current_language = []
        current_genre = []
        current_theme = []
        current_mini_theme = []
        list_url = f"https://letterboxd.com/film/{movie_name}/"
        page_response = requests.get(list_url)
        page = BeautifulSoup(page_response.content, 'html.parser')
        details = BeautifulSoup(page_response.content, 'html.parser')
        for i in details.find_all("a", class_="text-slug"):
            if 'href' in i.attrs.keys() and "/director/" == i.get("href")[:10]:
                current_director.append(i.get("href").split("/")[-2])
            if 'href' in i.attrs.keys() and "/studio/" == i.get("href")[:8]:
                current_studio.append(i.get("href").split("/")[-2])
            if 'href' in i.attrs.keys() and "/films/country/" == i.get("href")[:15]:
                current_country.append(i.get("href").split("/")[-2])
            if 'href' in i.attrs.keys() and "/films/language/" == i.get("href")[:16]:
                current_language.append(i.get("href").split("/")[-2])
            if 'href' in i.attrs.keys() and "/films/genre/" == i.get("href")[:13]:
                current_genre.append(i.get("href").split("/")[-2])
            if 'href' in i.attrs.keys() and "/films/theme/" == i.get("href")[:13]:
                current_theme.append(i.get("href").split("/")[-4])
            if 'href' in i.attrs.keys() and "/films/mini-theme/" == i.get("href")[:18]:
                current_mini_theme.append(i.get("href").split("/")[-4])
        movie.append(movie_name)
        for i in page.find_all(
                lambda tag: tag.name == "meta" and 'content' in tag.attrs.keys() and "out of 5" in tag["content"]):
            avg.append(i.attrs["content"][:i.attrs["content"].index("out") - 1])
        # Lidando com problema de falta de dados em determinados filmes
        if len(movie) > len(avg):
            avg.append(0)
        # Adicionar tempo do filme, caso tenha
        if details.find("p", class_="text-link text-footer") == None:
            movie_length.append(0)
        elif "mins" in details.find("p", class_="text-link text-footer").text.strip():
            movie_length.append(details.find("p", class_="text-link text-footer").text.strip()[
                                :details.find("p", class_="text-link text-footer").text.strip().index("mins") - 1])
        else:
            movie_length.append(0)
        director.append(current_director)
        studio.append(current_studio)
        country.append(current_country)
        language.append(current_language)
        genre.append(current_genre)
        theme.append(current_theme)
        mini_theme.append(current_mini_theme)

    lists_dict = {'movie': movie,
                  'avg': avg,
                  'length': movie_length,
                  'director': director,
                  'studio': studio,
                  'country': country,
                  'language': language,
                  'genre': genre,
                  'theme': theme,
                  'mini_theme': mini_theme}

    # Retorna dataframe com os filmes
    return pd.DataFrame(lists_dict)