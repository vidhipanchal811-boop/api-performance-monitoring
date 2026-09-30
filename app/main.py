from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr


app = FastAPI(
    title="API Performance Monitoring System",
    description="REST API for performance testing and deployment monitoring",
    version="1.0.0"
)


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class User(UserCreate):
    id: int


users = [
    User(
        id=1,
        name="Alice",
        email="alice@example.com"
    ),
    User(
        id=2,
        name="Bob",
        email="bob@example.com"
    )
]


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
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@app.post(
    "/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):
    new_id = max(user.id for user in users) + 1 if users else 1

    new_user = User(
        id=new_id,
        name=user.name,
        email=user.email
    )

    users.append(new_user)

    return new_user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: UserCreate):
    for index, user in enumerate(users):
        if user.id == user_id:
            updated = User(
                id=user_id,
                name=updated_user.name,
                email=updated_user.email
            )

            users[index] = updated

            return updated

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)

            return {
                "message": "User deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )