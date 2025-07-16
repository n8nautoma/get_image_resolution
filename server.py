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

        content_type = response.headers.get("Content-Type", "")
        print(f"ℹ️ Content-Type: {content_type}")

        if not content_type.startswith("image/"):
            return f"Неверный тип содержимого: {content_type}"

        img = Image.open(BytesIO(response.content))
        img.load()  # для избежания ошибок PIL
        return img.size
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")
        return str(e)

