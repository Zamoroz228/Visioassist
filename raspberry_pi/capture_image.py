from picamera2 import Picamera2
import time

def take_photo():
    try:
        picam2 = Picamera2()
        config = picam2.create_still_configuration(
            main={"size": (4608, 2592)},
            encode="main"
        )
        
        picam2.configure(config)
        
        picam2.set_controls({
            "AeEnable": True,
            "AfMode": 2,
            "AwbEnable": True,
            "Brightness": 0.1,
            "Contrast": 1.1,
            "Sharpness": 2.0
        })
        
        picam2.start()
        time.sleep(4)
        
        filename = "photo_max.jpg"
        picam2.capture_file(filename)

        return filename
    finally:
        picam2.close()