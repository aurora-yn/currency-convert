import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system('clear')
url_currency_codes= 'https://www.iban.com/currency-codes'

countries = []


def extract_countries(url):
  website = requests.get(url)
  soup = BeautifulSoup(website.text, 'html.parser')
  country_table = soup.find('table', {'class': 'table'})
  country_rows = country_table.find_all('tr')

  for row in country_rows[1:]:
    cols = row.find_all('td')

    if (cols[2].string != None) and (cols[3].string != None):
      country = {
        'name': cols[0].string.capitalize().replace('    ', ' '),
        'currency': cols[1].string,
        'code': cols[2].string,
        'number': int(cols[3].string)
      }
      countries.append(country)
    
  return countries
  
  
def select_country():
  while True:
    try:
      selected_num = int(input('# : '))
      if selected_num > largest_index:
        print(f'ERR > You can select a number from 0 to {largest_index}')
      else:
        selected_country = countries[selected_num]
        print(f'{selected_country["name"]}, the currency code is {selected_country["code"]}')
        return selected_num
        break
    except:
      print('ERR > You should type number only')


def type_amount(first_code, second_code):
  while True:
    try:
      amount = int(input(f'\nHow much {first_code} you would like to convert to {second_code} ? \n'))
      return amount
      break
    except:
      print('ERR > You should type number only')


def convert_currency():
  print('\nSelect a country by number')
  first_num = select_country()
  first_code = countries[first_num]['code']

  print('\nSelect another country you want to convert to using number')
  while True:
    second_num = select_country()
    if first_num != second_num:
      break
    else:
      print('ERR > You cannot select the same country')

  second_code = countries[second_num]['code']
  amount = type_amount(first_code, second_code)

  website = requests.get(f'https://transferwise.com/gb/currency-converter/{first_code}-to-{second_code}-rate?amount={amount}')
  soup = BeautifulSoup(website.text, 'html.parser')
  convert_box = soup.find('input', {'id': 'cc-amount-to'})
  converted_amount = convert_box['value']

  print('\n'+format_currency(amount, first_code, locale="ko_KR")+' is '+format_currency(converted_amount, second_code, locale="ko_KR"))


print('Welcome to the currency converter!')
countries = extract_countries(url_currency_codes)

for i, country in enumerate(countries):
  print(f'# {i} {country["name"]}')

largest_index = len(countries) - 1
convert_currency()
