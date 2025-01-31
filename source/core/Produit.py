from pydantic import BaseModel, PositiveFloat, Field, ConfigDict

class ProduitData(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    nom: str = Field(...)
    prix: PositiveFloat = Field(...)
    color: str = Field(...)
