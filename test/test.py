# Author:   Edmond Chuc
# Purpose:  Validate persistent web and RDF redirects. 

import requests
import yaml

import time


def test_web(url):
    r = requests.get(url)
    assert r.status_code == 200 == requests.codes.ok, f'URL failed: {url}'


def validate_response(r, url, media_type, request_type):
    assert media_type in r.headers['Content-Type'], url + f" received Content-Type as {r.headers['Content-Type']} instead of {media_type}. Request type: {request_type}"
    assert r.status_code == requests.codes.ok, f'{url} with code {r.status_code} and message: {r.content.decode("utf-8")}'


def validate_rdf(url, media_type, file_extension):
    if file_extension == '.owl':
        pass
    else:
        # Request types
        QSA = 'QSA'
        ACCEPT = 'ACCEPT'
        FILE_EXT = 'FILE_EXT'


        # Query string
        r = requests.get(url + f'?_format={media_type}')
        validate_response(r, url, media_type, QSA) 

        # Accept header
        r = requests.get(url, headers={'Accept': f'{media_type}'})
        validate_response(r, url, media_type, ACCEPT)

        # File extension
        r = requests.get(url + f'{file_extension}')
        validate_response(r, url, media_type, FILE_EXT)


def test_rdf(url):
    print('testing for .ttl', flush=True)
    validate_rdf(url, 'text/turtle', '.ttl')
    
    print('testing for .rdf', flush=True)
    validate_rdf(url, 'application/rdf+xml', '.rdf')

    print('testing for .nt', flush=True)
    validate_rdf(url, 'application/n-triples', '.nt')

    print('testing for .jsonld', flush=True)
    validate_rdf(url, 'application/ld+json', '.jsonld')

    print('testing for .n3', flush=True)
    validate_rdf(url, 'text/n3', '.n3')

    print('testing for .owl', flush=True)
    validate_rdf(url, None, '.owl')


def test_rdf_turtle(url):
    print('testing for .ttl', flush=True)
    validate_rdf(url, 'text/turtle', '.ttl')


if __name__ == '__main__':
    with open('test/test.yml') as f:
        config = yaml.safe_load(f)

        start_time = time.time()

        # Web artifacts
        for i, url in enumerate(config['web']):
            print(f'testing web {i + 1} of {len(config["web"])} with {url}', flush=True)
            test_web(f"{config['protocol']}://{config['docker_name']}/{url}")

        # RDF things
        for i, url in enumerate(config['rdf']):
            print(f'testing rdf {i + 1} of {len(config["rdf"])} with {url}', flush=True)
            test_rdf(f"{config['protocol']}://{config['docker_name']}/{url}")

        for i, url in enumerate(config['rdf_turtle']):
            print(f'testing rdf_turtle {i + 1} of {len(config["rdf_turtle"])} with {url}', flush=True)
            test_rdf_turtle(f"{config['protocol']}://{config['docker_name']}/{url}")

        print(f'All tests passed. Duration: {time.time() - start_time:.2f} seconds.')