import PyPDF2
import pandas as pd
from PIL import Image
import pytesseract
from pptx import Presentation
import json

def parse_file(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif file_type in ["txt", "py"]:
        return uploaded_file.read().decode("utf-8")

    elif file_type in ["csv"]:
        df = pd.read_csv(uploaded_file)
        return df.to_string()

    elif file_type in ["xlsx"]:
        df = pd.read_excel(uploaded_file)
        return df.to_string()

    elif file_type in ["json"]:
        data = json.load(uploaded_file)
        return json.dumps(data, indent=2)

    elif file_type in ["pptx"]:
        prs = Presentation(uploaded_file)
        text = ""
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text

    elif file_type in ["jpg", "jpeg", "png"]:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)
        return text

    else:
        return "Unsupported file type"