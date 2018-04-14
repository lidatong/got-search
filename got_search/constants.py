import pkg_resources as pr


class Constants:
    DATA_PACKAGE_NAME = 'data'
    SEASON_DIR = 'season_pages'
    EP_DIR = 'ep_pages'
    RESOURCE_DIR = f'{pr.resource_filename("data", "")}'
    SEASONS_CSV = 'seasons.csv'
    EPISODES_CSV = 'episodes.csv'
    SEASON_COLNAMES = ['season', 'synopsis']
    EP_COLNAMES = ['season', 'episode', 'title', 'synopsis']
    WIKI_SOURCE = 'http://gameofthrones.wikia.com'
    MIN_SLEEP = 1
    CURR_SEASON = 7
