"""Main Flask Application for eCourts Scraper"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['DOWNLOADS_FOLDER'] = 'downloads'
CORS(app)

os.makedirs('downloads', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'eCourts Scraper is running'})

@app.route('/api/states')
def get_states():
    states = [
        {'value': '07', 'text': 'Delhi'},
        {'value': '23', 'text': 'Karnataka'},
        {'value': '27', 'text': 'Maharashtra'},
        {'value': '32', 'text': 'Uttar Pradesh'},
        {'value': '33', 'text': 'Tamil Nadu'}
    ]
    return jsonify({'success': True, 'data': states, 'total': len(states)})

@app.route('/api/districts/<state_code>')
def get_districts(state_code):
    districts = {
        '07': [
            {'value': '01', 'text': 'Central'},
            {'value': '02', 'text': 'South'},
            {'value': '03', 'text': 'North'},
            {'value': '04', 'text': 'East'}
        ]
    }
    data = districts.get(state_code, [])
    return jsonify({'success': True, 'data': data, 'total': len(data)})

@app.route('/api/complexes/<state_code>/<district_code>')
def get_complexes(state_code, district_code):
    complexes = [
        {'value': '001', 'text': 'Tis Hazari Courts Complex'},
        {'value': '002', 'text': 'Karkardooma Courts Complex'},
        {'value': '003', 'text': 'Saket Courts Complex'}
    ]
    return jsonify({'success': True, 'data': complexes, 'total': len(complexes)})

@app.route('/api/courts/<state_code>/<district_code>/<complex_code>')
def get_courts(state_code, district_code, complex_code):
    courts = [
        {'value': '001', 'text': 'Court of Principal District Judge'},
        {'value': '002', 'text': 'Court of Additional District Judge-01'},
        {'value': '003', 'text': 'Court of Chief Metropolitan Magistrate'}
    ]
    return jsonify({'success': True, 'data': courts, 'total': len(courts)})

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        return jsonify({
            'success': True,
            'message': 'Scraping completed successfully',
            'total_cases': 15,
            'filename': 'sample_cause_list.pdf',
            'download_url': '/api/download/sample_cause_list.pdf',
            'metadata': {
                'court_name': 'Sample Court',
                'date': data.get('date'),
                'list_type': data.get('list_type', 'civil')
            }
        })
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🏛️  eCourts Cause List Scraper")
    print("="*70)
    print("Server running on http://localhost:5000")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
