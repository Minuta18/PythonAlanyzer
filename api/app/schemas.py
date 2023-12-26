import pydantic

class CreateTaskSchema(pydantic.BaseModel):
    code: str
