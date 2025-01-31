from pydantic import BaseModel, PositiveFloat, Field

class ProduitData(BaseModel):
    nom: str = Field(..., frozen=True)
    prix: PositiveFloat = Field(..., frozen=True)
    color: str = Field(..., frozen=True)


class ListeProduits(list[ProduitData]):
    pass
