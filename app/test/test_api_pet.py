import pytest
import requests

URL = 'https://petstore.swagger.io/v2/'
ID_USUARIO = 4781678
STATUS_CODE_ESPERADO = 200


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

    assert request.status_code == STATUS_CODE_ESPERADO


@pytest.mark.order(2)
def test_get_user():
    username = 'Isaac'
    email_esperado = 'admin@admin'
    firstname_esperado = 'Batata'

    request = requests.get(f'{URL}user/{username}')
    json = request.json()

    assert request.status_code == STATUS_CODE_ESPERADO
    assert json['id'] == ID_USUARIO
    assert json['username'] == username
    assert json['firstName'] == firstname_esperado
    assert json['email'] == email_esperado


@pytest.mark.order(3)
def test_find_and_login():
    user_name = 'Isaac'
    token = login(user_name, consultar_usuario_extrair_senha(user_name))


@pytest.mark.order(5)
def test_delete_user():

    username = 'Testinho'
    resposta = requests.delete(url=f'{URL}user/{username}')
    json = resposta.json()

    assert resposta.status_code == STATUS_CODE_ESPERADO
    assert json['code'] == STATUS_CODE_ESPERADO
    assert json['message'] == username


@pytest.mark.order(4)
def test_update_user(user):
    username = 'Testinho'

    user['username'] = username

    resposta = requests.put(url=f'{URL}user/{username}', json=user)
    json = resposta.json()

    assert resposta.status_code == STATUS_CODE_ESPERADO
    assert json['code'] == STATUS_CODE_ESPERADO
    assert json['message'] == str(ID_USUARIO)


def consultar_usuario_extrair_senha(username):

    resposta = requests.get(f'{URL}user/{username}')
    json = resposta.json()

    assert resposta.status_code == STATUS_CODE_ESPERADO
    return json['password']


def login(username, password):

    mensagem_esperada = 'logged in user session:'

    resposta = requests.get(
        f'{URL}user/login?username={username}&password={password}')

    json = resposta.json()

    token = json['message'].rpartition(':')[-1]

    assert resposta.status_code == STATUS_CODE_ESPERADO
    assert mensagem_esperada in json['message']
    return token
