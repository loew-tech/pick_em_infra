from dataclasses import dataclass


@dataclass(slots=True)
class Option:
    name: str
    interest: str
    effort: str

    @classmethod
    def from_dict(cls, option_dict: dict):
        return cls(
            name=option_dict['name'],
            interest=option_dict['interest'],
            effort=option_dict['effort']
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
