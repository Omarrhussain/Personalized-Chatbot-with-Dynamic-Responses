import logging

logger = logging.getLogger(__name__)

class OnlineMonitor:
    def __init__(self):
        self.latency_threshold_sec = 5.0

    def check_anomaly(self, duration: float, success: bool, sources_count: int):
        """
        Monitors real-time query metrics and logs anomalies.
        """
        if not success:
            logger.error("🚨 ONLINE MONITOR: Query failed.")
            
        if duration > self.latency_threshold_sec:
            logger.warning(f"⚠️ ONLINE MONITOR: High latency detected ({duration:.2f}s).")
            
        if sources_count == 0 and success:
            logger.warning("⚠️ ONLINE MONITOR: Successful query but 0 context sources retrieved. Potential hallucination risk.")
