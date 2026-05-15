import json
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.rag_pipeline import RAGPipeline

class OfflineEval:
    def __init__(self):
        self.chatbot = RAGPipeline()
        self.test_questions = [
            "What is artificial intelligence?",
            "Explain machine learning",
            "What is deep learning?",
            "How do neural networks work?"
        ]

    def run_evaluation(self):
        records = []

        print("Starting Evaluation Pipeline...")
        for q in self.test_questions:
            print(f"Testing: {q}")
            response = self.chatbot.ask_question(q, use_history=False)
            records.append({
                "question": q,
                "answer": response["answer"],
                "success": response["success"],
            })
            if response["success"]:
                print("Success")
            else:
                print(f"Failed: {response['answer']}")

        scores = {"success_rate": sum(1 for r in records if r["success"]) / len(records) * 100}

        report = {
            "timestamp": datetime.now().isoformat(),
            "scores": scores,
            "records": records
        }

        with open("evaluation_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print("RAG Evaluation Complete! Scores:")
        for k, v in scores.items():
            print(f"{k}: {v:.1f}%")

        return report

if __name__ == "__main__":
    OfflineEval().run_evaluation()
