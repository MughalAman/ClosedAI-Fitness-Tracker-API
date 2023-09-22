import fastapi as _fastapi
from fastapi.middleware.cors import CORSMiddleware

import fitness_api.settings as _settings
from fitness_api.core import logging as _logging
from fitness_api.core import services


_logging.check_logging_level()

app = _fastapi.FastAPI(docs_url="/", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.SETTINGS.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

services.create_database()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
