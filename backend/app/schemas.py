from pydantic import BaseModel


class CameraBase(BaseModel):
    name: str
    status: str
    nvr: str
    ip: str


class CameraCreate(CameraBase):
    pass


class CameraResponse(CameraBase):
    id: int

    class Config:
        from_attributes = True