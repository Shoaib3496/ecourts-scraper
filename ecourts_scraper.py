from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
from .captcha_handler import CaptchaHandler
from .pdf_generator import PDFGenerator

class ECourtsScraper:
    def __init__(self):
        self.base_url = "https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/"
        self.driver = None
        self.captcha_handler = CaptchaHandler()
        self.pdf_generator = PDFGenerator()
        
    def setup_driver(self, headless=True):
        """Initialize Chrome WebDriver with optimal settings"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)
    
    def get_states(self):
        """Fetch all available states"""
        if not self.driver:
            self.setup_driver()
            
        self.driver.get(self.base_url)
        state_select = Select(self.driver.find_element(By.ID, "state"))
        
        states = []
        for option in state_select.options[1:]:  # Skip first empty option
            states.append({
                'value': option.get_attribute('value'),
                'text': option.text
            })
        return states
    
    def get_districts(self, state_code):
        """Fetch districts for a given state"""
        state_select = Select(self.driver.find_element(By.ID, "state"))
        state_select.select_by_value(state_code)
        
        # Wait for districts to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "district"))
        )
        
        district_select = Select(self.driver.find_element(By.ID, "district"))
        districts = []
        for option in district_select.options[1:]:
            districts.append({
                'value': option.get_attribute('value'),
                'text': option.text
            })
        return districts
    
    def get_court_complexes(self, district_code):
        """Fetch court complexes for a given district"""
        district_select = Select(self.driver.find_element(By.ID, "district"))
        district_select.select_by_value(district_code)
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "court_complex"))
        )
        
        complex_select = Select(self.driver.find_element(By.ID, "court_complex"))
        complexes = []
        for option in complex_select.options[1:]:
            complexes.append({
                'value': option.get_attribute('value'),
                'text': option.text
            })
        return complexes
    
    def get_courts(self, complex_code):
        """Fetch individual courts for a given complex"""
        complex_select = Select(self.driver.find_element(By.ID, "court_complex"))
        complex_select.select_by_value(complex_code)
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "court"))
        )
        
        court_select = Select(self.driver.find_element(By.ID, "court"))
        courts = []
        for option in court_select.options[1:]:
            courts.append({
                'value': option.get_attribute('value'),
                'text': option.text
            })
        return courts
    
    def scrape_cause_list(self, state, district, complex, court, date, list_type="civil"):
        """Main method to scrape cause list"""
        try:
            # Navigate and fill form
            self.get_states()
            self.get_districts(state)
            self.get_court_complexes(district)
            self.get_courts(complex)
            
            # Select specific court
            court_select = Select(self.driver.find_element(By.ID, "court"))
            court_select.select_by_value(court)
            
            # Set date
            date_field = self.driver.find_element(By.ID, "date")
            self.driver.execute_script(f"arguments[0].value = '{date}';", date_field)
            
            # Handle CAPTCHA
            captcha_text = self.captcha_handler.solve_captcha(self.driver)
            captcha_input = self.driver.find_element(By.ID, "captcha")
            captcha_input.send_keys(captcha_text)
            
            # Submit form
            if list_type.lower() == "civil":
                submit_btn = self.driver.find_element(By.ID, "civil_submit")
            else:
                submit_btn = self.driver.find_element(By.ID, "criminal_submit")
            
            submit_btn.click()
            
            # Wait for results
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cause-list-table"))
            )
            
            # Extract cause list data
            html_content = self.driver.page_source
            cause_list_data = self.extract_cause_list_data(html_content)
            
            # Generate PDF
            pdf_path = self.pdf_generator.create_pdf(cause_list_data, {
                'state': state,
                'district': district, 
                'complex': complex,
                'court': court,
                'date': date,
                'type': list_type
            })
            
            return {
                'success': True,
                'pdf_path': pdf_path,
                'data': cause_list_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_cause_list_data(self, html_content):
        """Extract structured data from cause list HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the cause list table
        table = soup.find('table', class_='cause-list-table')
        if not table:
            return []
        
        cases = []
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 5:  # Ensure minimum columns
                case = {
                    'sr_no': cells[0].get_text(strip=True),
                    'case_no': cells[1].get_text(strip=True),
                    'petitioner': cells[2].get_text(strip=True),
                    'respondent': cells[3].get_text(strip=True),
                    'purpose': cells[4].get_text(strip=True)
                }
                cases.append(case)
        
        return cases
    
    def cleanup(self):
        """Close browser and cleanup resources"""
        if self.driver:
            self.driver.quit()
