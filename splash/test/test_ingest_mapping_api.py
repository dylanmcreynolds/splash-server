import pytest

from .testing_utils import generic_test_api_crud


@pytest.mark.usefixtures("splash_client", "token_header")
def test_flask_crud_ingest_mapping(api_url_root, splash_client, token_header):
    generic_test_api_crud(new_umapping, api_url_root + "/ingest_mappings", splash_client, token_header)


new_umapping = mapping_dict = {
        'name': 'test name',
        'description': 'test descriptions',
        'version': '42',
        'resource_spec': 'MultiKeySlice',
        'metadata_mappings': {
            '/measurement/sample/name': 'dataset',
            '/measurement/instrument/name': 'end_station',
            '/measurement/instrument/source/beamline': 'beamline',
        },
        'stream_mappings': {
            "primary": {
                "time_stamp": '/process/acquisition/time_stamp',
                "mapping_fields": [
                    {'name': '/exchange/data', 'external': True},
                    {'name': '/process/acquisition/sample_position_x', 'description': 'tile_xmovedist'}
                ]
            },
            "darks": {
                "time_stamp": '/process/acquisition/time_stamp',
                "mapping_fields": [
                    {'name': '/exchange/dark', 'external': True},
                    {'name': '/process/acquisition/sample_position_x', 'description': 'tile_xmovedist'}
                ]
            }
        }
    }