import pkg_resources as pr


class Config:
    PACKAGE_NAME = 'data'
    SEASON_DIR = 'season_pages'
    EP_DIR = 'ep_pages'
    RESOURCE_DIR = f'{pr.resource_filename("data", "")}'
    SYNOPSES_FILENAME = 'synopses.csv'
    COLNAMES = ['season', 'episode', 'title', 'synopsis']
    WIKI_SOURCE = 'http://gameofthrones.wikia.com'
    MIN_SLEEP = 1
    CURR_SEASON = 7
