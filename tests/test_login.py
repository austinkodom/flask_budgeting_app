def test_login_success(client, new_user):
    """Test successful login with correct credentials."""
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'TestPass123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Logged in successfully!' in response.data  # Check flash message
    assert b'Logout' in response.data  # Ensure logout button appears (means user is logged in)


def test_login_wrong_password(client, new_user):
    """Test login failure with incorrect password."""
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'WrongPass123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Incorrect password, try again.' in response.data  # Check flash message
    assert b'Login' in response.data  # Ensure login button still appears


def test_login_nonexistent_user(client):
    """Test login failure with an unregistered email."""
    response = client.post('/login', data={
        'email': 'doesnotexist@example.com',
        'password': 'SomePass123!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Email does not exist.' in response.data  # Check flash message
    assert b'Login' in response.data  # Ensure login button still appears

def test_restricted_access(client):
    """ Test that unauthorized user cannot access routes. """
    response = client.get('/expenses', follow_redirects=True)
    assert b'Please log in to access this page.' in response.data   # Flashed message
    assert b'Login' in response.data    # Ensure redirect to login page
