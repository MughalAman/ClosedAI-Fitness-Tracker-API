from fastapi.testclient import TestClient
import fastapi as _fastapi
from fastapi.middleware.cors import CORSMiddleware

import fitness_api.settings as _settings
from fitness_api.routes import token, user, friendship, exercise, workout, rating, tag

app = _fastapi.FastAPI(docs_url="/", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.SETTINGS.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token.router)
app.include_router(user.router)
app.include_router(friendship.router)
app.include_router(exercise.router)
app.include_router(workout.router)
app.include_router(rating.router)
app.include_router(tag.router)

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/user/",
        json={
            "name": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "height": 180,
            "weight": 80,
            "gender": "MALE",
            "birth_date": "1990-01-01"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "user_id" in data


def test_read_user_with_id():
    # assuming there is a user with id 1
    response = client.get("/user/1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
