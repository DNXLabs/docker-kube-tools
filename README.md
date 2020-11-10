# docker-kube-tools

![Security](https://github.com/DNXLabs/docker-kube-tools/workflows/Security/badge.svg)
![Lint](https://github.com/DNXLabs/docker-kube-tools/workflows/Lint/badge.svg)

## Dependencies
- Docker

## Docker

#### Build
Now you are ready to build an image from this project Dockerfile.
```bash
docker build -t kube-tools .
```

#### Run

After your image has been built successfully, you can run it as a container.

```bash
docker run kube-tools --help
docker run kube-tools <command>
```

## Author

Managed by [DNX Solutions](https://github.com/DNXLabs).

## License

Apache 2 Licensed. See [LICENSE](https://github.com/DNXLabs/docker-kube-tools/blob/master/LICENSE) for full details.