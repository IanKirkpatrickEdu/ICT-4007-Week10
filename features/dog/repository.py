from features.dog import models as dog_models
from uuid import UUID
import json
from fastapi.encoders import jsonable_encoder
from typing import Any
from pathlib import Path

current_file_path = Path(__file__).resolve()
current_dir = current_file_path.parent
dog_db_path = current_dir / "dog_db.json"

def as_json(model: Any):
    """lazy way of forcing json.
    should really tell how you want to serialize in the pydantic model itself.
    """
    as_json_string = model.model_dump_json()
    as_json = json.loads(as_json_string)
    return as_json

class DogRepo():
    
    __slots__ = ["dog_db_table"]
    
    def __init__(self):
        self.dog_db_table = dict[str, dict[str, Any]]()
    
    async def setup(self):
        with open(dog_db_path, "r") as f:
            self.dog_db_table = json.load(f)
            
    async def teardown(self):
        with open(dog_db_path, "w") as f:
            print("DOG TABLE:", self.dog_db_table)
            json.dump(self.dog_db_table, f, indent=4)
    
    async def list(self, dog_filters: dog_models.DogFilter) -> dog_models.DogListResponse: 
        all_dogs = [dog_models.Dog.model_validate(d) for d in self.dog_db_table.values()]
        filtered_dogs = []
        filters = {}
        for dog in all_dogs:
            # ignore any dogs that dont meet our search criteria with 'continue'
            # Note: this probably isn't the most performant but eh
            if dog_filters.min_age:
                filters["min_age"] = dog_filters.min_age
                if dog.age < dog_filters.min_age:
                    continue
            if dog_filters.max_age:
                filters["max_age"] = dog_filters.max_age
                if dog.age > dog_filters.max_age:
                    continue
            if dog_filters.breed:
                filters["breed"] = dog_filters.breed
                if dog.breed not in dog_filters.breed:
                    continue
            if dog_filters.sex:
                filters["sex"] = dog_filters.sex
                if dog.sex not in dog_filters.sex:
                    continue
            if dog_filters.color:
                filters["color"] = dog_filters.color
                if dog.color not in dog_filters.color:
                    continue
            filtered_dogs.append(dog)
        return dog_models.DogListResponse(
            filters=filters,
            entities=filtered_dogs,
            entities_count=len(filtered_dogs),
            total_count=len(all_dogs),
        )

    async def get(self, id: UUID) -> dog_models.Dog | None: 
        dog = self.dog_db_table.get(str(id))
        if not dog:
            return None
        return dog_models.Dog.model_validate(dog)

    async def post(self, dog: dog_models.Dog) -> dog_models.Dog:
        self.dog_db_table[str(dog.id)] = as_json(dog)
        return dog
    
    async def put(self, new_dog: dog_models.Dog) -> dog_models.Dog:
        self.dog_db_table[str(new_dog.id)] = as_json(new_dog)
        return new_dog
    
    async def patch(self, updated_dog: dog_models.Dog) -> dog_models.Dog:
        self.dog_db_table[str(updated_dog.id)] = as_json(updated_dog)
        return updated_dog
    
    async def delete(self, id: UUID) -> UUID | None:
        # if you want to error that the dog exists you can
        #   but not erroring keeps this endpoint idempotent
        id_str = str(id)
        if self.get(id_str):
            del self.dog_db_table[id_str]
        return id
    
    async def delete_all(self) -> dict[str, dict[str, Any]]:
        # if you want to error that the dog exists you can
        #   but not erroring keeps this endpoint idempotent
        self.dog_db_table = {}
        return self.dog_db_table