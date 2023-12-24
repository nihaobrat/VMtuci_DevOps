def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Добро пожаловать VMtuci' in response.get_data(as_text=True)

def test_registration_page(client):
    response = client.get('/registration')
    assert response.status_code == 200
    assert 'Регистрация VMtuci' in response.get_data(as_text=True)

def test_signin_page(client):
    response = client.get('/signin')
    assert response.status_code == 200
    assert 'Добро Пожаловать VMtuci' in response.get_data(as_text=True)

def test_user_settings_page(client):
    with client.session_transaction() as sess:
        sess['user'] = 'testuser'
    response = client.get('/user_settings')
    assert response.status_code == 200
    assert 'Редактировать профиль' in response.get_data(as_text=True)

def test_create_post_page(client):
    with client.session_transaction() as sess:
        sess['user'] = 'testuser'
    response = client.get('/createpost')
    assert response.status_code == 200
    assert 'Создание поста' in response.get_data(as_text=True)

def test_all_users_page(client):
    with client.session_transaction() as sess:
        sess['user'] = 'testuser'
    response = client.get('/allusers')
    assert response.status_code == 200
    assert 'Поиск Друзей' in response.get_data(as_text=True)

def test_logout(client):
    with client.session_transaction() as sess:
        sess['user'] = 'testuser'
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'Регистрация VMtuci' in response.get_data(as_text=True)