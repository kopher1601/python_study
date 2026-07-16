from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Server received: {message}")
    except WebSocketDisconnect:
        print("WebSocket connection closed")
