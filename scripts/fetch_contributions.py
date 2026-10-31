
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import json
import re

BASE_DIR = Path(__file__).resolve().parent.parent

USERNAME = "shreya-goyal26"

url = f"https://github.com/users/{USERNAME}/contributions"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

contributions = []

# GitHub contribution days are table cells (td)
cells = soup.select("td.ContributionCalendar-day[data-date]")

for cell in cells:
    date = cell.get("data-date")
    level = cell.get("data-level")
    cell_id = cell.get("id")

    if not date or level is None:
        continue

    # Find the tooltip containing the exact contribution count
    tooltip = soup.find("tool-tip", attrs={"for": cell_id})

    count = None

    if tooltip:
        match = re.search(
            r"([\d,]+)\s+contributions?",
            tooltip.get_text(" ", strip=True),
            re.IGNORECASE
        )

        if match:
            count = int(match.group(1).replace(",", ""))

    if count is None and int(level) == 0:
        count = 0

    contributions.append({
        "date": date,
        "count": count,
        "level": int(level)
    })

if not contributions:
    print("No contribution days found.")
    print("HTTP status:", response.status_code)
    print("Page title:", soup.title.get_text(strip=True) if soup.title else "No title")
    print("HTML preview:", response.text[:500])
    raise ValueError("GitHub contribution data could not be parsed.")

output_path = BASE_DIR / "data" / "contributions.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(contributions, file, indent=4)

print(f"Fetched {len(contributions)} contribution days.")
print(f"Data saved to: {output_path}")
