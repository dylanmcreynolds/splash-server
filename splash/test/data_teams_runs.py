from typing import List
from pydantic import parse_obj_as
from splash.models.teams import Team
from splash.models.users import UserModel

class MockRun():

    def __init__(self, run_user_id, team):
        self.metadata = {
            'start': {
                'user_id': run_user_id,
                'team': team,
                'projections': [
                    {
                        'name': 'foo',
                        'version': '1.0',
                        'configuration': 'why is this required?',
                        'projection': {
                            '/team_id': {
                                'type': 'linked',
                                'location': 'configuration',
                                'field': 'user_id'  # see above
                            }
                        }
                    }
                ]
            }
        }


catalog = {
    "tour_winners": {
            '85': MockRun('bernard_hinault', 'la_vie_claire'),
            # same team as hinault...for now
            '86': MockRun('greg_lemond', 'la_vie_claire'),
            '87': MockRun('stephen_roche', 'carrera'),
            '88': MockRun('pedro_delgado', 'cafe_de_columbia'),
            # lemond came back with different team, like a grad student in a different lab
            '89': MockRun('greg_lemond', 'ADR')
    }
}

teams_raw = [
    {
        'name': 'la_vie_claire',
        'members': {
            'lemond': ['member', 'leader'],
            'hinault': ['member', 'leader', 'owner'],
            'hampsten': ['member'],
        }
    }
]

teams = parse_obj_as(List[Team], teams_raw)


lemond = {
        'uid': 'lemond',
        'given_name': 'greg',
        'family_name': 'lemond',
        'email': 'greg@lemond.io',
        'authenticators': [
            {
                'issuer': 'aso',
                'email': 'greg@aso.com',
                'subject': 'randomsubject'
            }
        ]
    }

hinault = {
        'uid': 'hinault',
        'given_name': 'bernard',
        'family_name': 'hinault',
        'email': 'bernard@hinault.io',
        'authenticators': [
            {
                'issuer': 'aso',
                'email': 'bernard@aso.com',
                'subject': 'badger'
            }
        ]
    }
hampsten = {
        'uid': 'hampsten',
        'given_name': 'andy',
        'family_name': 'hampsten',
        'email': 'andy@ahmptsten.io',
        'authenticators': [
            {
                'issuer': 'aso',
                'email': 'andy@aso.com',
                'subject': 'alpduez'
            }
        ]
    }
fignon = {
        'uid': 'fignon',
        'given_name': 'lalurent',
        'family_name': 'fignon',
        'email': 'laurent@fignon.com',
        'authenticators': [
            {
                'issuer': 'aso',
                'email': 'laurent@aso.com',
                'subject': 'glasses'
            }
        ]
    }

user_leader = parse_obj_as(UserModel, lemond)
user_owner = parse_obj_as(UserModel, hinault)
user_team = parse_obj_as(UserModel, hampsten)
user_other_team = parse_obj_as(UserModel, fignon)
