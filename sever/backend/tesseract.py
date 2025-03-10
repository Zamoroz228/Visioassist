import cv2
import numpy as np
import os
import pytesseract

class TesseractOCRProcessor:
    def __init__(self, lang='rus+eng', tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        self.lang = lang
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def recognize_text(self, image_path):
        try:
            if not os.path.exists(image_path):
                return "Файл не найден"
            image = cv2.imread(image_path)
            if image is None:
                return "Не удалось прочитать изображение"
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
            config = '--oem 1 --psm 3'
            text = pytesseract.image_to_string(
                binary,
                lang=self.lang,
                config=config
            )
            
            return text
            
        except Exception as e:
            return f"Ошибка распознавания: {str(e)}"