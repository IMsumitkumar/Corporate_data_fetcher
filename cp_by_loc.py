import csv
import requests
from bs4 import BeautifulSoup

def fetch_data(url: str, loc:str, start_page_no:int, end_page_no: int):
    try:
        with open('./dataByLocation/cpdata-{loc}-{start}-{end}.csv'.format(loc=loc,start=start_page_no, end=end_page_no),
                  'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["CIN", "Name", "roc", "status"])

            if start_page_no < 1:
                start_page_no = 1
            else:
                start_page_no = start_page_no

            for i in range(start_page_no, end_page_no+1):
                print(f"[page - {i}] Done")
                all_data = []
                furl = url.format(location=loc)+"p-{page_no}-company.html".format(page_no=str(i))
                
                soup = BeautifulSoup(requests.get(furl).content, 'html.parser')

                table = soup.find("table", id="table")

                if table is not None:
                    rows = table.findAll('td')
                    [all_data.append(i.text.strip().replace("'"," ")) for i in rows]

                    i=0
                    data_rows =[]
                    while i<len(all_data):
                        data_rows.append(all_data[i:i+4])
                        i+=4
                    
                    csv_writer.writerows(data_rows)
                else:
                    data_rows.append([['None', 'None', 'None', 'None']])
    except Exception as e:
        print(e)
        
    # return data_rows


if __name__ == '__main__':
    url = 'https://www.zaubacorp.com/company-list/city-{location}/'
    location = str(input("Enter Company Name:")).replace(' ', '-').upper()
    start_index = int(input("starting page number from where you wanna fetch:"))
    end_index = int(input("ending page number:"))
    fetch_data(url=url, loc=location, start_page_no=start_index, end_page_no=end_index)
