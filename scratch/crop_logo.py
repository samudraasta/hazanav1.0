from PIL import Image
import os

filepath = 'logos_standard/LAZ Generasi Rabbani.png'

if os.path.exists(filepath):
    # Open the image
    img = Image.open(filepath)
    
    # Ensure it's in RGBA mode to check transparency
    img = img.convert("RGBA")
    
    # Get the bounding box of the non-transparent alpha channel
    bbox = img.getbbox()
    
    if bbox:
        # Crop the image to the bounding box
        cropped = img.crop(bbox)
        # Save it back (overwrite)
        cropped.save(filepath, "PNG")
        print(f"Successfully cropped {filepath}.")
    else:
        print("Image is entirely transparent, cannot crop.")
else:
    print("File not found.")
