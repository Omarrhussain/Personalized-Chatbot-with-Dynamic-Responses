import logging
import time

logger = logging.getLogger(__name__)

class Tracing:
    def __init__(self):
        self.active_traces = {}

    def start_trace(self, trace_id: str, step: str):
        self.active_traces[trace_id] = {"step": step, "start_time": time.time()}
        logger.info(f"Trace {trace_id} started: {step}")

    def end_trace(self, trace_id: str):
        if trace_id in self.active_traces:
            duration = time.time() - self.active_traces[trace_id]["start_time"]
            step = self.active_traces[trace_id]["step"]
            logger.info(f"Trace {trace_id} ended: {step}. Duration: {duration:.3f}s")
            del self.active_traces[trace_id]
