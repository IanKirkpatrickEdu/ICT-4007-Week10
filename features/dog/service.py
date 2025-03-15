from features.dog.repository import DogRepo
from features.dog import models as dog_models
from uuid import UUID
from loguru import logger
from fastapi import HTTPException, status
import json

class DogService():
    __slots__ = ["dog_repo"]

    def __init__(self, dog_repo: DogRepo):
        self.dog_repo = dog_repo

    async def list(self, dog_filters: dog_models.DogFilter) -> dog_models.DogListResponse: 
      return await self.dog_repo.list(dog_filters)

    async def get(self, id: UUID) -> dog_models.Dog | None: 
      return await self.dog_repo.get(id)

    async def post(self, dog: dog_models.Dog) -> dog_models.Dog:
      return await self.dog_repo.post(dog)

    async def put(self, id: UUID, new_dog: dog_models.DogCreateInput) -> dog_models.Dog:
      dog: dog_models.Dog | None = await self.get(id)
      if not dog:
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail=f"The dog you are looking to update with id={id} is not found!"
          )
      logger.info("Found dog to update (put) {}", json.loads(new_dog.model_dump_json()))
      new_dog_model = dog_models.Dog.model_validate(new_dog.model_dump())
      new_dog_model.id = id
      return await self.dog_repo.put(new_dog_model)

    async def patch(self, id: UUID, update_values: dog_models.DogUpdateInput) -> dog_models.Dog:
        dog: dog_models.Dog | None = await self.get(id)
        if not dog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The dog you are looking to update with id={id} is not found!"
            )
        logger.info("Found dog to update (patch) {}", json.loads(dog.model_dump_json()))
        update_json = update_values.model_dump(exclude_none=True)
        logger.info("Fields to update on found dog {}", update_json)
        updated_dog = dog.model_copy(update=update_json)
        return await self.dog_repo.patch(updated_dog)

    async def delete(self, id: UUID) -> UUID:
        return await self.dog_repo.delete(id)
    
    async def delete_all(self) -> dict[str, dog_models.DogBreedEnum]:
        return await self.dog_repo.delete_all()
