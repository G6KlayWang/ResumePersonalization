import os
import fitz
from PIL import Image
import io
import pytesseract
import json


def extract_all_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]


        page_text = page.get_text("text")
        all_text += page_text + "\n"

        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image = Image.open(io.BytesIO(image_bytes))

            ocr_text = pytesseract.image_to_string(image)
            all_text += ocr_text + "\n"

    return all_text

def process_pdfs_in_folder(folder_path):
    input_json_folder = "data_set/input_json_folder"
    extracted_data = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            extracted_text = extract_all_text_from_pdf(pdf_path)


            extracted_data[filename] = extracted_text
            print(f"Processed {filename}")

    json_output_path = os.path.join(input_json_folder, "extracted_resumes.json")
    with open(json_output_path, "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)
    print(f"All text saved to {json_output_path}")

pdf_folder = "data_set/pdf_folder"
folder_path = pdf_folder
process_pdfs_in_folder(folder_path)