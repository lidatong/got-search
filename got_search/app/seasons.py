import csv
from functools import lru_cache

import pkg_resources as pr
from flask import Blueprint, abort, render_template

from got_search.constants import Constants
from got_search.entities import Season
from got_search.utils.itertools2 import find

seasons = Blueprint('seasons', __name__)


@seasons.route('/seasons')
def index():
    return render_template('seasons.html', seasons=get_seasons())


@seasons.route('/seasons/<int:season_num>')
def show(season_num):
    season = find_season_or_abort(season_num)
    return render_template('season.html', season=season)


@lru_cache()
def get_seasons():
    seasons_csv = pr.resource_filename(Constants.DATA_PACKAGE_NAME,
                                       f'{Constants.SEASONS_CSV}')
    with open(seasons_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        return {Season(num=int(row['season']), synopsis=row['synopsis'])
                for row in reader}


def find_season_or_abort(season_num):
    season = find(get_seasons(), key=lambda season: season.num == season_num)
    if season is None:
        return abort(404)
    return season
