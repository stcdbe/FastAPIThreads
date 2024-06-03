from pydantic import UUID4, BaseModel, ConfigDict


class FromAttrsBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GUIDMixin(BaseModel):
    guid: UUID4


class Message(BaseModel):
    message: str
