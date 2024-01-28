import requests
import csv
import re

from bs4 import BeautifulSoup as bs4


def get_filename(p):
    regex = r"(art\. \d+[a-z]*)"

    groups = re.findall(regex, p.text);

    filename = p.text[0:52]

    for i in groups:
        filename += "_"
        filename += i
    return filename

def get_table_header(table):
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text)
    return headers


def format_table(table):
    result = []

    for row in table.find_all('tr'):
        row_data = []
        for td in table.find_all('td'):
            row_data.append(td.text)
        result.append(row_data)

    return result


def export_to_csv(filename, headers, data):
    with open(f'D:\Zadania\web-scrapper\{filename}.csv', 'w', encoding='UTF16', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(headers)

        print(data)
        for row in data:
            writer.writerow(row)


def format_data(filename, table):
    headers = get_table_header(table)
    data = format_table(table)

    export_to_csv(filename, headers, data)


if __name__ == '__main__':
    page_url = 'https://www.knf.gov.pl/dla_konsumenta/ostrzezenia_publiczne'
    page = requests.get(page_url)

    soup = bs4(page.content, 'html.parser', from_encoding='utf-16')

    for i in soup.find_all('div', {"class": "table-with-header-parent"}):
        filename = get_filename(i.find('p', {"class", "text-sm font-semibold text-white text-center max-w-[872px]"}))
        format_data(filename, i.find('table'))

