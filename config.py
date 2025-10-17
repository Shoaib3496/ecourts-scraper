"""Configuration for eCourts Scraper"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = True
    
    ECOURTS_BASE_URL = "https://services.ecourts.gov.in/ecourtindia_v6/"
    CAUSE_LIST_URL = "https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/"
    
    BROWSER_CONFIG = {
        'headless': False,
        'window_size': (1920, 1080),
        'timeout': 30,
        'implicit_wait': 10
    }
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DOWNLOADS_FOLDER = os.path.join(BASE_DIR, 'downloads')
    
    REQUEST_DELAY = 2
    MAX_RETRIES = 3
    
    CAPTCHA_CONFIG = {
        'retry_attempts': 3,
        'preprocessing': True
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    BROWSER_CONFIG = {'headless': True, 'window_size': (1920, 1080), 'timeout': 45}

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
