import asyncio
import websockets

connected_clients = set()  # Set to keep track of connected clients

async def send_data_to_clients():
    while True:
        if connected_clients:
            message = "Hello from server!"
            # Send message to each connected client
            for client in connected_clients:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    # Remove client from the set if connection is closed
                    connected_clients.remove(client)
        await asyncio.sleep(5)  # Send message every 5 seconds

async def websocket_server(websocket, path):
    try:
        print("Client connected")
        connected_clients.add(websocket)  # Add client to the set of connected clients

        # Handle incoming messages (optional)
        async for message in websocket:
            print(f"Received message from client: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("Client connection closed")
        connected_clients.remove(websocket)  # Remove client from the set upon disconnection

async def start_websocket_server():
    start_server = await websockets.serve(websocket_server, 'localhost', 8765)
    print("WebSocket server started...")

    # Start sending data to clients in the background
    asyncio.create_task(send_data_to_clients())

    # Keep the server running indefinitely
    await asyncio.Future()  # This keeps the coroutine running

if __name__ == "__main__":
    asyncio.run(start_websocket_server())
