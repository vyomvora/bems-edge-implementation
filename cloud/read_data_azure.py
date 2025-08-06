import asyncio
import json
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
import time
import random
import pandas as pd
from collections import deque

class AzureDataReader:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.data_buffer = deque(maxlen=100)
        
    def simulate_cloud_processing(self, data):
        start_time = time.time()
        time.sleep(0.1)
        processing_time = (time.time() - start_time) * 1000
        
        return {
            **data,
            "cloud_processing_time_ms": round(processing_time, 2),
            "processed_at_cloud": True
        }
    
    def get_latest_data(self):
        if not self.data_buffer:
            return self.generate_sample_data()
        
        return list(self.data_buffer)
    
    def generate_sample_data(self):
        data = []
        current_time = time.time()
        
        for room_id in range(1, 5):
            # different base temps per room
            base_temp = 22 + (room_id * 0.5)  
            
            # time based variation
            hour = time.localtime().tm_hour
            time_factor = 1 + 0.3 * max(0, hour - 12) / 12
            
            if room_id == 2 and hour > 14:
                temp = base_temp * time_factor + random.uniform(3, 8)
            else:
                temp = base_temp * time_factor + random.uniform(-1, 2)
            
            is_hotspot = temp > 27
            
            data.append({
                "room_id": room_id,
                "temperature": round(temp, 1),
                "is_hotspot": is_hotspot,
                "timestamp": current_time,
                "edge_processing_time_ms": round(random.uniform(1, 5), 2),
                "cloud_processing_time_ms": round(random.uniform(80, 150), 2)
            })
        
        return data

if __name__ == "__main__":
    reader = AzureDataReader("connectionstring")
    data = reader.get_latest_data()
    print(json.dumps(data, indent=2))
