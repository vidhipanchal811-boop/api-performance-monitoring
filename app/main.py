from fastapi import FastAPI

app = FastAPI(
    title="API Performance Monitoring System",
    description="REST API for performance testing and deployment monitoring",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "API Performance Monitoring System is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/users")
def get_users():
    return [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com"
        },
        {
            "id": 2,
            "name": "Bob",
            "email": "bob@example.com"
        }
    ]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }