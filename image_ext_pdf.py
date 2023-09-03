import fitz 
from wand.image import Image as WandImage
import os


pdf_path = 'EROLLGEN-S20-62-FinalRoll-Revision1-HIN-1-WI.pdf'

output_dir = 'output_image_pdf'
os.makedirs(output_dir, exist_ok=True)

# Open the PDF file
pdf_file = fitz.open(pdf_path)

# Iterate through each page of the PDF
for page_number in range(pdf_file.page_count):
    # Skip the first and last pages (page_number starts from 0)
    if page_number == 0 or page_number == pdf_file.page_count - 1:
        continue

    page = pdf_file[page_number]
    image_list = page.get_images(full=True)
    
    # Extract and enhance images on each page
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = pdf_file.extract_image(xref)
        image_data = base_image["image"]
        image_path = os.path.join(output_dir, f'page_{page_number + 1}_img_{img_index + 1}.png')
        
        # Save the extracted image to a file
        with open(image_path, 'wb') as f:
            f.write(image_data)
        
        # Enhance the saved image
        with WandImage(filename=image_path) as enhanced_img:
            enhanced_img.auto_orient()
            enhanced_img.sharpen(radius=2, sigma=1)  # Adjust radius and sigma for increased sharpening
            enhanced_img.contrast_stretch(black_point=0.07, white_point=0.1)  # Adjust black_point and white_point for increased contrast
            enhanced_img.save(filename=image_path)

print("Image extraction and enhancement completed.")
