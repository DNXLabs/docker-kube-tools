# docker-kubectl

![Security](https://github.com/DNXLabs/docker-kubectl/workflows/Security/badge.svg)
![Lint](https://github.com/DNXLabs/docker-kubectl/workflows/Lint/badge.svg)

## Dependencies
- Docker

## Docker

#### Build
Now you are ready to build an image from this project Dockerfile.
```bash
docker build -t kubectl .
```

#### Run

After your image has been built successfully, you can run it as a container.

```bash
docker run kubectl --help
docker run kubectl <command>
```

## Author
App managed by DNX Solutions.

## License
Apache 2 Licensed. See LICENSE for full details.