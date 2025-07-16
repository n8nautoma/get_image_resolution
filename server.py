from flask import Flask, request, jsonify
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

app = Flask(__name__)

def get_image_resolution(url):
    try:
        print(f"📥 Загружаю изображение: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")a
        print(f"ℹ️ Content-Type: {content_type}")

        if not content_type.startswith("image/"):
            return f"Неверный тип содержимого: {content_type}"

        img = Image.open(BytesIO(response.content))
        img.load()  # для избежания ошибок PIL
        return img.size
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")
        return str(e)

@app.route('/resolution', methods=['GET'])
def get_resolution():
    try:
        image_url = request.args.get('url')
        
        if not image_url:
            return jsonify({"error": "URL параметр обязателен"}), 400
        
        result = get_image_resolution(image_url)
        
        if isinstance(result, tuple) and len(result) == 2:
            return jsonify({
                "width": result[0],
                "height": result[1],
                "resolution": f"{result[0]}x{result[1]}"
            })
        else:
            return jsonify({"error": result}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
