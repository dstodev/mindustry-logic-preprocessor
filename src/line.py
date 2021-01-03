from dataclasses import dataclass


@dataclass
class Line:
    original_number: int
    content: str
    # Only store line deltas?
