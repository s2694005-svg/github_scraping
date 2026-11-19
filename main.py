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

print("\n--- 詳細情報 ---")

for name in repository_data:

    repo_url = f"https://github.com/google/{name}"

    response = requests.get(
        repo_url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    time.sleep(1)

    repo_soup = BeautifulSoup(response.text, "html.parser")

    print("リポジトリ名:", name)
    print("アクセス結果:", response.status_code)
    print("ページタイトル:", repo_soup.title.get_text(strip=True))

    print("\n--- 言語情報 ---")

    for tag in repo_soup.find_all("span"):
        if tag.get("class") and "Progress-item" in tag.get("class"):
            print("クラス:", tag.get("class"))
            print("文字:", tag.get_text(strip=True))

    print("\n--- Star情報 ---")

    print("stargazersがHTMLにあるか:",
          "starrazers" in response.text)

    print("starsがHTMLにあるか:",
          "stars" in response.text.lower())