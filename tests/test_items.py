def test_list_items(client):
    resp = client.get("/items")
    assert resp.status_code == 200
    assert resp.json() == []
