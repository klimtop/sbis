import csv, random, requests, time
import pandas as pd
from bs4 import BeautifulSoup

def get_html(url):
    '''Получаем HTML страницы'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def get_url_info(url):
    '''Достаем информацию из HTML'''
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        address = soup.find('div', itemprop='address')
        address = '' if not address else address.text.strip()
        phone = soup.find('div', itemprop='telephone')
        phone = '' if not phone else phone.text.strip()
        email = soup.find('a', itemprop='email')
        email = '' if not email else email.text.strip()
        url = soup.find('a', itemprop='url')
        url = '' if not url else url.text.strip()
        revenue = soup.find('div', class_='cCard__Contacts-Revenue-Desktop').find('span', class_='cCard__BlockMaskSum')
        revenue = '' if not revenue else revenue.text.strip()
        director = soup.find('div', class_='cCard__Director-Name').find('span', itemprop='employee')
        director = '' if not director else director.text.strip()
        company_info = {'address': address, 'phone': phone, 'email': email, 'url':url, 'revenue': revenue, 'director': director}
    else:
        company_info = {'address': '404', 'phone': '404', 'email': '404', 'url': '404', 'revenue': '404', 'director': '404'}
    return company_info

url_list_input = []
df = pd.DataFrame()

# Открываем файл с исходными url и записываем их в список
with open('input.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        url = row[0].split(',')[0]
        url_list_input.append(url)

# Для каждого url из списка получаем HTML, в нем находим нужную информацию и записываем в df
for url in url_list_input:
    if 'http' in url:
        company_info = get_url_info(url)
    else:
        company_info = {'address': '404', 'phone': '404', 'email': '404', 'url': '404', 'revenue': '404', 'director': '404'}
        category_link_list.append(category_link)
    company_info['sbis'] = url
    df = df.append(company_info, ignore_index=True)
    time.sleep(random.randint(2, 5))
    print(company_info)

# Записываем результат в csv    
df.to_csv ('output.csv', index = False, sep='\t', header=True, encoding='utf-8-sig')