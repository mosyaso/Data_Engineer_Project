from PIL import Image
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'c:\Users\syakir1937\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

img = Image.open('img1.jpg')
text =tess.image_to_string(img)
print(text)