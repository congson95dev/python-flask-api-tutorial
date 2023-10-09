import json


def get_response_body_from_request(client, url, data, method):
    response = getattr(client, method)(url, json=data)
    body = json.loads(response.get_data(as_text=True))
    return response, body


def get_response_body_from_request_form_data(client, url, data, method):
    response = getattr(client, method)(url, data=data, follow_redirects=True)
    body = json.loads(response.get_data(as_text=True))
    return response, body
