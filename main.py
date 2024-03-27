from bs4 import BeautifulSoup
import requests
import json


def get_bundesland():
    url = 'https://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    bundesland_table = soup.find_all('table', {'class': 'wikitable sortable zebra'})[0]
    bundesland = {}
    for row in bundesland_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        bundesland_name = columns[0].find('span').text
        bundesland_code = columns[0].text.split(' ')[1].strip('()')

        bundesland[bundesland_code] = bundesland_name

    return bundesland


def get_city():
    url = 'https://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    city_table = soup.find_all('dd')

    city = []
    for entry in city_table:
        city_name = entry.find('a').text
        city_code = entry.text.split('(')[-1].rstrip(')').strip() if '(' in entry.text and ')' in entry.text else ''
        city.append({'name': city_name, 'code': city_code})

    return city


def city_assign_bundeslandname():
    bundesland = get_bundesland()
    cities = get_city()
    city_bundesland = []
    for city in cities:
        bundesland_name = bundesland.get(city['code'], '')
        city_bundesland.append({'name': city['name'], 'bundesland': bundesland_name})
    return city_bundesland
def main():
    city_bundesland = city_assign_bundeslandname()
    with open('city_bundesland.json', 'w') as f:
        json.dump(city_bundesland, f, indent=4, ensure_ascii=False)
    # print(city_bundesland)

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
