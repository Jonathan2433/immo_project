import requests
from bs4 import BeautifulSoup


class NestennScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_soup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    def scraper_details(self, soup_detail):
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

    def get_announcements(self, url):
        soup = self.get_soup(url)
        announcements = soup.select("div.property_info_content")
        for announcement in announcements:
            link = announcement.select_one("a")['href']
            title = announcement.select_one(".property_title").text.strip()

            price = None
            maybe_price = announcement.select_one(":contains('€')")
            if maybe_price:
                price = maybe_price.text.strip()

            print(f"Lien: {link}")
            print(f"Titre: {title}")
            print(f"Prix: {price}")

            soup_detail = self.get_soup(link)
            self.scraper_details(soup_detail)

    def start(self, ville, type_bien, prix_max):
        url = f'{self.base_url}/?action=listing&prestige=0&transaction=acheter&list_ville={ville}&list_type={type_bien}&type={type_bien}&prix_max={prix_max}'
        self.get_announcements(url)


if __name__ == "__main__":
    scraper = NestennScraper('https://immobilier-merignac.nestenn.com')
    scraper.start("33130+Bègles", "Maison", "500000")
