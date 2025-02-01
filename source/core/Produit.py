from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class ProduitData(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    nom: str = Field(...)
    prix: Decimal = Field(...)
    color: str = Field(...)
