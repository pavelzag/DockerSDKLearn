from docker_handler import pull_docker, run_docker
import pytest
from httplib import HTTPConnection
import requests
from fake_useragent import UserAgent
from string_gen import generate_big_header


class MyHTTPConnection(HTTPConnection):

    _http_vsn_str = '6.9'

ip = '127.0.0.1'
url = '{}{}'.format('http://', ip)


@pytest.yield_fixture(scope='function')
def docker_handling():
    pull_docker()
    run_docker()


def generate_report():
    return 'agg'


def get_request(url):
    r = requests.get(url)
    return r.status_code


def post_request(url):
    r = requests.post(url)
    return r.status_code


def header_test(url, user_agent):
    ua = UserAgent()
    if user_agent == 'chrome':
        headers = {'User-Agent': ua.chrome}
    elif user_agent == 'safari':
        headers = {'User-Agent': ua.safari}
    response = requests.get(url, headers)
    return response.status_code


def other_http_status_code():
    conn = MyHTTPConnection(ip)
    conn.request("GET", "/")
    response = conn.getresponse()
    return response.status


def big_header_method():
    big_header = generate_big_header()
    headers = {'User-Agent': big_header}
    response = requests.get(url, headers=headers)
    return response.status_code


def test_get_request():
    assert get_request(url) == 200


def test_post_request():
    assert post_request(url) == 405


def test_user_agent_chrome():
    assert header_test(url, user_agent='chrome') == 200


def test_user_agent_safari():
    assert header_test(url, user_agent='safari') == 200


def test_other_status_code():
    assert other_http_status_code() == 200


def test_big_header():
    assert big_header_method() == 400



# import docker
#
# if __name__ == '__main__':
#     print('ya')
#     client = docker.from_env(version="1.22")
#     image = client.images.pull("alpine")
#     print client.containers.run("alpine", ["echo", "hello", "world"])
#     # client = docker.DockerClient(version="1.22", base_url='unix://var/run/docker.sock')
#     for container in client.containers.list():
#         print container.id
#         print(client)