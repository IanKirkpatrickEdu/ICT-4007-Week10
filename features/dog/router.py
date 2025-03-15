"""Example routes for learning general FastAPI inputs/outputs

CRUD Example

Note: this api will reset the dog_kennel when you restart the API
    the data in there is not persisted in a real database
"""
from fastapi import APIRouter, status, HTTPException, Body, Depends
from loguru import logger
from uuid import UUID
from features.dog import models as dog_models
from features.dog.singletons import DogServiceDependency
import json

router = APIRouter()


@router.post("/dogs")
async def post_dog(
    dog_service: DogServiceDependency,
    new_dog: dog_models.DogCreateInput = Body(),
) -> dog_models.Dog:
    """Create a dog!"""
    try:
        dog = dog_models.Dog.model_validate(new_dog.model_dump())
        new_dog = await dog_service.post(dog)
        return new_dog.model_dump()
    except Exception as e:
        logger.error("Error processing a: {}", str(e))
        raise e

@router.get("/dogs")
async def get_dogs(
    dog_service: DogServiceDependency,
    filters: dog_models.DogFilter = Depends()
) -> dog_models.DogListResponse:
    """Returns all dogs!"""
    try:
        logger.info("filters: {}", filters.model_dump)
        dog_list_response = await dog_service.list(filters)
        return dog_list_response
    except Exception as e:
        logger.error("Error processing a: {}", str(e))
        raise e

@router.get("/dogs/{dog_id}")
async def get_dog(
    dog_service: DogServiceDependency,
    dog_id: UUID
) -> dog_models.Dog:
    """Returns a single dog by ID!"""
    try:
        dog = await dog_service.get(dog_id)
        logger.info(dog)
        if not dog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The dog you are looking for with id={dog_id} is not found!"
            )
        return dog.model_dump()
    except Exception as e:
        logger.error("Error processing a: {}", str(e))
        raise e

@router.put("/dogs/{dog_id}")
async def put_dog(
    dog_service: DogServiceDependency,
    dog_id: UUID, 
    new_dog: dog_models.DogCreateInput = Body()
) -> dog_models.Dog:
    """Update a dog by ID!"""
    try:
        updated_dog =  await dog_service.put(dog_id, new_dog)
        return updated_dog.model_dump()
    except Exception as e:
        logger.error("Error processing a: {}", str(e))
        raise e
    

@router.patch("/dogs/{dog_id}")
async def patch_dog(
    dog_service: DogServiceDependency,
    dog_id: UUID, 
    dog_update_values: dog_models.DogUpdateInput = Body()
) -> dog_models.Dog:
    """Update a dog by ID!"""
    try:
        updated_dog = await dog_service.patch(dog_id, dog_update_values)
        return updated_dog.model_dump()            
    except Exception as e:
        logger.error("Error processing a: {}", str(e))
        raise e
    
@router.delete("/dogs/{dog_id}")
async def delete_dog(
    dog_service: DogServiceDependency,
    dog_id: UUID, 
) -> str:
    """Delete a dog by ID!"""
    try:
        return str(await dog_service.delete(dog_id))
    except Exception as e:
        logger.error("Error processing a: {}", str(e))
        raise e
    
@router.delete("/dogs")
async def delete_dogs(
    dog_service: DogServiceDependency,
) -> dict:
    """Delete a dog by ID!"""
    try:
        return await dog_service.delete_all()
    except Exception as e:
        logger.error("Error processing a: {}", str(e))
        raise e