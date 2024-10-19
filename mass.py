import requests
from bs4 import BeautifulSoup
import csv


def scrape_massacres_table():
    url = "https://en.wikipedia.org/wiki/List_of_massacres_in_Nigeria"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="wikitable sortable")

    headers = [th.text.strip() for th in table.find("tr").find_all("th")]

    rows = table.find_all("tr")[1:]
    table_data = []
    for row in rows:
        cols = row.find_all("td")
        cols = [element.text.strip() for element in cols]
        table_data.append(cols)

    return headers, table_data


if __name__ == "__main__":
    headers, table_data = scrape_massacres_table()

    with open("massacres_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(table_data)

    print("Data saved to massacres_data.csv")
