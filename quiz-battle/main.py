from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, payload: dict):
        for connection in self.active_connections:
            await connection.send_json(payload)

    def connection_count(self) -> int:
        return len(self.active_connections)

manager = ConnectionManager()


@app.websocket("/ws/{nickname}")
async def websocket_endpoint(websocket: WebSocket, nickname: str):
    await manager.connect(websocket)

    await manager.broadcast(
        {
            "type": "user.joined",
            "data": {
                "nickname": nickname,
                "online_count": manager.connection_count(),
            }
        }
    )

    try:
        while True:
            payload = await websocket.receive_json()

            if payload.get("type") != "chat.message":
                continue

            data = payload.get("data")

            if not isinstance(data, dict):
                continue

            message = data.get("message")

            if not isinstance(message, str) or not message.strip():
                continue

            await manager.broadcast(
                {
                    "type": "chat.message",
                    "data": {
                        "sender": nickname,
                        "message": message.strip(),
                    }
                }
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            {
                "type": "user.left",
                "data": {
                    "nickname": nickname,
                    "online_count": manager.connection_count(),
                }
            }
        )
        print("WebSocket connection closed")
