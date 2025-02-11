from bs4 import BeautifulSoup
import pandas as pd
import requests

# Funcao retorna filmes e notas do usuario parametrizado
def getUserInfo(username):
    usuario = []
    filme = []
    nota = []
    url = f"https://letterboxd.com/{username}/films/page/1/"
    response = requests.get(url)
    page = BeautifulSoup(response.content, 'html.parser')

    # Range2 é a variavel que vai indicar o numero de paginas de filmes a serem scrapped, iniciando em 1
    range2 = 1
    if not page.find_all("li", class_="paginate-page") == []:
        range2 = int(page.find_all("li", class_="paginate-page")[-1].text)
    for j in range(range2):
        url = f"https://letterboxd.com/{username}/films/page/{j + 1}/"
        response = requests.get(url)
        page = BeautifulSoup(response.content, 'html.parser')
        data = page.find_all("li", class_="poster-container")

        # Salva todos os filmes com suas notas em cada pagina
        for i in data:
            usuario.append(username)
            filme.append(i.find("div").get("data-film-slug"))
            # Valida se existe uma nota atribuida ao filme assistido
            if i.find("p").find("span") is not None and 'rated' in i.find("p").find("span").get("class")[3]:
                nota.append(i.find("p").find("span").get("class")[3].split("ated-")[1])
            else:
                nota.append(None)

    # Retorna um dataframe com todos os filmes assistidos e suas notas do usuario parametrizado
    return pd.DataFrame({'users': usuario, 'movie':filme,'rating':nota})