from flask import Flask, request, jsonify
import ollama
import re
import json
import time
import os
import uuid
from flask import send_from_directory
from validation import validate_image

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/extract-invoice", methods=["POST"])
def extract_invoice():

    print(" ----------------- step 1 ------------------ ")

    try:
        image_path = None

        if "image" in request.files:
            image_file = request.files["image"]
            # save_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
            ext = os.path.splitext(image_file.filename)[1]
            unique_name = f"{uuid.uuid4().hex}{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, unique_name)

            image_file.save(save_path)
            image_path = save_path

        if not image_path:
            return jsonify({"status": "fail", "message": "image (form-data) or image_path (JSON) is required"}), 400

        # validate image
        validate_image(image_path)

        prompt = "From this invoice, I need the party name, party address, party GST number, invoice amount, taxable amount, and all item details including item names and quantities, properly listed in JSON formatand,and if the image is cropped, blurry, or low quality then ask to re-upload a proper clear image."
        # prompt = "From this invoice, I need the party name, party address, party GST number, invoice amount, taxable amount, and all item details including item names and quantities, properly listed in JSON format"

        start_time = time.time()

        resp = ollama.chat(
            # model="qwen2.5vl:32b",
            model="qwen2.5vl:7b",
            messages=[{
                "role": "user",
                "content": prompt,
                "images": [image_path]
            }],
            stream=True 
        )

        print("RAW RESPONSE=========:\n", resp)

        content = ""
        for chunk in resp:
            if "message" in chunk and "content" in chunk["message"]:
                content += chunk["message"]["content"]

        end_time = time.time()
        elapsed = end_time - start_time

        # JSON extract
        match = re.search(r"```json\n(.*?)```", content, re.DOTALL)

        if match:
            json_data = json.loads(match.group(1))

            print("json_data", json_data)

            return jsonify({
                "status": "success",
                "message": "Invoice extracted successfully",
                "response": json_data,
                "elapsed_time": f"{elapsed:.2f} seconds"
            })

        else:
            return jsonify({
                "status": "fail",
                "message": "JSON not found in model response",
                "raw_response": content
            }), 422

    except FileNotFoundError as fnf:
        return jsonify({"status": "fail", "message": str(fnf)}), 404

    except ValueError as ve:
        return jsonify({"status": "fail", "message": str(ve)}), 400

    except Exception as e:
        return jsonify({"status": "fail", "message": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
