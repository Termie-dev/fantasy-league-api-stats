# Only for leagues from 2021 to now

from sleeper_wrapper.league import League
from sleeper_wrapper.base_api import BaseApi
from sleeper_wrapper.user import User
from sleeper_wrapper.drafts import Drafts
from sleeper_wrapper.stats import Stats
from sleeper_wrapper.players import Players
import pandas as pd
import json
from collections import defaultdict

# Create League objects to get data from
def initialize_league_objects(league_ids):
    league_objects = []
    for league_id in league_ids:
        league = League(league_id)
        league_objects.append(league)
    return league_objects

# Create list of the users in each iteration of the league
def get_users_for_all_leagues(league_objects):
    users_for_each_league = []
    for league in league_objects:
        users_for_each_league.append(league.get_users())
    return users_for_each_league

# Create list of the rosters in each iteration of the league
def get_rosters_for_all_leagues(league_objects):
    rosters_for_each_league = []
    for league in league_objects:
        rosters_for_each_league.append(league.get_rosters())
    return rosters_for_each_league

# Create a map from someone's Sleeper name to their Sleeper ID
def map_display_names_to_user_ids(users_for_each_league):
    display_names_to_user_ids = {}
    for users in users_for_each_league:
        for user in users:
            display_names_to_user_ids[user['display_name']] = user['user_id']
    return display_names_to_user_ids

# Create a map from someone's Sleeper ID to their Sleeper name
def map_user_ids_to_display_names(display_names_to_user_ids):
    user_id_to_display_name = {user_id: display_name for display_name, user_id in display_names_to_user_ids.items()}

# Create list of all the matchups in the league to get the points scored and against who
def get_matchups_in_all_leagues(league_objects):
    all_leagues_matchups = []
    for league in league_objects:
        league_matchups = []
        for i in range(15): # 17 week season. 2002-2020 had 16 weeks. Todo in the future
            matchups = league.get_matchups(i)
            league_matchups.append(matchups)

        all_leagues_matchups.append(league_matchups)

    return all_leagues_matchups

# Create a map from a Sleeper user's edited team name to their Sleeper name
def map_team_name_to_display_name(users_for_each_league):
    team_name_to_display_name = {}
    for users in users_for_each_league:
        for user in users:
            team_name = user.get('metadata', {}).get('team_name')
            if team_name:
                team_name_to_display_name[team_name] = user['display_name']
        
    return team_name_to_display_name

# Create a map from someone's roster ID to their Sleeper name
def map_roster_id_to_user_id(rosters_for_each_league):
    roster_id_to_user_id = {}
    for rosters in rosters_for_each_league:
        for roster in rosters:
            roster_id_to_user_id[roster['roster_id']] = roster['owner_id']

    return roster_id_to_user_id

def map_roster_id_to_display_name(user_id_to_display_name, roster_id_to_user_id):
    roster_to_display_name = {roster_id: user_id_to_display_name[user_id] for roster_id, user_id in roster_id_to_user_id.items()}

