def test_create_article_unauthorized(client):
    response = client.post(
        "/article/", 
        json={"title": "Test", "content": "..."}
    )
    
    assert response.status_code == 401

    
def test_get_article(client, articles):
    article = articles[0]
    
    response = client.get(f"/article/{article.id}")
    
    assert response.status_code == 200
    assert response.json["title"] == article.title
    assert response.json["content"] == article.content


def test_get_all_articles(client, articles):
    response = client.get("/article/all")
    
    assert response.status_code == 200
    assert len(response.get_json()) == len(articles)


def test_search_articles(client, articles):
    article = articles[0]
    
    response = client.get(
        "/article/search",
        json={"text": article.title}
    )
    
    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["title"] == article.title


def test_create_article(client, users, security_service):
    user = users[0]
    token = security_service.create_access_token(user.email)
    
    response = client.post(
        "/article/",
        json={
            "title": "Test Article",
            "content": "This is a test article."
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json["title"] == "Test Article"
    assert response.json["content"] == "This is a test article."


def test_update_article(client, articles, security_service):
    article = articles[0]
    token = security_service.create_access_token(article.owner.email)
    
    updated_title = "Updated Title"
    updated_content = "Updated Content"
    
    response = client.put(
        f"/article/{article.id}",
        json={"title": updated_title, "content": updated_content},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json["title"] == updated_title
    assert response.json["content"] == updated_content


def test_delete_article(client, articles, security_service):
    article = articles[0]
    token = security_service.create_access_token(article.owner.email)
    
    response = client.delete(
        f"/article/{article.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json["message"] == "Article deleted"
