from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class ProduitData(BaseModel):
    # Forbid extra arguments and freeze the data to make it hashable (dict)
    model_config = ConfigDict(extra='forbid', frozen=True)

    nom: str = Field(...)
    prix: Decimal = Field(...)
    color: str = Field(...)
