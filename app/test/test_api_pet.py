import pytest
import requests

URL = 'https://petstore.swagger.io/v2/'
ID_USUARIO = 4781678
STATUS_CODE_EXPECTED = 200


@pytest.fixture
def user():
    return {
        "id": 4781678,
        "username": "Isaac",
        "firstName": "Batata",
        "lastName": "Frita",
        "email": "admin@admin",
        "password": "batata456",
        "phone": "11999999999",
        "userStatus": 0
    }


# Para o correto teste é nescessario o uso da biblioteca pytest-order parar executar na ordem correta
@pytest.mark.order(1)
def test_store_user(user):

    request = requests.post(f'{URL}user', json=user)

    assert request.status_code == STATUS_CODE_EXPECTED


@pytest.mark.order(2)
def test_get_user():
    user_name = 'Isaac'
    email_expected = 'admin@admin'
    first_name_expected = 'Batata'

    request = requests.get(f'{URL}user/{user_name}')
    json = request.json()

    assert request.status_code == STATUS_CODE_EXPECTED
    assert json['id'] == ID_USUARIO
    assert json['username'] == user_name
    assert json['firstName'] == first_name_expected
    assert json['email'] == email_expected


@pytest.mark.order(3)
def test_find_and_test_login():
    user_name = 'Isaac'
    token = login(user_name, find_user_get_password(user_name))


@pytest.mark.order(5)
def test_delete_user():

    user_name = 'Testinho'
    response = requests.delete(url=f'{URL}user/{user_name}')
    json = response.json()

    assert response.status_code == STATUS_CODE_EXPECTED
    assert json['code'] == STATUS_CODE_EXPECTED
    assert json['message'] == user_name


@pytest.mark.order(4)
def test_update_user(user):
    user_name = 'Testinho'

    user['username'] = user_name

    response = requests.put(url=f'{URL}user/{user_name}', json=user)
    json = response.json()

    assert response.status_code == STATUS_CODE_EXPECTED
    assert json['code'] == STATUS_CODE_EXPECTED
    assert json['message'] == str(ID_USUARIO)


def find_user_get_password(user_name: str) -> dict:

    response = requests.get(f'{URL}user/{user_name}')
    json = response.json()

    assert response.status_code == STATUS_CODE_EXPECTED
    return json['password']


def login(user_name: str, password: str) -> str:

    message_expected = 'logged in user session:'

    response = requests.get(
        f'{URL}user/login?username={user_name}&password={password}')

    json = response.json()

    token = json['message'].rpartition(':')[-1]

    assert response.status_code == STATUS_CODE_EXPECTED
    assert message_expected in json['message']
    return token
