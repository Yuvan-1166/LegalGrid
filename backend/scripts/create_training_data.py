#!/usr/bin/env python3
"""Training Data Generation for Embedding Fine-tuning"""
import sys, os, json, random
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_training_data():
    # 150 positive pairs + 50 negative pairs
    positive = [
        ("indemnification clause enforceability", "Indemnification clauses must be clear and mutual. One-sided indemnity may be challenged under Section 23 IPC.", 1),
        ("termination without notice", "Employment termination requires reasonable notice per Labour Code Section 25.", 1),
        ("liability limitation validity", "Liability clauses cannot exclude gross negligence under Indian Contract Act Section 23.", 1),
        ("non-compete clause scope", "Non-compete clauses must be reasonable in scope, duration, geography.", 1),
        ("IP ownership employment", "IP created during employment belongs to employer unless specified otherwise.", 1),
    ] * 30  # Repeat to get 150
    
    negative = [
        ("contract termination", "Criminal breach of trust requires dishonest misappropriation under IPC 406.", 0),
        ("GST registration", "Arbitration clauses are enforceable under Arbitration Act 1996.", 0),
    ] * 25  # Repeat to get 50
    
    all_pairs = positive + negative
    random.shuffle(all_pairs)
    return all_pairs

def main():
    print("\n" + "="*70)
    print("GENERATING TRAINING DATA")
    print("="*70)
    pairs = generate_training_data()
    os.makedirs("data", exist_ok=True)
    output = {
        "metadata": {"created_at": datetime.now().isoformat(), "total_pairs": len(pairs), 
                     "positive": sum(1 for p in pairs if p[2]==1), "negative": sum(1 for p in pairs if p[2]==0)},
        "training_data": [{"query": q, "document": d, "label": l} for q, d, l in pairs]
    }
    with open("data/embedding_training_data.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"✓ Saved: data/embedding_training_data.json ({len(pairs)} pairs)")
    print("✅ Complete!\n")

if __name__ == "__main__":
    main()
