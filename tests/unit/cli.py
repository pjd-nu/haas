"""Functional tests for cli.py"""

# Notes:
#

from haas import model, api, cli
import pytest

from haas.config import cfg
cfg.add_section('client')
cfg.set('client', 'endpoint', 'http://abc:5000')

# Here's the fake HTTP infrastructure. Use monkeypatch to stash the method, url,
# and data and return a fake status code, then return them when needed.
#
# will need updating to provide data results for query.
#
class FakeResponse:
    method = None
    url = None
    data = None
    
    def __init__(self, method, url, data):
        self.status_code = 200  # 200 OK
        FakeResponse.method = method
        FakeResponse.url = url
        FakeResponse.data = data

    def reset(self):
        FakeResponse.method = None
        FakeResponse.url = None
        FakeResponse.data = None

    def check(self, method, url, values):
        assert FakeResponse.method == method
        assert FakeResponse.url == url
        for key,value in values:
            assert FakeResponse.data[key] == value

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.setattr("requests.put", lambda url,data: FakeResponse('PUT', url, data))
    monkeypatch.setattr("requests.delete", lambda url: FakeResponse('DELETE', url, None))
    monkeypatch.setattr("requests.post", lambda url,data: FakeResponse('POST', url, data))
    FakeResponse.reset()

# and now the tests. Note that these only test that (a) the cli functions don't
# crash, and (b) the http parameters match what we expect.
#
class TestCLI:
    def test_user_create(self):
        cli.user_create('joe', 'password')
        FakeResponse.check('PUT', 'http://abc:5000/user/joe', [('password', 'password')])

        def test_network_create(self):
            cli.network_create('net10', 'group1')
            FakeResponse.check('PUT', 'http://abc:5000/network/net10', [('group', 'group1')])

def network_delete(network):
    pass

def user_delete(username):
    pass
def group_add_user(group, user):

def group_remove_user(group, user):

def project_create(projectname, group, *args):
