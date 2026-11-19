import requests
from bs4 import BeautifulSoup
import time
import sqlite3

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
        repository_data[parts[1]] = {
            "language": None,
            "stars": None
        }

    container = repo.parent.parent
    text = (container.get_text(" ", strip=True))

    for tag in container.find_all("span"):
        text = tag.get_text(strip=True)

        if text in ["C++", "Python", "Java", "Go", "JavaScript", "TypeScript", "Rust"]:
            repository_data[parts[1]] = {
                "language": text
            }
            print("主要言語:", text)
       

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

    print("\n--- ページ確認 ---")

    print("URL:", response.url)
    print("ステータス:", response.status_code)
    print("タイトル:", repo_soup.title.get_text(strip=True))

    print("\n--- Star関連のHTML ---")

    for tag in repo_soup.find_all(attrs={"aria-label": True}):
        value = tag.get("aria-label", "")
        if "star" in value.lower():
            print(value)
        
    print("\n--- Star関連の数字 ---")

    for tag in repo_soup.find_all(attrs={"aria-label": True}):
        value = tag.get("aria-label", "")

        if "star" in value.lower():
            print("aria-label:", value)

    for tag in repo_soup.find_all("a", href=True):
        if "stargazers" in tag["href"]:
            print("リンク:", tag.get_text(" ", strip=True))
            print("URL:", tag["href"])

    print("\n--- Strongタグの内容 ---")

    for tag in repo_soup.find_all("strong"):
        parent_text = tag.parent.get_text(" ", strip=True)

        if "stars" in parent_text:
            print(type(repository_data[name]), repository_data[name])
            repository_data[name]["stars"] = parent_text
            print("スター数:", parent_text)

conn = sqlite3.connect("github_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS repositories (
    name TEXT,
    language TEXT,
    stars TEXT
)
""")

for name, data in repository_data.items():
    cursor.execute(
        "INSERT INTO repositories (name, language, stars) VALUES (?, ?, ?)",
        (name, data["language"], data["stars"])
    )

conn.commit()

cursor.execute("SELECT * FROM repositories")
rows = cursor.fetchall()

print("保存したデータ:")
for row in rows:
    print(row)

conn.close()

print("データベースに保存しました")
