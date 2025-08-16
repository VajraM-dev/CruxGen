from typing import Any, Optional
from pydantic import BaseModel

class OutputResponse(BaseModel):
    """
    A generic Pydantic model for standardized API responses.
    
    This class provides a consistent structure for success and error
    responses, with a flexible data payload field.
    """
    success: bool = True
    message: str = "Operation successful."
    output: Optional[Any] = None