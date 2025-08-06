import json
import time

class HotspotDetector:
    def __init__(self, threshold=27.0):
        self.threshold = threshold
        self.processed_count = 0
        
    def process_sensor_data(self, sensor_data):
        start_time = time.time()
        
        # Simple edge logic: detect if temperature > threshold
        is_hotspot = sensor_data["temperature"] > self.threshold
        
        processing_time = (time.time() - start_time) * 1000  # ms
        
        self.processed_count += 1
        
        result = {
            "room_id": sensor_data["room_id"],
            "temperature": sensor_data["temperature"],
            "hotspot_detected": is_hotspot,
            "edge_processing_time_ms": round(processing_time, 2),
            "processed_at_edge": True,
            "timestamp": sensor_data["timestamp"]
        }
        
        print(f"Edge processed: Room {result['room_id']}, Hotspot: {is_hotspot}, Time: {processing_time:.2f}ms")
        return result

if __name__ == "__main__":
    detector = HotspotDetector()
    
    test_data = {"room_id": 1, "temperature": 28.5, "timestamp": time.time()}
    result = detector.process_sensor_data(test_data)
    print(json.dumps(result, indent=2))
