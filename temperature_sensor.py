import asyncio
import json
import random
from azure.iot.device.aio import IoTHubDeviceClient

CONNECTION_STRING = "connection_string"

async def main():
    # Create IoT Hub client
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    await device_client.connect()
    
    print("Sensor started")
    
    while True:
        # Simulate building with 4 rooms
        for room_id in range(0, 5):
            # Generate realistic temperature
            # 10% chance of hotspot
            if random.random() < 0.1:
                # hotspot
                temperature = random.uniform(28, 35)
                is_hotspot = True
            else:
                # normal temp
                temperature = random.uniform(20, 26)
                is_hotspot = False
            
            # Create sensor data
            sensor_data = {
                "room_id": room_id,
                "temperature": round(temperature, 2),
                "timestamp": asyncio.get_event_loop().time(),
                "is_hotspot": is_hotspot
            }
            
            # Send to IoT Hub
            message = json.dumps(sensor_data)
            await device_client.send_message(message)
            print(f"Sent: Room {room_id}, Temp: {temperature:.2f}°C, Hotspot: {is_hotspot}")
        
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
