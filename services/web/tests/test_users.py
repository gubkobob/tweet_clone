from httpx import AsyncClient


async def test_get_user_by_id(ac: AsyncClient, insert_data):
    response = await ac.get("api/users/1")
    assert response.status_code == 200
    assert response.json()["user"]["id"] == 1

    response_2 = await ac.get("api/users/3")
    assert response_2.status_code == 404


async def test_post_follow_to_user(ac: AsyncClient, insert_data):
    response = await ac.post("api/users/2/follow", headers={"api-key": "aaa"})
    response_2 = await ac.post(
        "api/users/2/follow", headers={"api-key": "111"}
    )
    response_3 = await ac.post(
        "api/users/4/follow", headers={"api-key": "aaa"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response_2.status_code == 404
    assert response_3.status_code == 404


async def test_delete_follow_to_user(ac: AsyncClient, insert_data):
    response = await ac.delete(
        "api/users/2/follow", headers={"api-key": "aaa"}
    )
    response_2 = await ac.delete(
        "api/users/2/follow", headers={"api-key": "aaa"}
    )
    response_3 = await ac.delete(
        "api/users/4/follow", headers={"api-key": "aaa"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response_2.status_code == 404
    assert response_3.status_code == 404


async def test_get_user_me(ac: AsyncClient, insert_data):
    response = await ac.get("api/users/me", headers={"api-key": "aaa"})
    response_2 = await ac.get("api/users/me", headers={"api-key": "some"})
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response_2.status_code == 404


async def test_get_user_by_id(ac: AsyncClient, insert_data):
    response = await ac.get("api/users/1")
    response_2 = await ac.get("api/users/4")
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response_2.status_code == 404
