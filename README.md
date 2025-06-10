# Interactive Calculus Visualizer

## Live Demo

The app is deployed and accessible at: [http://calc-visualizer.duckdns.org/](http://calc-visualizer.duckdns.org/)

## Public Docker Image

A pre-built Docker image is available on Docker Hub:

```
docker pull asmeirs/calc-visualizer:latest
```

You can browse the image on Docker Hub: [https://hub.docker.com/repository/docker/asmeirs/calc-visualizer](https://hub.docker.com/repository/docker/asmeirs/calc-visualizer)

## Quick Start

### 1. Run the App with Docker

To run the application locally using the public Docker image:

```bash
# Pull the image
docker pull asmeirs/calc-visualizer:latest

# Run with Docker
docker run -p 8501:8501 asmeirs/calc-visualizer:latest
```

Then open your browser and navigate to `http://localhost:8501`.

### 2. Run the App Locally from Source

If you prefer to run the code directly:

```bash
# Clone the repository
git clone https://github.com/asmeirs/lpnu-ITPM-labs.git
cd lpnu-ITPM-labs

# (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the app
streamlit run src/app.py
```

Open your browser and go to `http://localhost:8501`.
