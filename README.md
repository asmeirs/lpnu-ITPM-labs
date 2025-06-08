# Interactive Calculus Visualizer

## Prerequisites
- Docker installed on your machine (https://www.docker.com/get-started)

## Build the Docker Image
From the root directory (where the `Dockerfile` is located), run:

```bash
docker build -t calc-visualizer .
````

* `-t calc-visualizer` tags the image with a name.
* `.` specifies the current directory as the build context.

## Run the Docker Container

Run the container in detached mode and map port 8501:

```bash
docker run -d -p 8501:8501 calc-visualizer
```

* `-d` runs the container in the background.
* `-p 8501:8501` maps port 8501 on the host to port 8501 in the container.

The app will be accessible at: [http://localhost:8501](http://localhost:8501)
