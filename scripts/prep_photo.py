
from pathlib import Path
from PIL import Image
from rembg import remove
import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "assets" / "profile.png"
output_path = BASE_DIR / "data" / "source-prepped.png"

if not input_path.exists():
    raise FileNotFoundError(f"Photo not found: {input_path}")

# Open the original photo
image = Image.open(input_path).convert("RGBA")

# Remove the background
image = remove(image)

# Create a white background
background = Image.new("RGBA", image.size, (255, 255, 255, 255))
background.alpha_composite(image)

# Convert to grayscale
image = background.convert("RGB")
image_array = np.array(image)
gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

# Improve image contrast
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
processed = clahe.apply(gray)

# Save the processed image
Image.fromarray(processed).save(output_path)

print(f"Photo processed successfully: {output_path}")
