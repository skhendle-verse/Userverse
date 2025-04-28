from tests.http.conftest import client

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Welcome to the Userverse backend API"}