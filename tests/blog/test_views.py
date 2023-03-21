from apps.blog.models import PostItem


def post_item(client, title, body, is_public):
    data = dict(title=title, body=body, is_public=is_public)
    return client.post('/blog/post', data=data, follow_redirects=True)
    
def test_post(client):
    title = 'test_title'
    body = 'body'
    is_public = True
    result = post_item(client, title=title, body=body, is_public=is_public)

    assert title in result.data.decode()
    assert body in result.data.decode()


def test_edit(client):
    title = 'test_title'
    body = 'body'
    is_public = True
    post_item(client, title=title, body=body, is_public=is_public)

    item = PostItem.query.first()

    result = client.get(f'/blog/{item.id}')