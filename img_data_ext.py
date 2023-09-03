import os
from google.cloud import vision_v1p3beta1 as vision
from google.oauth2 import service_account

# Set your Google Cloud credentials (replace 'YOUR_KEY_FILE.json' with your actual service account key file)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp.json'

# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

def extract_text_from_image(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Perform text detection on the image
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    # Extract the text annotations
    text_annotations = response.text_annotations

    if text_annotations:
        detected_text = text_annotations[0].description
        return detected_text
    else:
        return None

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == "__main__":
    image_folder = "output_image_pdf"  # folder containing your images
    output_folder = "output_text"  # Output folder named "output_text"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            extracted_text = extract_text_from_image(image_path)

            if extracted_text:
                output_file = os.path.join(output_folder, filename.replace(".", "_") + ".txt")
                save_text_to_file(extracted_text, output_file)
                print(f"Extracted text saved to {output_file}")
            else:
                print(f"No text detected in {image_path}")
