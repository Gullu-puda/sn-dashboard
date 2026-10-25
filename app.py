from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def serve_index():
    # Explicitly serve index.html from the absolute directory of app.py
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api/data', methods=['GET'])
def get_excel_data():
    try:
        sheet_name = request.args.get('sheet', 'Customer')
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'Status.xlsx')
        
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Sabhi datetime columns ko string me convert kar dena taaki JSON error (NaT) na aaye
        for col in df.select_dtypes(include=['datetime64', 'datetimetz']).columns:
            df[col] = df[col].dt.strftime('%Y-%m-%d')
            
        # Bachi hui khali (NaN/NaT) values ko blank string banayein
        df = df.fillna('')
        df = df.replace({pd.NaT: ''})
        
        # Data ko JSON format mein return karein
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("API is running! Dashboard will now fetch data dynamically.")
    app.run(host='0.0.0.0', port=5000, debug=True)