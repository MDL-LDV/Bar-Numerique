from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, List

class ProduitData(BaseModel):
    # Forbid extra arguments and freeze the data to make it hashable (dict)
    model_config = ConfigDict(extra='forbid', frozen=True)

    id_produit: int = Field(...)
    nom: str = Field(...)
    prix: Decimal = Field(...)
    image: Optional[bytes] = Field(bytes())
    color: str = Field(...)


class CommandeData(BaseModel):
    # Forbid extra arguments and freeze the data to make it hashable (dict)
    model_config = ConfigDict(extra='forbid', frozen=True)
    
    id_commande: int = Field(...)
    date: int = Field(...)
    heure: int = Field(...)
    total: Decimal = Field(...)
