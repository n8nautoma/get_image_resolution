from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

def get_image_resolution(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img.size  # (width, height)
    except Exception as e:
        return str(e)

@app.route("/resolution", methods=["GET"])
def resolution():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    result = get_image_resolution(url)
    if isinstance(result, tuple):
        width, height = result
        return jsonify({"width": width, "height": height})
    else:
        return jsonify({"error": result}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
