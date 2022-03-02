import re
from typing import List


def get_hashtags(text: str) -> List[str]:
    if len(text) == 0:
        return []

    hashtag_regex = re.compile(r"(?:#)(\w(?:(?:\w|(?:\.(?!\.))){0,28}(?:\w))?)")
    return re.findall(hashtag_regex, text.lower())


def get_mentions(text: str) -> List[str]:
    if len(text) == 0:
        return []

    mention_regex = re.compile(r"(?:^|\W|_)(?:@)(\w(?:(?:\w|(?:\.(?!\.))){0,28}(?:\w))?)")
    return re.findall(mention_regex, text.lower())
