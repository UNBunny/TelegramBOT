import requests
import json
from bs4 import BeautifulSoup


def get_drugs_info(page, drug_name):
    page = requests.get(f"https://farmakopeika.ru/search?query={drug_name}&page={page}&limit=48")
    soup = BeautifulSoup(page.text, 'html.parser')
    drugs_info = soup.findAll('div', "product")
    return drugs_info


def get_pharmacies(drug_name):
    page = requests.get(
        f"https://farmakopeika.ru/search?query={drug_name}&limit=48")  # Выполняет GET-запрос к веб-странице и возвращает ответ сервера, который сохраняется в переменной
    print(page.status_code)  # Выводит HTTP-статус код ответа сервера на консоль.
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        pages = int(soup.findAll('a', 'pagination__item')[-1].text)
    except: pages = 1
    drugs_dict = {}
    i = int()

    for page in range(1, pages + 1):
        drugs_info = get_drugs_info(page, drug_name)
        for drugs in drugs_info:
            drugs_title = " ".join(drugs.find("div", "product__title").text.split())
            drugs_price = " ".join(drugs.find("span", "product__price-text").text.split())
            drugs_available = " ".join(drugs.find("div", "product__spec-value").text.split())
            drugs_url = drugs.find("a", "product__link").get("href")
            i += 1
            drugs_dict[i] = {
                "drugs_title": drugs_title,
                "drugs_price": drugs_price,
                "drugs_available": drugs_available,
                "drugs_url": drugs_url,
            }

    with open("drugs_dict.json", "w", encoding='UTF-8') as file:
        json.dump(drugs_dict, file, indent=4, ensure_ascii=False)
