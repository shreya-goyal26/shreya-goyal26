from pathlib import Path
from datetime import date
import json
import html

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "data" / "contributions.json"
output_path = BASE_DIR / "data" / "contribution-heatmap.svg"

with open(input_path, "r", encoding="utf-8") as file:
    contributions = json.load(file)

colors = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353"
]

cell_size = 12
gap = 3
start_x = 45
start_y = 35

data = {
    item["date"]: item["level"]
    for item in contributions
}

dates = sorted(data.keys())

if not dates:
    raise ValueError("No contribution data found.")

first_day = date.fromisoformat(dates[0])
start_date = date.fromordinal(first_day.toordinal() - first_day.weekday())

rectangles = []

for day, level in data.items():
    current = date.fromisoformat(day)
    week = (current - start_date).days // 7
    weekday = current.weekday()

    x = start_x + week * (cell_size + gap)
    y = start_y + weekday * (cell_size + gap)

    level = max(0, min(4, int(level)))
    color = colors[level]

    rectangles.append(
        f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
        f'rx="3" fill="{color}">'
        f'<title>{html.escape(day)}: {level} contribution level</title>'
        f'</rect>'
    )

weeks = ((date.fromisoformat(dates[-1]) - start_date).days // 7) + 1

width = start_x * 2 + weeks * (cell_size + gap)
height = start_y * 2 + 7 * (cell_size + gap)

svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}" height="{height}"
     viewBox="0 0 {width} {height}">
    <rect width="100%" height="100%" fill="#0d1117"/>
    <g font-family="Arial" font-size="10" fill="#8b949e">
        <text x="5" y="{start_y + 10}">Mon</text>
        <text x="5" y="{start_y + 40}">Wed</text>
        <text x="5" y="{start_y + 70}">Fri</text>
    </g>
    {''.join(rectangles)}
</svg>
"""

output_path.write_text(svg, encoding="utf-8")

print(f"Heatmap created: {output_path}")