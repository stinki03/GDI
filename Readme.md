# Project Boilerplate with Docker and Virtual Environment

This project provides a basic setup using Docker containers for MongoDB and RabbitMQ, along with a Python virtual environment.

## Requirements

- Docker
- Python 3.8 or higher
- `venv` module for creating virtual environments

---

## 🐳 Docker Containers

### MongoDB

Start a MongoDB container exposed on port 27017:

```bash
docker run --name mongo -d -p 27017:27017 mongodb/mongodb-community-server

### RabbitMQ

Start a RabbitMQ container with ports exposed for the admin console (15672) and the broker (5672):

```bash
docker run -d --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq
