from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from werwolf_main import run_streamed_game
import json


app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "online"}
    
@app.post("/game/start")
def start_game():
    def event_generator():
        for data in run_streamed_game():
            yield f"data: {json.dumps(data)}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

