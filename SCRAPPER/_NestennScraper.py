from bs4 import BeautifulSoup
import requests


class NestennScraper:
    """
    Cette classe fournit des méthodes pour scraper les annonces immobilières du site Nestenn.
    Elle permet d'extraire :
        - Les détails d'une annonce (titre, description, image, etc.)
        - Les informations de base de chaque annonce listée (lien, titre, prix)

    Args:
        list_ville (list): Liste des villes et/ou départements à inclure dans la requête.
        list_type (list, optional): Liste des types de propriétés à rechercher.
        chambres (int, optional): Nombre de chambres souhaitées.
        pieces (int, optional): Nombre de pièces souhaitées.
        prix_max (int, optional): Prix maximum souhaité pour les propriétés.
    """

    BASE_URL = "https://nestenn.com"

    def __init__(self, list_ville: list, list_type: list = None, chambres: int = None, pieces: int = None,
                 prix_max: int = None):
        assert list_ville, "Au moins une ville ou un département doit être fourni."

        self.list_ville = list_ville
        self.list_type = list_type
        self.chambres = chambres
        self.pieces = pieces
        self.prix_max = prix_max

    def _construct_url(self) -> str:
        """
            Construit l'URL avec les paramètres fournis à l'initialisation.
        """
        query_parameters = {
            'action': 'listing',
            'prestige': '0',
            'transaction': 'acheter',
            'list_ville': ",".join(self.list_ville),
        }

        if self.list_type:
            query_parameters['list_type'] = ",".join(self.list_type)
            query_parameters['type'] = ",".join(self.list_type)
        if self.chambres:
            query_parameters['chambres'] = str(self.chambres)
        if self.pieces:
            query_parameters['pieces'] = str(self.pieces)
        if self.prix_max:
            query_parameters['prix_max'] = str(self.prix_max)

        query_string = "&".join(f"{key}={value}" for key, value in query_parameters.items())

        return f"{self.BASE_URL}/?{query_string}"

    def start(self) -> None:
        """
        Démarre le processus de scraping en utilisant les paramètres de recherche fournis à l'initialisation.
        """
        query_url = self._construct_url()
        response = requests.get(query_url)
        soup = BeautifulSoup(response.text, "html.parser")

        annonces = soup.select("div.property_info_content")

        for annonce in annonces:
            relative_link = annonce.select_one("a")['href']
            lien = f"{self.BASE_URL}/{relative_link}"  # Ajoutez l'URL de base ici
            titre = annonce.select_one(".property_title").text.strip()

            prix = None
            maybe_prix = annonce.select_one(":-soup-contains('€')")  # Utilisez :-soup-contains
            if maybe_prix:
                prix = maybe_prix.text.strip()

            print(f"Lien: {lien}")
            print(f"Titre: {titre}")
            print(f"Prix: {prix}")

            # Accéder à la page détaillée de l'annonce
            response_detail = requests.get(lien)
            soup_detail = BeautifulSoup(response_detail.text, "html.parser")

            # Scrapper les détails
            self.scraper_details(soup_detail)

    def scraper_details(self, soup_detail):
        """
        Extraire les détails d'une annonce à partir de sa page de détail.

        Args:
            soup_detail (BeautifulSoup): Objet BeautifulSoup de la page détaillée.

        Returns:
            None: Cette méthode imprime les détails à l'écran.
        """
        # Extraire le titre
        titre_element = soup_detail.select_one(".square_title")
        if titre_element:
            titre = titre_element.text.strip()
            print(f"Titre: {titre}")
        else:
            print("Titre introuvable")

        # Extraire la description
        description_element = soup_detail.select_one(".square_text_p")
        if description_element:
            description = description_element.text.strip()
            print(f"Description: {description}")
        else:
            print("Description introuvable")

        # Extraire l'image
        image_element = soup_detail.select_one(".square_content.square_img.no_mobile")
        if image_element and 'style' in image_element.attrs:
            image_url = image_element['style']
            if '("' in image_url and '")' in image_url:
                image_url = image_url.split('("')[1].split('")')[0]
                print(f"Image URL: {image_url}")
            else:
                print("URL de l'image introuvable")
        else:
            print("Élément d'image introuvable")

        # Extraire les détails du bien
        details = soup_detail.select(".icon_property_description")
        if details:
            for detail in details:
                print(detail.text.strip())
        else:
            print("Détails du bien introuvables")

        print("---------")

