import os
import json
from tqdm import tqdm
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torch
import torch.optim as optim
from transformers import (
    VisionEncoderDecoderModel,
    AutoTokenizer,
    ViTImageProcessor,
)


TRAIN_IMAGES_DIR = "dataset/train2017"
VAL_IMAGES_DIR = "dataset/val2017"
TRAIN_ANN_PATH = "dataset/annotations/captions_train2017.json"
VAL_ANN_PATH = "dataset/annotations/captions_val2017.json"

with open(TRAIN_ANN_PATH, 'r', encoding='utf-8') as f:
    train_ann = json.load(f)
with open(VAL_ANN_PATH, 'r', encoding='utf-8') as f:
    val_ann = json.load(f)

train_img_id2file = {img["id"]: img["file_name"] for img in train_ann["images"]}
val_img_id2file = {img["id"]: img["file_name"] for img in val_ann["images"]}

train_data = []
for ann in train_ann["annotations"]:
    img_id = ann["image_id"]
    caption = ann["caption"]
    img_file = train_img_id2file[img_id]
    img_path = os.path.join(TRAIN_IMAGES_DIR, img_file)
    train_data.append((img_path, caption))

val_data = []
for ann in val_ann["annotations"]:
    img_id = ann["image_id"]
    caption = ann["caption"]
    img_file = val_img_id2file[img_id]
    img_path = os.path.join(VAL_IMAGES_DIR, img_file)
    val_data.append((img_path, caption))

image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

class COCODataset(Dataset):
    def __init__(self, data, tokenizer, max_length=64, transform=None):
        self.data = data
        self.transform = transform
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path, caption = self.data[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)

        tokenized = self.tokenizer(
            caption,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        input_ids = tokenized.input_ids.squeeze(0)
        attention_mask = tokenized.attention_mask.squeeze(0)

        return image, input_ids, attention_mask
model = VisionEncoderDecoderModel.from_encoder_decoder_pretrained(
    "google/vit-base-patch16-224-in21k",
    "gpt2"
)

image_processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

model.config.decoder_start_token_id = tokenizer.bos_token_id
model.config.pad_token_id = tokenizer.pad_token_id
model.config.vocab_size = len(tokenizer)

train_dataset = COCODataset(train_data, tokenizer, transform=image_transform)
val_dataset = COCODataset(val_data, tokenizer,transform=image_transform)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=0)

if torch.cuda.is_available():
    print('Use cuda')
    device=torch.device("cuda")
else:
    print('Use cpu')
    device=torch.device("cpu")

model.to(device)

optimizer = optim.AdamW(model.parameters(), lr=1e-4)

checkpoint_path = "models/model_epoch_2.pt"
checkpoint = torch.load(checkpoint_path)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
start_epoch = checkpoint['epoch'] + 1

def train_epoch(model, loader, optimizer, epoch, total_epochs):
    model.train()
    total_loss = 0
    pbar = tqdm(loader, desc=f"Training Epoch {epoch}/{total_epochs}", leave=True)
    for images, input_ids, attention_mask in pbar:
        images = images.to(device)
        input_ids = input_ids.to(device)

        outputs = model(
            pixel_values=images,
            labels=input_ids  
        )

        loss = outputs.loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        pbar.set_postfix({"loss": f"{loss.item():.4f}"})
    return total_loss / len(loader)


def validate(model, loader, epoch, total_epochs):
    model.eval()
    total_loss = 0
    pbar = tqdm(loader, desc=f"Validation Epoch {epoch}/{total_epochs}", leave=True)
    with torch.no_grad():
        for images, input_ids, attention_mask in pbar:
            images = images.to(device)
            input_ids = input_ids.to(device)

            outputs = model(
                pixel_values=images,
                labels=input_ids
            )

            loss = outputs.loss
            total_loss += loss.item()
            pbar.set_postfix({"val_loss": f"{loss.item():.4f}"})
    return total_loss / len(loader)

if __name__ == '__main__':
    EPOCHS = 5
    for epoch in range(start_epoch, EPOCHS + 1):
        train_loss = train_epoch(model, train_loader, optimizer, epoch, EPOCHS)
        
        val_loss = validate(model, val_loader, epoch, EPOCHS)
        
        print(f"Epoch {epoch}/{EPOCHS}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
        
        save_path = os.path.join("models", f"model_epoch_{epoch}.pt") 
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'train_loss': train_loss,
            'val_loss': val_loss
        }, save_path)
        print(f"Model saved to {save_path}") 