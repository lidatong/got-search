"""
crawler.py

Html parsing is super hacky and assuming of text and structure.
"""

import re
import csv

import pkg_resources as pr

from got_search.utils.http_client import HttpClient
from got_search.constants import Constants

from got_search.utils.parser import (extract_snippet,
                                     extract_snippet_with_fallbacks,
                                     html_to_str)

client = HttpClient(Constants.WIKI_SOURCE, 'wiki')


def parse_ep_titles_from_season_page(html):
    ep_li_pattern = '<td> "<a href="/wiki/'
    ep_title_pattern = 'title="'
    for i, match in enumerate(re.finditer(ep_li_pattern, html), start=1):
        yield i, extract_snippet(html[match.end():], ep_title_pattern, '"')


def parse_synopsis_from_season_page(html):
    start_patterns = [
        '<h2><span class="mw-headline" id="Plot">Plot</span></h2>'
    ]
    end_patterns = [
        '<h2><span class="mw-headline" id="Video_recap">Video recap</span></h2>',
        '<h2><span class="mw-headline" id="Production">Production</span></h2>'
    ]
    synopsis = extract_snippet_with_fallbacks(html,
                                              start_patterns=start_patterns,
                                              end_patterns=end_patterns)
    return html_to_str(synopsis)


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
    for season_num in range(1, Constants.CURR_SEASON + 1):
        season_title = f'Season_{season_num}'
        season_page = client.get(season_title)
        season_path = f'{Constants.RESOURCE_DIR}/season_pages/{season_title}'
        with open(season_path, 'w') as fp:
            fp.write(season_page)

        for ep_num, ep_title in parse_ep_titles_from_season_page(season_page):
            ep_page = client.get(ep_title)
            ep_path = f'{Constants.RESOURCE_DIR}/ep_pages/{season_num}/{ep_num} - {ep_title}'
            with open(ep_path, 'w') as fp:
                fp.write(ep_page)


def persist_seasons_as_csv():
    csvname = pr.resource_filename(Constants.DATA_PACKAGE_NAME,
                                   Constants.SEASONS_CSV)
    with open(csvname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=Constants.SEASON_COLNAMES)
        writer.writeheader()
        for season_page_title in pr.resource_listdir(Constants.DATA_PACKAGE_NAME,
                                                     Constants.SEASON_DIR):
            _, season_num = season_page_title.split("_")
            season_page = pr.resource_string(Constants.DATA_PACKAGE_NAME,
                                             f'{Constants.SEASON_DIR}/{season_page_title}')
            season_html = season_page.decode('utf-8')
            synopsis = parse_synopsis_from_season_page(season_html)
            writer.writerow({"season": int(season_num),
                             "synopsis": synopsis})


def persist_episodes_as_csv():
    csvname = pr.resource_filename(Constants.DATA_PACKAGE_NAME,
                                   Constants.EPISODES_CSV)
    with open(csvname, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=Constants.EP_COLNAMES)
        writer.writeheader()
        for season in pr.resource_listdir(Constants.DATA_PACKAGE_NAME,
                                          Constants.EP_DIR):
            dir_path = f'{Constants.EP_DIR}/{season}'
            for ep in pr.resource_listdir(Constants.DATA_PACKAGE_NAME, dir_path):
                ep_num, ep_title = [s.strip() for s in ep.split("-")]
                path = f'{dir_path}/{ep}'
                ep_page = pr.resource_string(Constants.DATA_PACKAGE_NAME, path)
                synopsis = parse_synopsis_from_ep_page(ep_page.decode('utf-8'))
                writer.writerow({"season": int(season),
                                 "episode": int(ep_num),
                                 "title": ep_title,
                                 "synopsis": synopsis})


def persist_documents():
    persist_seasons_as_csv()
    persist_episodes_as_csv()


def main():
    persist_documents()


if __name__ == '__main__':
    main()
