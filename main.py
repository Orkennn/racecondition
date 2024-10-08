from fastapi import FastAPI
import uvicorn
import asyncio
from fastapi.responses import HTMLResponse
from asyncio import Lock

app = FastAPI()
counter = 0
counter_lock = Lock()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Race Condition Test</title>
        </head>
        <body>
            <h1>Race Condition Test</h1>
            <button onclick="incrementCounter()">Increment Counter</button>
            <h2>Counter: <span id="counter">0</span></h2>
            <script>
                async function incrementCounter() {
                    const numRequests = 10; // Количество параллельных запросов
                    const promises = [];
                    for (let i = 0; i < numRequests; i++) {
                        promises.push(fetch('/increment'));
                    }
                    const responses = await Promise.all(promises);
                    for (const response of responses) {
                        const data = await response.json();
                        console.log(`Counter updated to: ${data.counter}`);
                        document.getElementById('counter').innerText = data.counter;
                    }
                }
            </script>
        </body>
    </html>
    """

@app.get("/increment")
async def increment():
    global counter
    async with counter_lock:
        # Симуляция долгой операции
        await asyncio.sleep(1)  # Можно изменить на случайную задержку
        counter += 1
        return {"counter": counter}

@app.get("/get_counter")
async def get_counter():
    return {"counter": counter}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
