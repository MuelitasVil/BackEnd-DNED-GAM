import re
from typing import Any

from typing import Optional, Annotated
from datetime import date
from pydantic import BaseModel, BeforeValidator


def validate_period_code(value: Any) -> str:
    regex = r"^\d{4}-(1|2)(-I)?$"
    if not isinstance(value, str) or not re.match(regex, value):
        raise ValueError(
            "cod_period debe tener el formato 'AAAA-1', 'AAAA-2', "
            "'AAAA-1-I' o 'AAAA-2-I'"
        )
    return value


class PeriodInput(BaseModel):
    cod_period: Annotated[str, BeforeValidator(validate_period_code)]
    initial_date: Optional[date] = None
    final_date: Optional[date] = None
    description: Optional[str] = None
