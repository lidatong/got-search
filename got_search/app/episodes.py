import csv
from collections import defaultdict
from functools import lru_cache
from operator import attrgetter

import pkg_resources as pr
from flask import Blueprint, abort, render_template

from got_search.app.seasons import find_season_or_abort, get_seasons
from got_search.constants import Constants
from got_search.entities import Episode
from got_search.utils.itertools2 import find, grouper

episodes = Blueprint('episodes', __name__)


@episodes.route('/episodes')
def base_index():
    return render_season_and_episodes('Episodes')


@episodes.route('/seasons/<int:season_num>/episodes')
def index(season_num):
    season = find_season_or_abort(season_num)
    eps = [ep for ep in get_episodes() if ep.season == season]
    return render_template('episodes.html',
                           season=season,
                           episodes=eps)


@episodes.route('/seasons/<int:season_num>/episodes/<int:episode_num>')
def show(season_num, episode_num):
    def pred(ep):
        return ep.season.num == season_num and ep.num == episode_num

    season = find_season_or_abort(season_num)
    episode = find(get_episodes(), key=pred)
    return render_template('episode.html',
                           season=season,
                           episode=episode)


@lru_cache()
def get_episodes():
    nums_to_seasons = {season.num: season for season in get_seasons()}
    episodes_csv = pr.resource_filename(Constants.DATA_PACKAGE_NAME,
                                        f'{Constants.EPISODES_CSV}')
    with open(episodes_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        return {Episode(num=int(row['episode']),
                        title=row['title'],
                        synopsis=row['synopsis'],
                        season=nums_to_seasons[int(row['season'])])
                for row in reader}


def render_season_and_episodes(heading):
    episodes = get_episodes()
    episodes_by_season = defaultdict(list)
    for episode in episodes:
        episodes_by_season[episode.season].append(episode)
    seasons = sorted(episodes_by_season.keys(), key=attrgetter('num'))
    season_groups = grouper(seasons, 5)
    return render_template('index.html',
                           episodes_by_season=episodes_by_season,
                           season_groups=season_groups,
                           heading=heading)
