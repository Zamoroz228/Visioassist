import requests

image_path = '/home/andrey/python/photo_max.jpg'
server_url = 'http://91.77.167.51:5000/process_image'

def ping(url = server_url, timeout=1):
    try:
        response = requests.head(url, timeout=timeout)
        return True
    except requests.RequestException:
        return False

def generation_text(mode):
    with open(image_path, 'rb') as image:
        files = {'image': image}
        form = {'mode': mode}
        response = requests.post(server_url, files=files, data=form)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                'error': f'Ошибка: {response.status_code}',
                'details': response.text
            }