import docker
import os
import time


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