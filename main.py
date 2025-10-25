
from fastapi import FastAPI, HTTPException
from resources_config import resources

app = FastAPI(title="Environment Access Controller API", version="1.0.0")
# Health and utility endpoints
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/echo")
def echo(payload: dict):
    return {"you_sent": payload}

@app.get("/status")
def get_all_status():
    return resources.get_all_status()

@app.get("/help")
def get_help():
    return {
        "general": [
            "GET /health - Health check",
            "POST /echo - Echo payload",
            "GET /status - Get all resource statuses",
            "GET /help - Get this help"
        ],
        "publishers": [
            "GET /publishers - List all publishers",
            "GET /publishers/available - List available publishers",
            "GET /publishers/info/{publisher_id} - Get publisher info",
            "GET /publishers/status/{publisher_id} - Get publisher status",
            "GET /publishers/history/{publisher_id} - Get publisher history",
            "POST /publishers/take/{publisher_id}?user=<username> - Take publisher",
            "POST /publishers/steal/{publisher_id}?user=<username> - Steal publisher",
            "POST /publishers/release/{publisher_id} - Release publisher"
        ],
        "environments": [
            "GET /environments - List all environments",
            "GET /environments/available - List available environments",
            "GET /environments/info/{env_name} - Get environment info",
            "GET /environments/status/{env_name} - Get environment status",
            "GET /environments/history/{env_name} - Get environment history",
            "POST /environments/take/{env_name}?user=<username> - Take environment",
            "POST /environments/steal/{env_name}?user=<username> - Steal environment",
            "POST /environments/release/{env_name} - Release environment"
        ]
    }

# ==================== Publisher Endpoints ====================

@app.get("/publishers")
def list_all_publishers():
    return {
        pub_id: pub.get_info()
        for pub_id, pub in resources.get_all_publishers().items()
    }

@app.get("/publishers/available")
def list_available_publishers():
    available = resources.get_available_publishers()
    return {
        pub.metadata.get("publisherId", pub.name): pub.get_info()
        for pub in available
    }

@app.get("/publishers/info/{publisher_id}")
def get_publisher(publisher_id: str):
    publisher = resources.get_publisher(publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail=f"Publisher not found: {publisher_id}")
    return publisher.get_info()

@app.get("/publishers/status/{publisher_id}")
def get_publisher_status(publisher_id: str):
    publisher = resources.get_publisher(publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail=f"Publisher not found: {publisher_id}")
    return publisher.get_status()

@app.get("/publishers/history/{publisher_id}")
def get_publisher_history(publisher_id: str):
    publisher = resources.get_publisher(publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail=f"Publisher not found: {publisher_id}")
    return {
        "publisher_id": publisher_id,
        "history": publisher.get_history()
    }

@app.post("/publishers/take/{publisher_id}")
def take_publisher(publisher_id: str, user: str):
    publisher = resources.get_publisher(publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail=f"Publisher not found: {publisher_id}")

    success = publisher.try_to_take(user)
    if success:
        return {
            "success": True,
            "message": f"Publisher {publisher_id} successfully taken by {user}",
            "status": publisher.get_status()
        }
    else:
        return {
            "success": False,
            "message": f"Publisher {publisher_id} is already taken by {publisher.taken_by}",
            "status": publisher.get_status()
        }

@app.post("/publishers/steal/{publisher_id}")
def steal_publisher(publisher_id: str, user: str):
    publisher = resources.get_publisher(publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail=f"Publisher not found: {publisher_id}")

    previous_owner = publisher.taken_by
    publisher.steal(user)

    return {
        "success": True,
        "message": f"Publisher {publisher_id} stolen by {user}" +
                   (f" from {previous_owner}" if previous_owner else ""),
        "previous_owner": previous_owner,
        "status": publisher.get_status()
    }

@app.post("/publishers/release/{publisher_id}")
def release_publisher(publisher_id: str):
    publisher = resources.get_publisher(publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail=f"Publisher not found: {publisher_id}")

    success = publisher.release()
    if success:
        return {
            "success": True,
            "message": f"Publisher {publisher_id} successfully released",
            "status": publisher.get_status()
        }
    else:
        return {
            "success": False,
            "message": f"Publisher {publisher_id} was not taken",
            "status": publisher.get_status()
        }

# ==================== Environment Endpoints ====================
@app.get("/environments")
def list_all_environments():
    return {
        env_id: env.get_info()
        for env_id, env in resources.get_all_environments().items()
    }

@app.get("/environments/available")
def list_available_environments():
    available = resources.get_available_environments()
    return {
        env.name: env.get_info()
        for env in available
    }

@app.get("/environments/info/{env_name}")
def get_environment(env_name: str):
    environment = resources.get_environment(env_name)
    if not environment:
        raise HTTPException(status_code=404, detail=f"Environment not found: {env_name}")
    return environment.get_info()

@app.get("/environments/status/{env_name}")
def get_environment_status(env_name: str):
    environment = resources.get_environment(env_name)
    if not environment:
        raise HTTPException(status_code=404, detail=f"Environment not found: {env_name}")
    return environment.get_status()


@app.get("/environments/history/{env_name}")
def get_environment_history(env_name: str):
    environment = resources.get_environment(env_name)
    if not environment:
        raise HTTPException(status_code=404, detail=f"Environment not found: {env_name}")
    return {
        "environment_name": env_name,
        "history": environment.get_history()
    }

@app.post("/environments/take/{env_name}")
def take_environment(env_name: str, user: str):
    environment = resources.get_environment(env_name)
    if not environment:
        raise HTTPException(status_code=404, detail=f"Environment not found: {env_name}")

    success = environment.try_to_take(user)
    if success:
        return {
            "success": True,
            "message": f"Environment {env_name} successfully taken by {user}",
            "status": environment.get_status()
        }
    else:
        return {
            "success": False,
            "message": f"Environment {env_name} is already taken by {environment.taken_by}",
            "status": environment.get_status()
        }

@app.post("/environments/steal/{env_name}")
def steal_environment(env_name: str, user: str):
    environment = resources.get_environment(env_name)
    if not environment:
        raise HTTPException(status_code=404, detail=f"Environment not found: {env_name}")

    previous_owner = environment.taken_by
    environment.steal(user)

    return {
        "success": True,
        "message": f"Environment {env_name} stolen by {user}" +
                   (f" from {previous_owner}" if previous_owner else ""),
        "previous_owner": previous_owner,
        "status": environment.get_status()
    }

@app.post("/environments/release/{env_name}")
def release_environment(env_name: str):
    environment = resources.get_environment(env_name)
    if not environment:
        raise HTTPException(status_code=404, detail=f"Environment not found: {env_name}")

    success = environment.release()
    if success:
        return {
            "success": True,
            "message": f"Environment {env_name} successfully released",
            "status": environment.get_status()
        }
    else:
        return {
            "success": False,
            "message": f"Environment {env_name} was not taken",
            "status": environment.get_status()
        }