import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ExifTags
from neural_network import generate_caption, initialize_model
from translate import EnglishToRussianTranslator
from tesseract import TesseractOCRProcessor

app = Flask(__name__)
CORS(app)

ocr = TesseractOCRProcessor()
initialize_model()
translator = EnglishToRussianTranslator()

def fix_image_orientation(image):
    try:
        exif = image._getexif()
        if exif is None:
            return image
            
        orientation_key = None
        for key, value in ExifTags.TAGS.items():
            if value == 'Orientation':
                orientation_key = key
                break
                
        if orientation_key and orientation_key in exif:
            orientation = exif[orientation_key]
            
            if orientation == 2:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                image = image.rotate(180)
            elif orientation == 4:
                image = image.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                image = image.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                image = image.rotate(-90, expand=True)
            elif orientation == 7:
                image = image.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
                
        return image
    except Exception as e:
        print(f"Ошибка при исправлении ориентации: {str(e)}")
        return image
    

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok'})

@app.route('/last_image', methods=['GET'])
def get_last_image():
    try:
        file_path = os.path.join("uploads", "image.png")
    
        if not os.path.exists(file_path):
            return jsonify({'error': 'Image not found'}), 404
            
        return send_file(file_path, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        
        mode = request.form.get('mode')
        
        file = request.files.get('image')
        if file is None:
            print("Файл не найден в запросе")
            return jsonify({'error': 'No image file provided'}), 400

        image = Image.open(file.stream)
        
        image = fix_image_orientation(image)
        
        file_path = os.path.join("uploads", "image.png")
        image.save(file_path)
        
        result = None
        if mode == '1':
            result = ocr.recognize_text(file_path)
        elif mode == '2':
            text = generate_caption(file_path)
            result = translator.translate(text)
        else:
            print(f"Неверный режим: {mode}")
            return jsonify({'error': 'Invalid mode parameter'}), 400
        
        response_data = {'result': result if result else 'Обработка завершена, но результат пустой'}
        print(f"Отправляем ответ: {response_data}")
        return jsonify(response_data)
    
    except Exception as e:
        import traceback
        print(f"Ошибка: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
