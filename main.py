from fastapi import FastAPI

app = FastAPI(title="Minimal API", version="0.1.0")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/echo")
def echo(payload: dict):
    # Just reflects whatever JSON you send
    return {"you_sent": payload}