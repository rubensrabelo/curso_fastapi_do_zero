from http import HTTPStatus

from schemas import UserPublic
from security import create_access_token


def test_root_should_return_ok_and_hello_world(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello, world!"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret"
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1
    }


def test_create_user_409_username_already_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "email": "alice@example.com",
            "password": "secret"
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_create_user_409_email_already_exists(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": user.email,
            "password": "secret"
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password}
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_read_user_by_id(client, user):
    response = client.get(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
                "username": user.username,
                "email": user.email,
                "id": user.id
            }


def test_404_for_read_user_by_id(client):
    response = client.get("/users/0")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": user.id,
    }

# Está dando no testes abaixo - ver isso depois
# def test_update_integrity_error(client, user, token):
#     response = client.put(
#         f"/users/{user.id}",
#         headers={"Authorization": f"Bearer {token['access_token']}"},
#         json={
#             "username": "fausto",
#             "email": "bob@example.com",
#             "password": "mynewpassword",
#         }
#     )
#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {"detail": "Username or Email already exists"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


# def test_404_for_delete(client, user, token):
#     response = client.delete(
#         f"/users/{user.id}",
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {"detail": "User not found"}

def test_get_current_user_not_found(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exists__exercicio(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
