from fastapi import FastAPI, UploadFile, File
import json
import uuid
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=500)

app = FastAPI()

@app.post("/sum")
def get_sum(file: UploadFile = File(...)):
    """
    POST method to calculate the sum of numbers from a JSON file. Return sum
    """
    try:
        contents = file.file.read()
        data = json.loads(contents)
        numbers = data.get("array", [])
        numbers = [int(n) for n in numbers if n is not None]
        total = sum(numbers)
        return {"sum": total}
    except Exception as e:
        return {"error": str(e)}

@app.post("/send_json")
async def get_session_id(file: UploadFile = File(...)):
    """
    POST method to calculate the sum of numbers from a JSON file. Return session ID
    """
    try:
        data = await file.read()
        data = json.loads(data)
        numbers = data.get("array", [])
        session_id = uuid.uuid4().hex
        numbers = [int(n) for n in numbers if n is not None]
        total = sum(numbers)
        cache[session_id] = total
        return {"session_id": session_id}
    except Exception as e:
        return {"error": str(e)}

@app.get("/{session_id}")
async def get_result(session_id: str):
    """
    GET sum by session id
    """
    result = cache.get(session_id)
    if result is None:
        return {"error": "Invalid session id"}
    else:
        return {"sum": result}