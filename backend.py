from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
from text_preprocessing_module import apply_preprocessing
from charset_normalizer import from_bytes

app = Flask(__name__)
CORS(app)

# Define the path for the temp folder
TEMP_FOLDER = os.path.join(os.path.dirname(__file__), 'temp')
os.makedirs(TEMP_FOLDER, exist_ok=True)  # Create temp folder if it doesn't exist


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    temp_file_path = os.path.join(TEMP_FOLDER, file.filename)

    try:
        # Save the file to the temp folder
        file.save(temp_file_path)

        # Detect encoding
        with open(temp_file_path, 'rb') as f:
            raw_data = f.read()
            detected = from_bytes(raw_data).best()
            encoding = detected.encoding if detected else 'utf-8'

        # Load the CSV file using the detected encoding
        df = pd.read_csv(temp_file_path, encoding=encoding)

        preview = df.head(10).to_json(orient='records')
        return jsonify({"preview": preview, "columns": df.columns.tolist(), "file_path": temp_file_path})

    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500


@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    column = data.get('column')
    options = data.get('options', {})
    temp_file_path = data.get('file_path')  # Path of the uploaded temp file
    processed_file_path = os.path.join(TEMP_FOLDER, f"processed_{os.path.basename(temp_file_path)}")

    try:
        # Read the file from the temp folder
        with open(temp_file_path, 'rb') as f:
            raw_data = f.read()
            detected = from_bytes(raw_data).best()
            encoding = detected.encoding if detected else 'utf-8'

        df = pd.read_csv(temp_file_path, encoding=encoding)

        if column not in df.columns:
            return jsonify({"error": "Invalid column"}), 400

        # Apply preprocessing dynamically based on options
        df[f'Processed_{column}'] = df[column].apply(lambda x: apply_preprocessing(x, options))

        # Save the processed file to the temp folder
        df.to_csv(processed_file_path, index=False)

        # Return the path for download
        return jsonify({"preview": df.head(10).to_json(orient='records'), "download_url": "/download", "file_path": processed_file_path})
    except Exception as e:
        return jsonify({"error": f"Failed to process file: {str(e)}"}), 500


@app.route('/download', methods=['GET'])
def download_file():
    file_path = request.args.get('file_path')  # File path provided as a query parameter
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File path not provided or file does not exist"}), 400

    try:
        return send_file(file_path, mimetype='text/csv', as_attachment=True, download_name=os.path.basename(file_path))
    except Exception as e:
        return jsonify({"error": f"Failed to download file: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
