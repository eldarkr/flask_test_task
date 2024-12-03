def test_login_success(auth_service, users):
    user = users[0]
    email = user.email
    password = user.password
    token = auth_service.login(password, email)
    assert token is not None


def test_login_invalid_password(auth_service, users):
    user = users[0]
    email = user.email
    password = user.password + "1"
    
    token = auth_service.login(password, email)
    
    assert token is None


def test_login_user_not_found(auth_service):
    email = "notexist@example.com"
    password = "password123"
    
    token = auth_service.login(password, email)
    
    assert token is None
