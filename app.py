from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from scraper.ecourts_scraper import ECourtsScraper
import os, logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scraper = ECourtsScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/states', methods=['GET'])
def get_states():
    try:
        states = scraper.get_states()
        return jsonify({'success': True, 'data': states, 'total': len(states)})
    except Exception as e:
        logger.exception("Failed to get states")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/districts/<state_code>', methods=['GET'])
def get_districts(state_code):
    try:
        districts = scraper.get_districts(state_code)
        return jsonify({'success': True, 'data': districts, 'total': len(districts)})
    except Exception as e:
        logger.exception("Failed to get districts")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/complexes/<state_code>/<district_code>', methods=['GET'])
def get_complexes(state_code, district_code):
    try:
        complexes = scraper.get_court_complexes(state_code, district_code)
        return jsonify({'success': True, 'data': complexes, 'total': len(complexes)})
    except Exception as e:
        logger.exception("Failed to get complexes")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/courts/<state_code>/<district_code>/<complex_code>', methods=['GET'])
def get_courts(state_code, district_code, complex_code):
    try:
        courts = scraper.get_courts(state_code, district_code, complex_code)
        return jsonify({'success': True, 'data': courts, 'total': len(courts)})
    except Exception as e:
        logger.exception("Failed to get courts")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/scrape', methods=['POST'])
def scrape_cause_list():
    data = request.get_json()
    required = ['state', 'district', 'complex', 'court', 'date', 'listType']
    for r in required:
        if not data.get(r):
            return jsonify({'success': False, 'error': f'Missing field {r}'}), 400
    try:
        result = scraper.scrape_cause_list(
            state=data['state'],
            district=data['district'],
            complex=data['complex'],
            court=data['court'],
            date=data['date'],
            list_type=data['listType']
        )
        if result.get('success'):
            filename = os.path.basename(result['pdf_path'])
            return jsonify({'success': True, 'filename': filename, 'message': 'Cause list scraped successfully'})
        else:
            return jsonify({'success': False, 'error': result.get('error', 'Unknown')}), 500
    except Exception as e:
        logger.exception("Scrape failed")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join('downloads', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    app.run(debug=True, host='127.0.0.1', port=5000)
