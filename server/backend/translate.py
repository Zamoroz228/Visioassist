from transformers import MarianMTModel, MarianTokenizer

class EnglishToRussianTranslator:
    def __init__(self):
        self.model_name = "Helsinki-NLP/opus-mt-en-ru"
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    def translate(self, text: str) -> str:
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = self.model.generate(**inputs)
        return self.tokenizer.decode(translated[0], skip_special_tokens=True)