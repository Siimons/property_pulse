from pydantic import BaseModel, Field
from typing import List, Optional

class ListingBase(BaseModel):
    title: str = Field(..., description="Заголовок объявления")
    description: str = Field(..., description="Описание объявления")
    price: float = Field(..., description="Цена объявления")
    location: str = Field(..., description="Местоположение объекта")
    url: Optional[str] = Field(None, description="Ссылка на объявление")

class ListingCreate(ListingBase):
    pass

class ListingUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Заголовок объявления")
    description: Optional[str] = Field(None, description="Описание объявления")
    price: Optional[float] = Field(None, description="Цена объявления")
    location: Optional[str] = Field(None, description="Местоположение объекта")
    url: Optional[str] = Field(None, description="Ссылка на объявление")

class Listing(ListingBase):
    id: int = Field(..., description="Идентификатор объявления")

    class Config:
        orm_mode = True

class ListingsResponse(BaseModel):
    listings: List[Listing] = Field(..., description="Список объявлений")
