import fastapi
import app as application

app = fastapi.FastAPI()
app.include_router(application.router)

