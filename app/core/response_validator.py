import json
from typing import Type, TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


def validate_response(
    response_text: str,
    output_model: Type[T],
) -> T:

    data = json.loads(response_text)

    return output_model.model_validate(data)