
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import html

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "assets" / "profile.png"
output_path = BASE_DIR / "data" / "ascii-portrait.svg"

CHARS = "@%#*+=-:. "
WIDTH = 160
FONT_SIZE = 7

image = Image.open(input_path).convert("RGB")

# Crop around the face and upper body
w, h = image.size
image = image.crop((
    int(w * 0.12),
    int(h * 0.02),
    int(w * 0.84),
    int(h * 0.90)
))

# Convert to grayscale and improve details
image = ImageOps.grayscale(image)
image = ImageOps.autocontrast(image, cutoff=1)
image = ImageEnhance.Contrast(image).enhance(1.3)

# Preserve proportions while accounting for character shape
height = max(1, int(image.height / image.width * WIDTH * 0.60))

image = image.resize(
    (WIDTH, height),
    Image.Resampling.LANCZOS
)

pixels = image.load()
rows = []

for y in range(height):
    row = ""

    for x in range(WIDTH):
        brightness = pixels[x, y]
        index = (255 - brightness) * (len(CHARS) - 1) // 255
        row += CHARS[index]

    rows.append(row)

svg_rows = []

for y, row in enumerate(rows):
    svg_rows.append(
        f'<text x="0" y="{(y + 1) * FONT_SIZE}" '
        f'class="line" style="animation-delay:{y * 0.035}s">'
        f'{html.escape(row)}</text>'
    )

svg_width = WIDTH * FONT_SIZE * 0.62
svg_height = height * FONT_SIZE * 1.3

svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}" height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">

<style>
.line {{
    font-family: monospace;
    font-size: {FONT_SIZE}px;
    white-space: pre;
    fill: #ffffff;
    opacity: 0;
    animation: appear 0.5s forwards;
}}

@keyframes appear {{
    to {{ opacity: 1; }}
}}
</style>

<rect width="100%" height="100%" fill="#0d1117"/>
{''.join(svg_rows)}
</svg>"""

output_path.write_text(svg, encoding="utf-8")

print(f"ASCII portrait created: {output_path}")
