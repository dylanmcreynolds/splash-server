import pytest
import databroker
from splash.service.runs_service import RunsService


class MockRun():

    def __init__(self, run_user_id):
        self.metadata = {
            'start': {
                'user_id': run_user_id,
                'projections': [
                    {
                        'name': 'foo',
                        'version': '1.0',
                        'configuration': 'why is this required?',
                        'projection': {
                            '/user': {
                                'type': 'linked',
                                'location': 'configuration',
                                'field': 'user_id'  # see above
                            }
                        }
                    }
                ]
            }
        }


def test_get_runs_auth(monkeypatch):
    
    catalog = {
        "run_catalog": {
                '85': MockRun('bernard_hinault'),
                '86': MockRun('greg_lemond'),
                '87': MockRun('laurent_fignon'),
                '88': MockRun('laurent_fignon'),
                '89': MockRun('greg_lemond'),
        }
    }

    runs_service = RunsService()
    # monkeypatch.setattr(runs_service, '_catalog', catalog)
    monkeypatch.setattr('splash.service.runs_service.catalog', catalog,)
    runs = runs_service.get_runs({'uid': 'greg_lemond'}, 'run_catalog')
    assert runs is not None
