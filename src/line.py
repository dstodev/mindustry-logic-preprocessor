from dataclasses import dataclass


@dataclass
class Line:
    original_number: int
    original_content: str
    content: str
    elide: bool
    # Only store line deltas?
