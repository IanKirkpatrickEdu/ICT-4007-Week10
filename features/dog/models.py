from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query
from enum import Enum
from uuid import uuid4, UUID
import datetime

class DogBreedEnum(str, Enum):
    LABRADOR = 'Labrador Retriever'
    BEAGLE = 'Beagle'
    BULLDOG = 'Bulldog'
    POODLE = 'Poodle'
    GERMAN_SHEPARD = 'German Shepherd'

class MixinModelDefaults:
    """Entity Creation Bookeeping Mixin."""
    # default factory will create an id if one does not exist
    id: UUID = Field(default_factory=lambda: uuid4())
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    class Config:
        json_encoders = {
            UUID: str,  # This will convert UUID to a string when calling model_dump()
            datetime.datetime: str
        }

default_config_dict = ConfigDict(
    extra='forbid',  # error if fields not defined below are provided
    str_strip_whitespace=True,  # trims extra whitespace to left/right of every input in model
    str_max_length = 255,  # longest any string can be
    use_enum_values=True
)

class DogSexEnum(str, Enum):
    """Sex of the dog using shorthand."""
    MALE="m"
    FEMALE="f"
    SPAYED="s"
    NEUTERED="n"
    UNKNOWN="u"


class Dog(BaseModel, MixinModelDefaults):
    model_config = default_config_dict # pydantic model settings
    # fields
    name: str
    breed: DogBreedEnum
    color: str = Field(min_length=1, max_length=20)
    age: int = Field(min=0, max=30)
    sex: DogSexEnum 
    description: str | None = None # using default max length from model_config

class DogCreateInput(BaseModel):
    model_config = default_config_dict # pydantic model settings
    # fields
    name: str
    breed: DogBreedEnum
    color: str = Field(min_length=1, max_length=20)
    age: int = Field(min=0, max=30)
    sex: DogSexEnum 
    description: str | None = None # using default max length from model_config

class DogUpdateInput(BaseModel):
    """Similar to the create model but all fields are optional."""
    model_config = default_config_dict # pydantic model settings
    # fields
    name: str | None = None
    breed: DogBreedEnum | None = None
    color: str | None = Field(default=None, min_length=1, max_length=20)
    age: int | None = Field(default=None,min=0, max=30)
    sex: DogSexEnum | None = Field(default=None)
    description: str | None = None # using default max length from model_config

class DogFilter(BaseModel):
    breed: list[DogBreedEnum] | None = Field(Query([]))
    min_age: int | None = Field(Query(None), min=0)
    max_age: int | None = Field(Query(None), max=30)
    color: list[str] | None = Field(Query([]))
    sex: list[DogSexEnum] | None = Field(Query([]))

class DogListResponse(BaseModel):
    filters: dict
    entities: list[Dog]
    entities_count: int
    total_count: int
