from flask import Flask, render_template, jsonify
from config.version import APP_VERSION
from scanner import scan_network, save_to_db
from init_db import init_db
import sqlite3

DB_NAME = 'scanner.db'

app = Flask(__name__)

# Inject the app version into all templates
@app.context_processor
def inject_version():
    return dict(app_version=APP_VERSION)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Scanner results page
@app.route('/scanner')
def scanner_view():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute('''
            SELECT name, type, ip, mac, vlan, location, status, scan_time
            FROM scanned_devices
            ORDER BY scan_time DESC
        ''')
        rows = cursor.fetchall()
    return render_template('scanner.html', results=rows)

# API endpoint to launch a scan
@app.route('/launch-scan')
def launch_scan():
    devices = scan_network()
    save_to_db(devices)
    return jsonify({"message": "Scan completed", "devices": len(devices)})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5001)
