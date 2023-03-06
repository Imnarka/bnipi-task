# Тестовое задание

## Содержание
1. [Описание](#Описание)
2. [Решение](#решение)
3. [Руководство запуска](#руководство-запуска)


# Описание
### Необходимо разработать сервис REST API с интерфейсом openapi/swagger ui, который на входе будет получать файл json формата со списком цифр, обратно пользователю направлять сумму всех цифр.

Пример json файла:

```json
{

"array": ["1", "2", "3", "4", null]

}
```
Реализовать с помощью двух методов:

1) Синхронный

2) Асинхронный (пользователь получает ID сессии и получает ответ по ID сессии). Реализовать простую схему хранения сессии и результата

Весь код должен запускаться в виде докер сервиса.

# Решение
Для синхронного метода трудно пока представить, как сделать form-data без ```await``` сделал так
```python
@app.post("/sum")
def get_sum(data: dict):
    """
    POST method to calculate the sum of numbers from a JSON file. Return sum
    """
    numbers = data.get("array", [])
    numbers = [int(n) for n in numbers if n is not None]
    total = sum(numbers)
    return {"sum": total}
``` 

Для ассинхронного метода форма загрузки работает:
```python
@app.post("/send_json")
async def get_session_id(file: UploadFile = File(...)):
    """
    POST method to calculate the sum of numbers from a JSON file. Return session ID
    """
    data = await file.read()
    data = json.loads(data)
    numbers = data.get("array", [])
    session_id = uuid.uuid4().hex
    numbers = [int(n) for n in numbers if n is not None]
    total = sum(numbers)
    cache[session_id] = total
    return {"session_id": session_id}


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
```

# Руководство запуска

```
cd /path/to/repository/
```
```
docker build -t myimage .
```
```
docker run -d --name mycontainer -p 80:8000 myimage
```
Открываем веб приложение по пути ```/docs```