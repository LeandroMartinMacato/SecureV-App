import cv2
import os
import pytesseract as tess
from PIL import Image


tess.pytesseract.tesseract_cmd = r"E:\Programming_Files\Tesseract-OCR\tesseract.exe"
# tess.pytesseract.tesseract_cmd = r"E:\Programming_Files\Tesseract-OCR\pytesseract.exe"


img = Image.open(r"E:\Main\Pictures\test_ocr.png")

text = tess.image_to_string(img)
# text = tess.image_to_string(img, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')


print(text)

