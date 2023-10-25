from bs4 import BeautifulSoup
import requests


class NestennScraper:
    """
    Cette classe fournit des méthodes pour scraper le site immobilier Nestenn:
        - Obtenir les détails des annonces
        - Récupérer l'URL, le titre et le prix des annonces

    Utilisez cette classe pour extraire des informations pertinentes sur les annonces immobilières de Nestenn.

    Args:
        base_url (str): URL de base pour initier le scraping.
    """

    # to do
    # make verification

    def __init__(self, base_url: str):
        self.base_url = base_url

    def scraper_details(self, soup: BeautifulSoup) -> None:
        """
        Extraire les détails d'une annonce à partir de sa page de détail.

        Args:
            soup (BeautifulSoup): Objet BeautifulSoup de la page détaillée.

        Returns:
            None: Cette méthode imprime les détails à l'écran.
        """
        # Extraire le titre
        titre_element = soup.select_one(".square_title")
        if titre_element:
            titre = titre_element.text.strip()
            print(f"Titre: {titre}")
        else:
            print("Titre introuvable")

        # Extraire la description
        description_element = soup.select_one(".square_text_p")
        if description_element:
            description = description_element.text.strip()
            print(f"Description: {description}")
        else:
            print("Description introuvable")

        # Extraire l'image
        image_element = soup.select_one(".square_content.square_img.no_mobile")
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
        details = soup.select(".icon_property_description")
        if details:
            for detail in details:
                print(detail.text.strip())
        else:
            print("Détails du bien introuvables")

        print("---------")

    def get_listings(self, url: str) -> None:
        """
        Extraire et afficher les annonces à partir de l'URL donnée.

        Args:
            url (str): L'URL de la page contenant les annonces.

        Returns:
            None: Cette méthode imprime les annonces à l'écran.
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        annonces = soup.select("div.property_info_content")

        for annonce in annonces:
            lien = annonce.select_one("a")['href']
            titre = annonce.select_one(".property_title").text.strip()

            prix = None
            maybe_prix = annonce.select_one(":contains('€')")
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
