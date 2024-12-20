from pydantic import BaseModel
from typing import Dict, Any

class ImageData(BaseModel):
    image: str
    dict_of_vars: Dict[str, Any] = {}
