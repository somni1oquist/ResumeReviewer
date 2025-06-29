from dataclasses import dataclass, field
from typing import Annotated, Optional
from langgraph.graph.message import add_messages
import operator


def merge_dicts(a: dict, b: dict) -> dict:
    """Merges two dicts, with values from b overwriting a on key conflicts."""
    merged = dict(a)  # make a copy to avoid mutation
    merged.update(b)
    return merged

def safe_concat(a: str | None, b: str | None) -> str:
    return (a or "") + (b or "")


@dataclass
class ReviewState:
    resume: Annotated[dict, merge_dicts] = field(default_factory=dict)
    job: Annotated[dict, merge_dicts] = field(default_factory=dict)
    messages: Annotated[list, add_messages] = field(default_factory=list)
    report: Annotated[str, safe_concat] = field(default="")
    accepted: Annotated[bool, operator.or_] = field(default=False)
    has_error: Annotated[bool, operator.or_] = field(default=False)
