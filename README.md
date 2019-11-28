# TERN Tests - W3ID Persistent URI Service

## Run tests with Docker

We use the `Dockerfile` to create a container for the Apache HTTP server containing our `.htaccess` rules. A second Dockerfile in `tests/Dockerfile` will be used to run tests against the Apache container. 


### Apache container

Create a Docker network for the Apache container and the test container to communicate.

```
docker network create test
```

Build the Docker image from the Dockerfile in the **current** directory.

```
docker build -t httpd .
```

Run the Docker image as a container.

```
docker run -dit --rm --name httpd -p 8000:80 --network test httpd
```

The redirects should work on `localhost:8000`. E.g. try going to `localhost:8000/tern/ontologies/org`. 


### Test scripts container

Follow the instructions in [test/README.md](test/README.md). 
