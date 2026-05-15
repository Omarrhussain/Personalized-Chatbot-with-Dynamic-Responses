import logging
import json
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class FeedbackCollector:
    def __init__(self, log_file: str = "data/feedback/user_feedback.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log_feedback(self, trace_id: str, rating: int, comment: str = ""):
        """
        Logs user feedback linked to a specific trace_id.
        Rating: 1 (positive) or 0 (negative)
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "trace_id": trace_id,
            "rating": rating,
            "comment": comment
        }
        
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
            logger.info(f"Feedback logged for trace {trace_id}")
        except Exception as e:
            logger.error(f"Failed to log feedback: {e}")
