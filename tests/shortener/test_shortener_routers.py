import asyncio
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_simple_shorten_and_redirect(async_client):
    # shorted link and duplicate query don't create obj
    response = await async_client.post("/shorten", json={"url": "https://example.com/"})
    response_2 = await async_client.post("/shorten", json={"url": "https://example.com/"})

    assert response.status_code == 200
    assert response_2.status_code == 200

    data = response.json()
    data_2 = response_2.json()

    assert data.get("short_id") == "DxFdsGK3wN"
    assert data_2.get("short_id") == "DxFdsGK3wN"

    # redirect (do not follow) and check location header
    response = await async_client.get(f"/{data['short_id']}", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "https://example.com/"

    # stats should show 1 visit
    response = await async_client.get(f"/stats/{data['short_id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["visits"] == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_multiple_visits_increment(async_client):
    response = await async_client.post("/shorten", json={"url": "https://example.com/123"})
    data = response.json()

    # visit 10 times
    tasks = [async_client.get(f"/{data['short_id']}", follow_redirects=False) for _ in range(10)]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == 307

    response = await async_client.get(f"/stats/{data['short_id']}")

    data = response.json()
    assert data["visits"] == 10


@pytest.mark.asyncio(loop_scope="session")
async def test_validate(async_client):
    response = await async_client.post("/shorten", json={"url": "foo"})
    data = response.json()

    assert response.status_code == 422
    assert data.get('detail', [])[0].get('msg') == 'Input should be a valid URL, relative URL without a base'

    response = await async_client.get(f"/123", follow_redirects=False)
    data = response.json()

    assert response.status_code == 404
    assert data.get('detail') == 'Not found'

    response = await async_client.get(f"/stats/123", follow_redirects=False)
    data = response.json()

    assert response.status_code == 404
    assert data.get('detail') == 'Not found'
