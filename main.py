from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()

# Gerenciar conexões ativas de WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str, sender: WebSocket):
        for connection in self.active_connections:
            if connection != sender:
                await connection.send_text(message)

# Inicialização do gerenciador de conexões
manager = ConnectionManager()

# Rota para servir a página HTML do chat
@app.get("/")
async def get():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Endpoint WebSocket para lidar com conexões WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, websocket)
            await websocket.send_text(f"Você: {data}")  # Envia a mensagem de volta para o remetente
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Cliente saiu do chat", websocket)  # Informa quando um cliente desconectar

# Monta o diretório 'static' para servir arquivos estáticos (CSS, JS, imagens)
app.mount("/static", StaticFiles(directory="static"), name="static")
