from httpx import AsyncClient


async def test_get_tweet(ac: AsyncClient, insert_data):
    response = await ac.get("api/tweets/1")
    response_2 = await ac.get("api/tweets/4")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response_2.status_code == 404


async def test_get_tweets(ac: AsyncClient, insert_data):
    response = await ac.get("api/tweets/", headers={"api-key": "aaa"})
    response_2 = await ac.get("api/tweets/", headers={"api-key": "some"})

    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response_2.status_code == 404


async def test_post_tweets(ac: AsyncClient, insert_data):
    response = await ac.post(
        "api/tweets/",
        headers={"api-key": "aaa"},
        json={"tweet_data": "Hello all"},
    )
    response_2 = await ac.post("api/tweets/", headers={"api-key": "aaa"})

    assert response.status_code == 200
    assert response.json()["tweet_id"] == 2
    assert response_2.status_code == 422


async def test_post_like_to_tweet(ac: AsyncClient, insert_data):
    response = await ac.post("api/tweets/1/likes", headers={"api-key": "aaa"})
    response_2 = await ac.post(
        "api/tweets/1/likes", headers={"api-key": "aaa"}
    )
    response_3 = await ac.post(
        "api/tweets/3/likes", headers={"api-key": "aaa"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response_2.status_code == 404
    assert response_3.status_code == 404


async def test_delete_like_to_tweet(ac: AsyncClient, insert_data):
    response = await ac.delete(
        "api/tweets/1/likes", headers={"api-key": "aaa"}
    )
    response_2 = await ac.delete(
        "api/tweets/1/likes", headers={"api-key": "aaa"}
    )
    response_3 = await ac.delete(
        "api/tweets/3/likes", headers={"api-key": "aaa"}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response_2.status_code == 404
    assert response_3.status_code == 404


async def test_delete_tweet(ac: AsyncClient, insert_data):
    response = await ac.delete("api/tweets/1", headers={"api-key": "aaa"})
    response_2 = await ac.delete("api/tweets/1", headers={"api-key": "some"})
    response_3 = await ac.delete("api/tweets/4", headers={"api-key": "aaa"})
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response_2.status_code == 404
    assert response_3.status_code == 404
