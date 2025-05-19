from pydantic import BaseModel
from typing import Any, Optional

class BaseResponse(BaseModel):
    status_code: Optional[int] = 0
    error_description: Optional[str]
    data: Optional[Any] = None

    
    
