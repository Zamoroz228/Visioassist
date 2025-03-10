import torch
from PIL import Image
from torchvision import transforms
from transformers import VisionEncoderDecoderModel, AutoTokenizer, ViTImageProcessor

MODEL_PATH = "models/model_epoch_5.pt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = None
tokenizer = None
processor = None


def initialize_model(model_path=MODEL_PATH):
    global model, tokenizer, processor

    model = VisionEncoderDecoderModel.from_encoder_decoder_pretrained(
        "google/vit-base-patch16-224-in21k",
        "gpt2"
    )
    checkpoint = torch.load(model_path, map_location=DEVICE)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(DEVICE)
    model.eval()

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")


def process_image(image_path):
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image_tensor = transform(image).unsqueeze(0)
    return image_tensor.to(DEVICE)


def generate_caption(image_path):
    global model, tokenizer, processor

    image_tensor = process_image(image_path)
    with torch.no_grad():
        generated_ids = model.generate(
            pixel_values=image_tensor,
            max_length=64,
            num_beams=5,
            temperature=0.7
        )
    caption = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return caption