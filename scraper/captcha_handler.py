from PIL import Image
import pytesseract, io, traceback
from selenium.webdriver.common.by import By

class CaptchaHandler:
    def __init__(self):
        pass

    def solve_captcha(self, driver):
        try:
            img_el = driver.find_element(By.ID, "captcha_image")
            png = img_el.screenshot_as_png
            img = Image.open(io.BytesIO(png)).convert('L')
            img = img.point(lambda p: 255 if p > 160 else 0)
            text = pytesseract.image_to_string(img, config='--psm 7')
            text = ''.join(filter(str.isalnum, text)).strip()
            return text
        except Exception as e:
            print("Captcha auto-solve failed:", e)
            traceback.print_exc()
            return ""
