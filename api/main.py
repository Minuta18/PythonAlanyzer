import fastapi
import app as application
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()
app.include_router(application.router)

origins = [
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8000/api/v1'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
