import json
from pathlib import Path

class GoldenDataset:
    def __init__(self, file_path: str = "evaluation/golden_dataset.json"):
        self.file_path = Path(file_path)
        
    def generate_default(self):
        dataset = [
            {
                "question": "What is artificial intelligence?",
                "expected_answer_concepts": ["machine learning", "mimic human intelligence", "computer systems"]
            },
            {
                "question": "Explain machine learning",
                "expected_answer_concepts": ["data", "algorithms", "learn", "improve"]
            },
            {
                "question": "What is deep learning?",
                "expected_answer_concepts": ["neural networks", "layers", "subset of machine learning"]
            },
            {
                "question": "How do neural networks work?",
                "expected_answer_concepts": ["nodes", "neurons", "weights", "activation", "layers"]
            }
        ]
        
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w") as f:
            json.dump(dataset, f, indent=2)
            
        return dataset

    def load(self):
        if not self.file_path.exists():
            return self.generate_default()
            
        with open(self.file_path, "r") as f:
            return json.load(f)
