import pytest
from splash.data.base import MongoCollectionDao


@pytest.mark.usefixture("mongodb")
def test_retrieve_paged(mongodb):
    data = [
        {"user": {"uid": "42_0", "name": "zaphod", "job": "president"}},
        {"user": {"uid": "42_1", "name": "trillian", "job": "captain"}},
        {"user": {"uid": "42_2", "name": "slartibartfast", "job": "architect"}},
        {"user": {"uid": "42_3", "name": "ford", "job": "hitchhiker"}},
        {"user": {"uid": "42_4", "name": "arthur", "job": "hitchhiker"}},
        {"user": {"uid": "42_5", "name": "hiker", "job": "hitchhiker"}}
    ]

    dao = MongoCollectionDao(mongodb, 'characters')
    for character in data:
        dao.create(character)

    return_data = list(dao.retrieve_paged(0))
    assert len(return_data) == len(data)

    # with a query
    return_data = list(dao.retrieve_paged(query={"user.uid": "42_0"}))
    assert len(return_data) == 1
    assert return_data[0]['user']['name'] == "zaphod"

    # with query and a page_size
    return_data = list(dao.retrieve_paged(0, query={"user.job": "hitchhiker"}, limit=2))
    assert len(return_data) == 2
    assert return_data[0]['user']['job'] == "hitchhiker"
