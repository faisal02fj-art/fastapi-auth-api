USER = {
    "name": "faisal",
    "email": "fai@gmail.com",
    "age": 25,
    "password": "asd123",
}


def register(client, **changes):
    return client.post("/register", json={**USER, **changes})


def login(client, email=USER["email"], password=USER["password"]):
    return client.post("/login", data={"username": email, "password": password})


def auth_header(client):
    register(client)
    token = login(client).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_success(client):
    r = register(client)
    print(r.json())                          # see the real response with: pytest -s
    assert r.status_code == 200


def test_register_duplicate_email(client):
    register(client)
    r = register(client)
    print(r.json())
    assert r.status_code in (400, 409)       # use the code your route returns


def test_register_short_password_rejected(client):
    assert register(client, password="1").status_code == 422


def test_login_success_returns_token(client):
    register(client)
    r = login(client)
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    register(client)
    assert login(client, password="WrongPass1").status_code == 401


def test_login_unknown_email(client):
    assert login(client, email="nobody@gmail.com").status_code == 401


def test_protected_route_without_token(client):
    assert client.get("/Secure").status_code == 401


def test_protected_route_with_bad_token(client):
    r = client.get("/Secure", headers={"Authorization": "Bearer undefined"})
    assert r.status_code == 401


def test_protected_route_with_valid_token(client):
    r = client.get("/Secure", headers=auth_header(client))
    assert r.status_code == 200