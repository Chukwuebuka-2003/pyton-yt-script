import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://en.wikipedia.org/wiki/List_of_massacres_in_Nigeria"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the "Political violence" table
table = soup.find("table", class_="wikitable")

# Extract data from the table
rows = table.find_all("tr")
data = []
for row in rows:
    # Extract data from each row
    cells = row.find_all(["th", "td"])
    row_data = [cell.get_text(strip=True) for cell in cells]
    if row_data:  # Check if row_data is not empty
        data.append(row_data)

# Convert the data into a DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Save the DataFrame to a CSV file
df.to_csv("political_violence_nigeria.csv", index=False)

# Display the DataFrame
print(df)
