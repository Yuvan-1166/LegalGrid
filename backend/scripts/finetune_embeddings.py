#!/usr/bin/env python3
"""Fine-tune Sentence Transformers on Legal Domain"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from datetime import datetime

def load_training_data():
    with open("data/embedding_training_data.json", "r") as f:
        data = json.load(f)
    examples = [
        InputExample(texts=[item["query"], item["document"]], label=float(item["label"]))
        for item in data["training_data"]
    ]
    return examples

def finetune_model():
    print("\n" + "="*70)
    print("FINE-TUNING EMBEDDINGS FOR LEGAL DOMAIN")
    print("="*70)
    print(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Load base model
    print("Loading base model: all-mpnet-base-v2...")
    model = SentenceTransformer("all-mpnet-base-v2")
    
    # Load training data
    print("Loading training data...")
    train_examples = load_training_data()
    print(f"✓ Loaded {len(train_examples)} training pairs\n")
    
    # Create DataLoader
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    
    # Define loss
    train_loss = losses.CosineSimilarityLoss(model)
    
    # Fine-tune
    print("Fine-tuning (this may take 30-60 minutes)...")
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=3,
        warmup_steps=100,
        output_path="models/legal-mpnet-finetuned",
        show_progress_bar=True
    )
    
    print(f"\n✓ Model saved: models/legal-mpnet-finetuned")
    print(f"End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n✅ Fine-tuning complete!\n")

if __name__ == "__main__":
    finetune_model()
