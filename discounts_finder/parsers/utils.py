import re
from decimal import Decimal
from typing import List, Tuple


def remove_letters(text: str) -> str:
    return re.sub(r"[^\d.,]", "", text)


def price_text_to_decimal(text: str) -> Decimal:
    return remove_letters(text).replace(",", ".")


def get_matching_text(text_samples: List[str], pattern: str) -> List[Tuple[int, str]]:
    matches = [re.match(pattern, text_sample) for text_sample in text_samples]
    matched_text = [
        (index, match.group(0)) for index, match in enumerate(matches) if match
    ]
    return matched_text
