import requests
import re

USERNAME = "AshuMLTech"   # your GitHub username
README_FILE = "README.md"

# keywords to filter repos
FILTER_KEYWORDS = ["ml", "machine", "data", "ai", "project"]

def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=50"
    response = requests.get(url)
    repos = response.json()
    filtered = []
    for repo in repos:
        if repo["fork"]:
            continue
        description = (repo["description"] or "").lower()
        if any(keyword in description for keyword in FILTER_KEYWORDS):
            filtered.append(f"- [{repo['name']}]({repo['html_url']}) ⭐ {repo['stargazers_count']}")
    return filtered[:5]  # show only latest 5

def update_readme(repos):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    new_projects = "\n".join(repos) if repos else "No recent ML/Data projects."
    updated_content = re.sub(
        r"<!-- PROJECTS:START -->(.*?)<!-- PROJECTS:END -->",
        f"<!-- PROJECTS:START -->\n{new_projects}\n<!-- PROJECTS:END -->",
        content,
        flags=re.DOTALL
    )

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    repos = fetch_repos(USERNAME)
    update_readme(repos)
