import requests
from bs4 import BeautifulSoup
import time

url = "https://github.com/orgs/google/repositories"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

time.sleep(1)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title.get_text())

repos = soup.select('a[href^="/google/"]')

repository_data = {}

for repo in repos:
    href = repo.get("href", "")
    name = repo.get_text(strip=True)

    parts =href.strip("/").split("/")

    if len(parts) == 2 and name:
        repository_data[parts[1]] = parts[1]

print("リポジトリ数 : ", len(repository_data))

for name in repository_data:
    print(name)