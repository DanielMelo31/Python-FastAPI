from typing import Any
from pydantic import BaseModel, validator
from pydantic.utils import GetterDict
from peewee import ModelSelect


# Convert object to dict
class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default:Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res

class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

# ---------------User---------------

class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('La longitud del nombre de usuario debe estar entre 3 y 50 caracteres')
        
        return username

# Object validated reponse
class UserResponseModel(ResponseModel):
    id: int
    username: str

# ---------------Movies---------------
class MovieResponseModel(ResponseModel):
    id: int
    title: str


# ---------------Review---------------

class ReviewValidator():
    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('Porfavor puntue la pelicula con valores de 1 a 5 puntos')

        return score

class ReviewRequestModel(BaseModel, ReviewValidator):
    user_id: int
    movies_id: int
    review: str
    score: int

class ReviewResponseModel(ResponseModel):
    id: int
    user: UserResponseModel
    movies: MovieResponseModel
    review: str
    score: int

class ReviewRequestPutModel(BaseModel, ReviewValidator):
    review: str
    score: int
    
    
