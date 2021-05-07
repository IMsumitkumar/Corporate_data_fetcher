import csv
import requests
from bs4 import BeautifulSoup

def fetch_data(url):
    all_data = []
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    table = soup.find("table", id="results")

    if table is not None:
        rows = table.findAll('td')
        [all_data.append(i.text.strip().replace("'"," ")) for i in rows]

        # we should limit all data records
        # as it is fetching all pagination data 
        i=0
        data_rows =[]
        while i<len(all_data):
            data_rows.append(all_data[i:i+3])
            i+=3

        return data_rows
    else:
        return [['None', 'None', 'None']]


if __name__ == '__main__':
    url = 'https://www.zaubacorp.com/companysearchresults/{comp_name}'
    company_name = str(input("Enter Company Name:")).replace(' ', '-')
    data_rows = fetch_data(url.format(comp_name=company_name))

    with open('data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["CIN", "Name", "address"])
        csv_writer.writerows(data_rows)


