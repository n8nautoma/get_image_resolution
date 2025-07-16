from flask import Flask, request, jsonify
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

app = Flask(__name__)

def get_image_resolution(url):
    try:
        print(f"🟡 Получаю изображение: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Проверим Content-Type, чтобы избежать SVG, HTML и т.п.
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            return f"Неверный Content-Type: {content_type}"

        # Пытаемся открыть как изображение
        img = Image.open(BytesIO(response.content))
        img.verify()  # проверка валидности
        img = Image.open(BytesIO(response.content))  # повторно открыть

        return img.size  # (width, height)
    except UnidentifiedImageError:
        return "Ошибка: невозможно определить формат изображения"
    except requests.exceptions.Re
