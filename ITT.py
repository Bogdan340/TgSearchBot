import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

print(fr'{Path(__file__).resolve().parent}\Tesseract-OCR\tesseract.exe')
def itt(path): # image to text
    pytesseract.pytesseract.tesseract_cmd = fr'{Path(__file__).resolve().parent}\Tesseract-OCR\tesseract.exe'
    image = cv2.imread(path)
    string = pytesseract.image_to_string(image, lang="rus")
    return string.replace("\n", "")