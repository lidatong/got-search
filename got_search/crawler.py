"""
crawler.py

Html parsing is super hacky and assuming of text and structure.
"""

import re
import csv
import os

import pkg_resources as pr

from itertools import product
from typing import List
from got_search.http_client import HttpClient
from got_search.config import Config

client = HttpClient(Config.WIKI_SOURCE, 'wiki')


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


def parse_ep_titles_from_season_page(html):
    ep_li_pattern = '<td> "<a href="/wiki/'
    ep_title_pattern = 'title="'
    for i, match in enumerate(re.finditer(ep_li_pattern, html), start=1):
        yield i, extract_snippet(html[match.end():], ep_title_pattern, '"')


def parse_synopsis_from_ep_page(html):
    start_patterns = [
        '<h2><span class="mw-headline" id="Summary">Summary</span></h2>',
        '<h2><span class="mw-headline" id="Summary"> Summary </span></h2>',
        '<h2><span class="mw-headline" id="Synopsis">Synopsis</span></h2>'
    ]
    end_patterns = [
        '<h2><span class="mw-headline" id="Recap">Recap</span></h2>',
        '<h2><span class="mw-headline" id="Appearances"> Appearances </span></h2>',
        '<h2><span class="mw-headline" id="Appearances">Appearances</span></h2>'
    ]
    synopsis = extract_snippet_with_fallbacks(html,
                                              start_patterns=start_patterns,
                                              end_patterns=end_patterns)
    return html_to_str(synopsis)


def crawl_season_and_ep_pages():
    for season_num in range(1, Config.CURR_SEASON + 1):
        season_title = f'Season_{season_num}'
        season_page = client.get(season_title)
        season_path = f'{Config.RESOURCE_DIR}/season_pages/{season_title}'
        with open(season_path, 'w') as fp:
            fp.write(season_page)

        for ep_num, ep_title in parse_ep_titles_from_season_page(season_page):
            ep_page = client.get(ep_title)
            ep_path = f'{Config.RESOURCE_DIR}/ep_pages/{season_num}/{ep_num} - {ep_title}'
            with open(ep_path, 'w') as fp:
                fp.write(ep_page)


def persist_documents():
    csvname = pr.resource_filename(Config.PACKAGE_NAME,
                                   Config.SYNOPSES_FILENAME)
    with open(csvname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=Config.COLNAMES)
        writer.writeheader()

        for season in pr.resource_listdir(Config.PACKAGE_NAME, Config.EP_DIR):
            dir_path = f'{Config.EP_DIR}/{season}'
            for ep in pr.resource_listdir(Config.PACKAGE_NAME, dir_path):
                ep_num, ep_title = [s.strip() for s in ep.split("-")]
                path = f'{dir_path}/{ep}'
                ep_page = pr.resource_string(Config.PACKAGE_NAME, path)
                synopsis = parse_synopsis_from_ep_page(ep_page.decode('utf-8'))
                writer.writerow({"season": int(season),
                                 "episode": int(ep_num),
                                 "title": ep_title,
                                 "synopsis": synopsis})


def main():
    persist_documents()


if __name__ == '__main__':
    main()
