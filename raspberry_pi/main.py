import lgpio
from capture_image import take_photo
from tesserasct import TesseractOCRProcessor
from sound import SileroTTS
from api import generation_text, ping
import time

h = lgpio.gpiochip_open(0)

BUTTON1_PIN = 17
BUTTON2_PIN = 27

lgpio.gpio_claim_input(h, BUTTON1_PIN, lgpio.SET_PULL_UP)
lgpio.gpio_claim_input(h, BUTTON2_PIN, lgpio.SET_PULL_UP)

last_button1_state = 1
last_button2_state = 1

sound = SileroTTS()
ocr = TesseractOCRProcessor()
time.sleep(10)
connect_server = ping()
sound.play('Есть соединение с сервером' if connect_server else 'Нет соединения с сервером')

try:
    while True:
        button1_state = lgpio.gpio_read(h, BUTTON1_PIN)
        button2_state = lgpio.gpio_read(h, BUTTON2_PIN)
    
        if button1_state == 0 and last_button1_state == 1:
            if connect_server:
                take_photo()
                text=generation_text('1')['result']
            else:
                text = ocr.recognize_text(take_photo())
            sound.play(text)
        if button2_state == 0 and last_button2_state == 1:
            if connect_server:
                take_photo()
                text=generation_text('2')['result']
            else:
                text = ocr.recognize_text(take_photo())
            sound.play(text)  
        last_button1_state = button1_state
        last_button2_state = button2_state
        
        time.sleep(0.01) 

except KeyboardInterrupt:
    print("\nПрограмма завершена")
finally:
    lgpio.gpiochip_close(h)
