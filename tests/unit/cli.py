from haas import model, api, cli
import pytest

import requests

req_URI = ''
req_method = ''
req_data = ''
req_status = 0

from haas.config import cfg
cfg.add_section('client')
cfg.set('client', 'endpoint', 'http://abc:5000')

class foo:
    def __init__(self, rsp):
        self.status_code = rsp
        
def do_put(url, data):
    global req_URI, req_method, req_data
    req_URI = url
    req_method = 'PUT'
    req_data = data
    return foo(req_status)

def do_delete(url):
    global req_URI, req_method, req_data
    req_URI = url
    req_method = 'DELETE'
    req_data = None
    return foo(req_status)

def do_post(url, data):
    global req_URI, req_method, req_data
    req_URI = url
    req_method = 'POST'
    req_data = data
    return foo(req_status)

def test_user_create(monkeypatch):
    global req_status
    monkeypatch.setattr(requests, 'put', do_put)
    req_status = 200
    cli.user_create('joe', 'password')
    assert req_method == 'PUT'
    assert req_URI == 'http://abc:5000/user/joe'
    assert 'password' in req_data and req_data['password'] == 'password'

def test_network_create(monkeypatch):
    global req_status
    monkeypatch.setattr(requests, 'put', do_put)
    req_status = 200
    cli.network_create('net10', 'group1')
    assert req_method == 'PUT'
    assert req_URI == 'http://abc:5000/network/net10'
    assert req_data['group'] == 'group1'

