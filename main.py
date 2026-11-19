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

print("取得した件数 : ", len(repos))

for repo in repos:
    href = repo.get("href", "")
    name = repo.get_text(strip=True)

    if len(href.strip("/").split("/")) == 2 and name:
        print(name)