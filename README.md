ecourts-scraper
Real-time eCourts India cause list scraper with PDF generation

🌟Features:
-> Fetches live cause lists from Indian District Courts via the eCourts portal
-> Cascading UI: State → District → Court Complex → Court
-> Real-time updates, progress tracking, status indicators
-> Bulk mode: Scrape all courts in a selected complex
-> Generates professional, ready-to-download PDF reports
-> Automated CAPTCHA handling with fallback
-> Modern Bootstrap 5 responsive frontend
-> Easy to extend, modular backend (Flask, Selenium, Tesseract OCR, ReportLab)

🚀 Quick Start:
git clone https://github.com/yourusername/ecourts-scraper.git
cd ecourts-scraper
python -m venv venv
# macos: source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

Visit http://localhost:5000 in your browser.

🎥 Live Demo
See the full demo interface here:
https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/bb75bcacc1d01d879dfeedcd5b7b0fba/95ca3b5c-1003-4e02-b667-3d5af6ee27de/index.html

Project Structure:
ecourts_scraper/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── requirements.txt          # Dependencies
├── run.py                    # Easy launcher script
├── README.md                 # Comprehensive documentation
├── scraper/
│   ├── ecourts_scraper.py   # Core scraping logic
│   ├── captcha_handler.py   # CAPTCHA automation
│   └── pdf_generator.py     # Professional PDFs
├── static/
│   ├── css/style.css        # Custom styling
│   └── js/main.js           # Frontend functionality
├── templates/
│   └── index.html           # Modern web interface
├── utils/helpers.py         # Utility functions
└── tests/test_scraper.py    # Unit tests
