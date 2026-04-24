
from pydantic import BaseModel

from schemas.action import Action


class StepResponse(BaseModel):
    action: Action
    old_state_idx: int
