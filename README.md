# Test-Data-Generator

## Overview

This Python project serves as a test data generator with Snowflake integration. It allows you to generate test data and load it into a Snowflake database, making it suitable for various testing and development purposes. The project is structured to run within a Docker container for portability and ease of use.

## Project Structure

The project is organized as follows:
```plaintext
test-data-generator/
├── Dockerfile
├── docker-compose.yml
├── config/
│ ├── config.yaml
│ └── secrets.yaml
├── generators/
│ ├── init.py
│ ├── name_generator.py
│ ├── email_generator.py
│ └── ...
├── tests/
│ ├── init.py
│ ├── test_data_generation.py
├── data/
│ ├── pii_data/
│ └── generated_data/
├── main.py
├── snowflake/
│ ├── snowflake_connection.py
│ ├── snowflake_loader.py
├── README.md
├── requirements.txt
```

- `Dockerfile`: Defines the Docker container for the project.
- `docker-compose.yml`: Orchestrates services and dependencies for running the project with Docker Compose.
- `config`: Contains configuration files, including `config.yaml` and `secrets.yaml`.
- `generators`: Houses data generation modules, such as `name_generator.py` and `email_generator.py`.
- `tests`: Contains unit tests for data generation modules.
- `data`: Stores PII data and generated data.
- `main.py`: The entry point of the application.
- `snowflake`: Holds modules for Snowflake integration.
- `README.md`: This document.
- `requirements.txt`: Lists project dependencies.

## Prerequisites

Before using this project, you need to have the following prerequisites installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.x
- Required Python dependencies listed in `requirements.txt`.

## Usage

1. Clone this repository to your local machine.

2. Set up your Snowflake credentials in `config/secrets.yaml`.

3. Build the Docker image:

   ```bash
   docker build -t test-data-generator . 

4. Run the Docker Container
```docker-compose up -d```
