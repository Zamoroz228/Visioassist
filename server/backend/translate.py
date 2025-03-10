from transformers import MarianMTModel, MarianTokenizer

class EnglishToRussianTranslator:
    """
    Класс для перевода текста с английского на русский.
    Модель и токенизатор загружаются один раз и остаются в памяти.
    """
    def __init__(self):
        """
        Конструктор класса. Загружает модель и токенизатор.
        """
        self.model_name = "Helsinki-NLP/opus-mt-en-ru"
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    def translate(self, text: str) -> str:
        """
        Перевод текста с английского на русский.
        :param text: Строка на английском языке для перевода.
        :return: Переведённая строка на русском языке.
        """
        # Токенизация входного текста
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        # Генерация перевода
        translated = self.model.generate(**inputs)
        # Декодирование результата
        return self.tokenizer.decode(translated[0], skip_special_tokens=True)