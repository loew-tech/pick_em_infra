from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class Option:
    name: str
    interest: str
    effort: str
    category_id: str
    created_at: datetime

    @classmethod
    def from_dict(cls, option_dict: dict):
        created_at_str = option_dict['created_at']
        clean_str = created_at_str.replace("Z", "+00:00")
        created_at_dt = datetime.fromisoformat(clean_str)
        return cls(
            name=option_dict['name'],
            interest=option_dict['interest'],
            effort=option_dict['effort'],
            category_id=option_dict['category_id'],
            created_at=created_at_dt
        )


@dataclass(slots=True)
class Category:
    name: str
    choices: list[Option]

    @classmethod
    def from_dict(cls, category_dict: dict):
        return cls(
            name=category_dict['name'],
            choices=[Option.from_dict(option_dict) for option_dict in category_dict['choices']],
        )
