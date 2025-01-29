def test_signup(client):
    response = client.post('/sign-up', data={
        "email": "newuser@example.com",
        "firstName": "NewUser",
        "password1": "SecurePass123!",
        "password2": "SecurePass123!"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Account Created Successfully!' in response.data
