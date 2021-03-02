from client import client


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'404' in rv.data


def test_quote(client):
    """
    Test to add a quote.

    :param client: The client
    """
    response = client.post(
        '/quotes',
        json={
            'text': 'This is a quote',
            'author': 'A wise man',
            'book': 'A good book',
        }
    )
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json['text'] == 'This is a quote'
    quote_id = response_json['id']
    assert client.put(f'/quote/{quote_id}', json={'text': 'A modified quote'}).status_code == 200
    assert client.delete(f'/quote/{quote_id}').status_code == 200
    assert client.get('/quote/1').status_code == 404


def test_get_quotes(client):
    """
    Test to get quotes.

    :param client: the client
    """
    client.post(
        '/quotes',
        json={
            'text': 'This is a quote',
            'author': 'A wise man',
            'book': 'A good book',
        }
    )
    rv = client.get('/quotes').get_json()
    assert len(rv['quotes']) > 0
