from fastapi import FastAPI, UploadFile, File
from typing import List
import json
import uuid
from cachetools import TTLCache
import asyncio

cache = TTLCache(maxsize=100, ttl=500)

app = FastAPI()

app.sessions = {} # {session: task object}

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

async def calculate_sum(numbers: List[int]):
    return sum([int(n) for n in numbers if n is not None])

@app.post("/sum_async")
async def sum_numbers_handler(file: UploadFile = None, session_id: str = None):
    """
    Async method to calculate the sum of numbers from a JSON file.
    1st case: Send the file and get session id
    2nd case: Send the session id and get sum of numbers
    """
    if session_id is None:
        session_id = str(uuid.uuid4())
    if session_id in app.sessions:
        task = app.sessions[session_id]
        if not task.done():
            return {"status": "calculated"}
        try:
            total = await task
        except Exception as e:
            raise f'Error: {e}'
        
        del app.sessions[session_id]
        return {"sum": total}
    
    if file is not None:
        data = await file.read()
        data = json.loads(data)
        numbers = data.get("array", [])
        if numbers is not None:
            task = asyncio.create_task(calculate_sum(numbers))
            app.sessions[session_id] = task
            return {"session_id": session_id}
    raise "File or session id were not uploaded"