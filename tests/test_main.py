def test_read_users(db_session, test_client, subtests):
    response = test_client.get("/")

    with subtests.test("Check response status code"):
        assert response.status_code == 200

    with subtests.test("Check if 'User Information' is in response"):
        assert "User Information" in response.text

    with subtests.test("Check if 'Ervin Howell' is in response"):
        assert "Ervin Howell" in response.text
