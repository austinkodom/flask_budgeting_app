def test_logout(client, new_user):
    """Test user logout functionality."""
    # Log in first
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'TestPass123!'
    }, follow_redirects=True)

    # Check user is logged in
    response = client.get('/')
    assert b'Logout' in response.data  # Check logout button appears

    # Log out
    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data  # Ensure the user is redirected to the login page
    assert b'Logged out successfully!' in response.data  # Flash message
