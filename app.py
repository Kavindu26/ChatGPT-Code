from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Pet Store API")


class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Pet(BaseModel):
    id: Optional[int] = None
    name: str
    category: Optional[Category] = None
    photoUrls: List[str]
    tags: Optional[List[Tag]] = None
    status: Optional[str] = None


# In-memory storage for pets
pets: dict[int, Pet] = {}


@app.post("/pet", response_model=Pet)
def add_pet(pet: Pet) -> Pet:
    """Add a new pet to the store."""
    if pet.id is None:
        raise HTTPException(status_code=400, detail="Pet id required")
    pets[pet.id] = pet
    return pet


@app.put("/pet", response_model=Pet)
def update_pet(pet: Pet) -> Pet:
    """Update an existing pet."""
    if pet.id is None or pet.id not in pets:
        raise HTTPException(status_code=404, detail="Pet not found")
    pets[pet.id] = pet
    return pet


@app.get("/pet/{pet_id}", response_model=Pet)
def get_pet(pet_id: int) -> Pet:
    """Return a pet by ID."""
    if pet_id not in pets:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pets[pet_id]


@app.delete("/pet/{pet_id}")
def delete_pet(pet_id: int) -> dict:
    """Delete a pet by ID."""
    if pet_id not in pets:
        raise HTTPException(status_code=404, detail="Pet not found")
    del pets[pet_id]
    return {"message": "Pet deleted"}
