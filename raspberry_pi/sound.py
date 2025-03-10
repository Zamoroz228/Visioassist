import os
import torch
import soundfile as sf
import pygame
from pathlib import Path

class SileroTTS:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.base_dir = Path(os.path.dirname(__file__))
        self.models_dir = self.base_dir / "models"
        self.audio_dir = self.base_dir / "audio"
        self.audio_dir.mkdir(exist_ok=True)
    
        self.device = torch.device('cpu')
        model_file = self.models_dir / "model.pt"
        print(f"Loading model from: {model_file}")
        self.model = torch.package.PackageImporter(model_file).load_pickle("tts_models", "model")
        self.model.to(self.device)
    
    def play(self, text):
        if not text:
            text = "Текст не распознан"
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        speaker = 'xenia'
        
        sample_rate = 48000
        audio = self.model.apply_tts(
            text=text,
            speaker=speaker,
            sample_rate=sample_rate
        )
        
        audio_file = self.audio_dir / "temp_speech.wav"
        sf.write(str(audio_file), audio.numpy(), sample_rate)
    
        pygame.mixer.music.load(str(audio_file))
        pygame.mixer.music.play()