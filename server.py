import asyncio
import json
import websockets
from queue import Queue
import threading
from queue import Queue
from scan import scan
import socket
import picar_4wd as fc
import json
import time

HOST = "192.168.0.187" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
def move_car_forward(speed, direction):
    start_time = time.time()
    map = {'forward': fc.forward, 'left': fc.turn_left, 'right': fc.turn_right}
    while time.time() - start_time < 0.2:
        map[direction](speed)



async def handle_client(websocket, path):
    try:
        while True:
            data = await websocket.recv()
            print(f"Received message from client: {data}")

            try:
                data = json.loads(data)  # Echo back to client
            except json.JSONDecodeError:
                data = {'duration': 0, 'speed': 0, 'direction': 'stop'}

            result_queue = Queue()

            for i in range(0, int(float(data['duration']) // 0.2)+1):
                move_thread = threading.Thread(target=move_car_forward, args=(data['speed'], data['direction']))
                scan_thread = threading.Thread(target=scan, args=([], result_queue))
                move_thread.start()
                scan_thread.start()

                for thread in [move_thread, scan_thread]:
                    thread.join()
                grid = result_queue.get()

                data_to_send = {'object_locals': grid, 'time_moving': str(i*0.2), 'speed': data['speed']}
                data_json = json.dumps(data_to_send)

                await websocket.send(data_json)

            fc.stop()

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():

    server = await websockets.serve(handle_client, HOST, PORT)
    print(f"WebSocket server listening on {HOST}:{PORT}")