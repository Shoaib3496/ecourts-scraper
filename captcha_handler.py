from PIL import Image
import pytesseract
import io
import base64
from selenium.webdriver.common.by import By
import time

class CaptchaHandler:
    def __init__(self):
        # Configure Tesseract if needed
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def solve_captcha(self, driver):
        """Attempt to solve CAPTCHA automatically"""
        try:
            # Find CAPTCHA image
            captcha_img = driver.find_element(By.ID, "captcha_image")
            
            # Get image as base64
            img_data = captcha_img.screenshot_as_png
            img = Image.open(io.BytesIO(img_data))
            
            # Preprocess image for better OCR
            img = self.preprocess_image(img)
            
            # Use Tesseract to extract text
            captcha_text = pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            
            # Clean extracted text
            captcha_text = captcha_text.strip().replace(' ', '').upper()
            
            # Validate length (eCourts uses 5-character CAPTCHA)
            if len(captcha_text) == 5:
                return captcha_text
            else:
                # Fallback: manual input or retry
                return self.manual_captcha_input()
                
        except Exception as e:
            print(f"CAPTCHA solving failed: {e}")
            return self.manual_captcha_input()
    
    def preprocess_image(self, img):
        """Preprocess CAPTCHA image for better OCR accuracy"""
        # Convert to grayscale
        img = img.convert('L')
        
        # Apply threshold to make black and white
        threshold = 128
        img = img.point(lambda p: p > threshold and 255)
        
        # Resize for better recognition
        width, height = img.size
        img = img.resize((width * 3, height * 3), Image.LANCZOS)
        
        return img
    
    def manual_captcha_input(self):
        """Fallback for manual CAPTCHA input"""
        # In production, this could display CAPTCHA to user
        # For testing, return a placeholder or implement web interface
        print("CAPTCHA requires manual solving")
        return input("Enter CAPTCHA text: ")
