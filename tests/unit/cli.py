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

    @staticmethod
    def check(method, url, values):
        assert FakeResponse.method == method
        assert FakeResponse.url == url
        if values == None:
            assert FakeResponse.data == None
        else:
            for key,value in values:
                assert FakeResponse.data[key] == value
            
@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.setattr("requests.put",
                        lambda url,data: FakeResponse('PUT', url, data))
    monkeypatch.setattr("requests.post",
                        lambda url,data: FakeResponse('POST', url, data))
    monkeypatch.setattr("requests.delete",
                        lambda url: FakeResponse('DELETE', url, None))
    monkeypatch.setattr("requests.post",
                        lambda url,data: FakeResponse('POST', url, data))

# and now the tests. Note that these only test that (a) the cli functions don't
# crash, and (b) the http parameters match what we expect.
#

class TestCLI:
    def test_user_create(self):
        cli.user_create('joe', 'password')
        FakeResponse.check('PUT', 'http://abc:5000/user/joe', 
                           [('password', 'password')])
    
    def test_user_delete(self):
        cli.user_delete('joe')
        FakeResponse.check('DELETE', 'http://abc:5000/user/joe', [])

    def test_network_create(self):
        cli.network_create('net10', 'group1')
        FakeResponse.check('PUT', 'http://abc:5000/network/net10',
                           [('group', 'group1')])
    
    def test_network_delete(self):
        cli.network_delete('net10')
        FakeResponse.check('DELETE', 'http://abc:5000/network/net10', [])
        pass

    def test_group_add_user(self):
        cli.group_add_user('group12', 'user4')
        FakeResponse.check('POST', 'http://abc:5000/group/group12/add_user',
                           [('user', 'user4')])

    def test_group_remove_user(self):
        cli.group_remove_user('group17', 'user42')
        FakeResponse.check('POST', 'http://abc:5000/group/group17/remove_user',
                           [('user', 'user42')])
        
    def test_project_create(self):
        cli.project_create('projectname12', 'group2')
        FakeResponse.check('PUT', 'http://abc:5000/project/projectname12',
                           [('group', 'group2')])
