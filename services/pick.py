from collections import namedtuple
from random import randint

from database.constants import TIERS, WEIGHTS
from database.models import Category

SelectionOption = namedtuple('Option', ['name', 'start', 'weight', 'category'])


def pick(categories: list[Category], interest, effort) -> SelectionOption:
    options = _get_options(categories, interest, effort)
    return _pick_item(options)


def _get_options(categories: list[Category], interest, effort: str) -> list[SelectionOption]:
    i = {*TIERS[TIERS.index(interest):]}
    e = {*TIERS[:TIERS.index(effort) + 1]}
    options = []
    for c in categories:
        for o in c.choices:
            if o.effort not in e or o.interest not in i:
                continue
            start = options[-1].start + options[-1].weight if options else 0
            # @TODO: is this how I want to handle interest < effort
            wght = max(1, WEIGHTS[o.interest] // WEIGHTS[o.effort])
            options.append(SelectionOption(name=o.name, start=start, weight=wght,
                                           category=c))
    return options


def _pick_item(options: list[SelectionOption]) -> SelectionOption:
    start, stop = 0, len(options) - 1
    selection = randint(start, options[-1].start + options[-1].weight - 1)
    while start <= stop:
        mid = (start + stop) // 2
        end = options[mid].start + options[mid].weight
        if options[mid].start <= selection < end:
            return options[mid]
        elif end <= selection:
            start = mid + 1
        else:
            stop = mid - 1
    return SelectionOption(
        name='NOT FOUND', start=-1, weight=-1, category='NOT FOUND'
    )
