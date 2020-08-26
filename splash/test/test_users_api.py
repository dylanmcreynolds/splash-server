import pytest
from ..models.users import NewUserModel
from .testing_utils import generic_test_api_crud


@pytest.mark.usefixtures("splash_client", "token_header")
def test_api_crud_user(api_url_root, splash_client, token_header):
    generic_test_api_crud(new_user, api_url_root + "/users", splash_client, token_header)


def test_api_search_user(api_url_root, splash_client, token_header):
    response = splash_client.get(api_url_root + "/users", headers=token_header, params={"user": "tricia"})
    assert response.status_code == 200, f"{response.status_code}: response is {response.content}"
    response_dict = response.json()
    assert len(response_dict) > 0


new_user_dict = {
    "given_name": "tricia",
    "family_name": "mcmillan",
    "email": "trillian@heartofgold.improbable",
    "authenticators": [
        {"issuer": "accounts.google.com",
         "subject": "dsfsdsdfsdfsdfsdfsdf",
         "email": "trillian@hearfofconld.improbable"}
    ]
}
new_user = NewUserModel(**new_user_dict)
