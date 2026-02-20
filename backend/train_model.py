"""
Train blood type classification model using transfer learning with MobileNetV2
"""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class BloodTypeDataset(Dataset):
    """Custom dataset for blood group images"""
    
    def __init__(self, image_dir: str, labels_file: str, transform=None):
        """
        Args:
            image_dir: Directory containing blood group images
            labels_file: CSV file with columns: image_path, blood_type
            transform: Image transforms
        """
        import pandas as pd
        self.image_dir = Path(image_dir)
        self.transform = transform
        self.labels_df = pd.read_csv(labels_file)
        self.blood_types = ["A", "B", "AB", "O"]
    
    def __len__(self):
        return len(self.labels_df)
    
    def __getitem__(self, idx):
        from PIL import Image
        row = self.labels_df.iloc[idx]
        img_path = self.image_dir / row['image_path']
        label = self.blood_types.index(row['blood_type'])
        
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        
        return image, label


def train_blood_type_model(
    train_image_dir: str,
    train_labels_file: str,
    val_image_dir: str = None,
    val_labels_file: str = None,
    epochs: int = 25,
    batch_size: int = 32,
    learning_rate: float = 1e-4,
    output_path: str = None
):
    """
    Train blood type classification model
    
    Args:
        train_image_dir: Path to training images
        train_labels_file: CSV with training labels
        val_image_dir: Path to validation images
        val_labels_file: CSV with validation labels
        epochs: Number of training epochs
        batch_size: Batch size
        learning_rate: Learning rate
        output_path: Where to save the model
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Image transforms
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    # Create datasets
    train_dataset = BloodTypeDataset(train_image_dir, train_labels_file, train_transform)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    val_loader = None
    if val_image_dir and val_labels_file:
        val_dataset = BloodTypeDataset(val_image_dir, val_labels_file, val_transform)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    # Load pre-trained MobileNetV2
    model = models.mobilenet_v2(pretrained=True)
    
    # Freeze early layers
    for param in model.features.parameters():
        param.requires_grad = False
    
    # Replace classifier
    model.classifier = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(1280, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(256, 4)  # 4 blood types
    )
    
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.classifier.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)
    
    # Training loop
    best_val_loss = float('inf')
    
    for epoch in range(epochs):
        # Train
        model.train()
        train_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        
        # Validate
        val_loss = 0.0
        if val_loader:
            model.eval()
            correct = 0
            total = 0
            with torch.no_grad():
                for images, labels in val_loader:
                    images, labels = images.to(device), labels.to(device)
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                    val_loss += loss.item()
                    
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
            
            val_loss /= len(val_loader)
            val_accuracy = correct / total
            scheduler.step(val_loss)
            
            print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f}, "
                  f"Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.2%}")
            
            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                if output_path:
                    torch.save(model.state_dict(), output_path)
                    print(f"Model saved to {output_path}")
        else:
            print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f}")
    
    return model


if __name__ == "__main__":
    # Example usage
    train_blood_type_model(
        train_image_dir="data/train/images",
        train_labels_file="data/train/labels.csv",
        val_image_dir="data/val/images",
        val_labels_file="data/val/labels.csv",
        epochs=25,
        batch_size=32,
        output_path="backend/models/agglutination_model.pth"
    )
