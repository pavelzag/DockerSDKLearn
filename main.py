import docker
from fake_useragent import UserAgent
from httplib import HTTPConnection
import os
import pytest
from random import choice
import requests
from string import ascii_uppercase
import time


class MyHTTPConnection(HTTPConnection):
    _http_vsn_str = '6.9'

ip = '127.0.0.1'
url = '{}{}'.format('http://', ip)


@pytest.yield_fixture(scope='function')
def docker_handling():
    pull_docker()
    run_docker()


def generate_big_header():
    return ''.join(choice(ascii_uppercase) for i in range(32000))


def pull_docker():
    client = docker.from_env(version="1.22")
    start_time = time.time()
    image = client.images.pull("nginx")
    print('{} {}'.format('Time to pull', time.time() - start_time))
    print(image.id)


def run_docker():
    start_time = time.time()
    client = docker.from_env(version="1.22")
    os.system('docker run -d --name test-nginx -p 8080:8080 -v $(pwd):/example/nginx/index.html:ro nginx:latest')
    print('{} {}'.format('Time to run', time.time() - start_time))
    client.containers.list()
    print('{} {}'.format('Time to list', time.time() - start_time))


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


def test_get_request(docker_handling):
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