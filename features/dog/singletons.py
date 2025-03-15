
from features.dog.repository import DogRepo
from features.dog.service import DogService
from typing import Annotated
from fastapi import Depends
from functools import lru_cache

@lru_cache
def get_dog_service() -> DogService:
    dog_repo = DogRepo()
    dog_service = DogService(dog_repo)
    return dog_service

DogServiceDependency = Annotated[DogService, Depends(get_dog_service)]
