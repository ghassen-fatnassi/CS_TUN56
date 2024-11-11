import uuid
import threading
import zipfile
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import magic
import hashlib
import requests
import os
import time
import tensorflow as tf

app = Flask(__name__)
CORS(app)

dug_i = 1


def debug():
    global dug_i
    print('stage', dug_i)
    dug_i += 1


model = tf.keras.models.load_model('malware_model_checkpoints.h5.keras')
malware_classes = ["Adialer.C", "Agent.FYI", "Allaple.A", "Allaple.L Alueron.gen!J", "Autorun.K", "C2LOP.P",
                   "C2LOP.gen!g Dialplatform.B", "Dontovo.A", "Fakerean", "Instantaccess", "Lolyda.AA1",
                   "Lolyda.AA2", "Lolyda.AA3", "Lolyda.AT", "Malex.gen!J", "Obfuscator.AD", "Rbot!gen",
                   "Skintrim.N", "Swizzor.gen!E", "Swizzor.gen!I", "VB.AT", "Wintrim.BX", "Yuner.A"]

API_KEY = "2db7f201703404731e94721a388ee1106d04ab9a248a534c4aa65ee31fa92991"


def binary_to_image(binary_data):
    """Convert binary data to a 256x256 RGB image."""
    # Convert binary to hex array
    hex_array = [byte for byte in binary_data]

    # Create 2D array with 16 columns, padding the last row if necessary
    array = []
    for i in range(0, len(hex_array), 16):
        row = hex_array[i:i + 16]
        if len(row) < 16:
            row.extend([0] * (16 - len(row)))  # Pad row to length 16
        array.append(row)

    # Convert to numpy array
    array = np.array(array, dtype=np.uint8)

    # Calculate dimensions for a square image
    b = int((array.shape[0] * 16) ** 0.5)
    b = 2 ** (int(np.log2(b)) + 1)
    a = int(array.shape[0] * 16 / b)

    # Reshape array to square dimensions
    array = array[:a * b // 16, :]
    array = np.reshape(array, (a, b))

    # Convert to PIL Image and resize to 256x256
    im = Image.fromarray(array).convert("L")
    im = im.resize((256, 256), Image.LANCZOS)

    # Convert to RGB (3 channels)
    im = im.convert("RGB")

    return im


def virus_total_analyze_file(file_path):
    url = 'https://www.virustotal.com/api/v3/files'
    headers = {
        'x-apikey': API_KEY,
        "accept": "application/json",
    }

    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file)}
        print(files)
        response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        json_response = response.json()
        analysis_id = json_response.get("data", {}).get("id")
        return analysis_id
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def check_virus_total_analysis(analysis_id, max_retries=10, wait_time=3):
    """Checks the analysis status on VirusTotal and returns the result if complete."""
    url = f'https://www.virustotal.com/api/v3/analyses/{analysis_id}'
    headers = {
        'x-apikey': API_KEY,
        "accept": "application/json",
        "content-type": "multipart/form-data"
    }

    for _ in range(max_retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            json_response = response.json()
            status = json_response.get("data", {}).get("attributes", {}).get("status")
            print(status)

            if status == "completed":
                print(f"niggas type : {json_response}")
                return json_response

            time.sleep(wait_time)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    return None


def get_number_of_malicious_detections(analysis_id):
    url = f'https://www.virustotal.com/api/v3/analyses/{analysis_id}'
    headers = {
        'x-apikey': API_KEY,
        "accept": "application/json",
        "content-type": "multipart/form-data"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        print(json_response.get('data', {}).get('attributes', {}).get('stats', {}))
        return json_response.get('data', {}).get('attributes', {}).get('stats', {}).get('malicious', 0)

    else:
        return 0


def calculate_hashes(file_path):
    """Calculate various hashes of the file."""
    with open(file_path, 'rb') as f:
        content = f.read()

    return {
        'md5': hashlib.md5(content).hexdigest(),
        'sha1': hashlib.sha1(content).hexdigest(),
        'sha256': hashlib.sha256(content).hexdigest(),
    }


# @app.route('/analyze_ai', methods=['POST'])
# def analyse_with_ai():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
#
#     file = request.files['file']
#     if not file.filename.endswith('.exe'):
#         return jsonify({'error': 'Invalid file type'}), 400
#
#     random_filename = f"{uuid.uuid4()}.exe"
#     temp_path = os.path.join('temp_files', random_filename)
#
#     os.makedirs(os.path.dirname(temp_path), exist_ok=True)
#
#     file.save(temp_path)
#
#     # Process the binary data as an image for AI analysis
#     with open(temp_path, 'rb') as f:
#         binary_data = f.read()
#
#     # Submit file for VirusTotal analysis and get an analysis ID
#     analysis_id = virus_total_analyze_file(temp_path)
#     if not analysis_id:
#         return jsonify({'error': 'Failed to submit file to VirusTotal'}), 500
#
#     try:
#         img = binary_to_image(binary_data)
#     except Exception as e:
#         return jsonify({'error': f'Failed to convert file to image: {str(e)}'}), 500
#
#     img_array = np.array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array = img_array / 255.0
#
#     predictions = model.predict(img_array)
#     predicted_class_idx = np.argmax(predictions[0])
#     predicted_class = "class " + str(predicted_class_idx)
#     confidence = float(predictions[0][predicted_class_idx])
#     print(predicted_class)
#     try:
#         file_info = {
#             'file_name': file.filename,
#             'file_size': os.path.getsize(temp_path),
#             'file_type': magic.from_file(temp_path),
#             'mime_type': magic.from_file(temp_path, mime=True)
#         }
#
#         hashes = calculate_hashes(temp_path)
#
#         results = {
#             'file_info': file_info,
#             'hashes': hashes,
#             'model_analysis': f"class:{predicted_class}, confidence: {confidence}",
#             'virus_total_analysis_id': analysis_id,
#         }
#
#         print(results)
#         return jsonify(results)
#
#     except Exception as e:
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
#         return jsonify({'error': str(e)}), 500
#
#     finally:
#         analysis_result: dict = poll_virus_total_status(analysis_id)
#
#         if analysis_result:
#             malicious_count = get_number_of_malicious_detections(analysis_id)
#             print(malicious_count)
#             if malicious_count == 0:
#                 if os.path.exists(temp_path):
#                     os.remove(temp_path)
#             else:
#                 malware_folder = 'malwares_folder'
#
#                 os.makedirs(malware_folder, exist_ok=True)
#                 zip_path = os.path.join(malware_folder, f"{os.path.basename(temp_path)}.zip")
#
#                 with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
#                     zipf.write(temp_path, arcname=os.path.basename(temp_path))
#
#                 print(f"Malicious file saved and zipped at {zip_path}")
#

def handle_virus_total_analysis(temp_path, analysis_id):
    analysis_result = poll_virus_total_status(analysis_id)
    if analysis_result:
        malicious_count = get_number_of_malicious_detections(analysis_id)
        if malicious_count == 0:
            # If not malicious, delete the file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        else:
            # If malicious, save to 'malwares_folder' and zip the file
            malware_folder = 'malwares_folder'
            os.makedirs(malware_folder, exist_ok=True)
            zip_path = os.path.join(malware_folder, f"{os.path.basename(temp_path)}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_path, arcname=os.path.basename(temp_path))
            print(f"Malicious file saved and zipped at {zip_path}")


@app.route('/analyze_ai', methods=['POST'])
def analyse_with_ai():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file.filename.endswith('.exe'):
        return jsonify({'error': 'Invalid file type'}), 400

    random_filename = f"{uuid.uuid4()}.exe"
    temp_path = os.path.join('temp_files', random_filename)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    file.save(temp_path)

    # Process the binary data as an image for AI analysis
    with open(temp_path, 'rb') as f:
        binary_data = f.read()

    try:
        img = binary_to_image(binary_data)
    except Exception as e:
        return jsonify({'error': f'Failed to convert file to image: {str(e)}'}), 500

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    predictions = model.predict(img_array)
    predicted_class_idx = np.argmax(predictions[0])
    predicted_class = malware_classes[predicted_class_idx]
    confidence = float(predictions[0][predicted_class_idx])

    try:
        file_info = {
            'file_name': file.filename,
            'file_size': os.path.getsize(temp_path),
            'file_type': magic.from_file(temp_path),
            'mime_type': magic.from_file(temp_path, mime=True)
        }
        hashes = calculate_hashes(temp_path)
        analysis_id = virus_total_analyze_file(temp_path)

        virus_total_results = poll_virus_total_status(analysis_id)
        number = get_number_of_malicious_detections(analysis_id)
        if number > 0:
            pred = f"Class:{predicted_class}, Confidence: {confidence}"
        else:
            pred = "The File is Safe"
        results = {
            'file_info': file_info,
            'hashes': hashes,
            'model_analysis': pred,
            'virus_total_analysis': virus_total_results
        }

        handle_virus_total_analysis(temp_path, analysis_id)
        # # Prepare results from AI analysis
        # results = {
        #     'file_info': file_info,
        #     'hashes': hashes,
        #     'model_analysis': f"class:{predicted_class}, confidence: {confidence}",
        #     'virus_total_analysis_id': analysis_id
        # }
        # if analysis_id:
        #     thread = threading.Thread(target=handle_virus_total_analysis, args=(temp_path, analysis_id))
        #     thread.start()
        response = jsonify(results)

        return response

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500


def poll_virus_total_status(analysis_id, maxRetries=20, wait_time=5):
    virus_total_result = check_virus_total_analysis(analysis_id)
    while virus_total_result is None and maxRetries > 0:
        virus_total_result = check_virus_total_analysis(analysis_id)
        maxRetries -= 1
        time.sleep(wait_time)
    return virus_total_result


@app.route('/virus_total_status/<analysis_id>', methods=['GET'])
def check_virus_total_status(analysis_id):
    virus_total_result = check_virus_total_analysis(analysis_id)
    if virus_total_result is None:
        return jsonify({"status": "pending"}), 202
    else:
        return jsonify({"status": "completed", "virus_total_analysis": virus_total_result})


if __name__ == '__main__':
    app.run(debug=True)
