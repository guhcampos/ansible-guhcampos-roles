from pydantic import BaseModel, ConfigDict


class RoleGenerationConfig(BaseModel):
    model_config = ConfigDict(extra="allow")

    template: str
