import re
from itertools import product
from typing import List


def extract_snippet(s: str, start_pattern: str, end_pattern: str):
    """
    Extracts a snippet from a string `s` that starts immediately after
    start_pattern and ends immediately before end_pattern.

    Returns an empty string if either start or end pattern is not found.
    """
    try:
        start = s.index(start_pattern) + len(start_pattern)
        end = s[start:].index(end_pattern) + start
    except ValueError:
        return ""
    else:
        return s[start:end]


def extract_snippet_with_fallbacks(s: str,
                                   *,
                                   start_patterns: List[str],
                                   end_patterns: List[str]):
    """
    Extract a snippet, falling back on alternative start and end patterns if
    there is no match.
    """
    for start_pattern, end_pattern in product(start_patterns, end_patterns):
        snippet = extract_snippet(s, start_pattern, end_pattern)
        if snippet:
            return snippet
    return ""


def html_to_str(html):
    html = re.sub('<[^<]+?>', '', html)
    html = re.sub('[\t\r\f\v]', '', html)
    html = re.sub('  +', '', html)
    html = re.sub('\n+', ' ', html)
    return html.strip().replace('\n', ' ')