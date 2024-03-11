import requests
from bs4 import BeautifulSoup
import json
import re


def parse_vacancies():
    print('starting scrap process')
    i = 0
    url = "https://hh.ru/search/vacancy?text=Python&area=1&area=2"  # Москва и Санкт-Петербург
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    regex = re.compile(r'vacancy-serp__vacancy vacancy-serp__vacancy_\w*')
    vacancies = soup.find_all('div', {'data-qa': regex})

    result = []
    print('init complete')
    for vacancy in vacancies:
        try:
            title = vacancy.find('span', {'data-qa': 'serp-item__title'}).text
            link = vacancy.find('a', {'class': 'bloko-link'})['href']
            company = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
            city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            salary = salary.text if salary else 'Не указано'

            response2 = requests.get(link, headers=headers)
            soup2 = BeautifulSoup(response2.content, 'html.parser')
            description = soup2.find('div', {'data-qa': 'vacancy-description'}).text
            if 'Django' in description or 'Flask' in description:
                result.append({
                    'title': title,
                    'link': link,
                    'company': company,
                    'city': city,
                    'salary': salary
                })
            i += 1
            print('vacancy number ' + str(i) + ' scanned!')
        except:
            print('failed to get data for position ' + str(i))
    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print('complete! check vacancies.json')
    print('PS: if something didnt load, its recommended to restart the script')

parse_vacancies()
