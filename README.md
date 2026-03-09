# devops-capstone-project

![Build Status](https://github.com/Aviral3501/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)

# Customer Accounts microservice 

## Overview

The **DevOps Capstone Project** demonstrates the application of modern DevOps practices to design, build, test, secure, containerize, and deploy a cloud-native microservice.

In this project, a **Customer Accounts microservice** is developed using Python and Flask. The service exposes RESTful APIs that allow users to create, read, update, delete, and list customer account records.

The project follows **Agile development practices** and implements a complete **DevOps lifecycle**, including test-driven development (TDD), continuous integration (CI), containerization, and automated deployment to Kubernetes.

## Project Goals

The goal of this project is to implement and demonstrate the following DevOps practices:

* Agile project planning using GitHub Issues and a Kanban board
* Test-Driven Development (TDD) for building REST APIs
* Continuous Integration using GitHub Actions
* Code quality checks using Flake8 and code coverage tools
* Secure coding practices using Flask security extensions
* Containerization using Docker
* Deployment to Kubernetes / OpenShift
* Continuous Delivery pipeline using Tekton

## Microservice Features

The Customer Accounts microservice provides the following functionality:

* Create a new customer account
* Retrieve account details
* Update existing account information
* Delete a customer account
* List all customer accounts

## Technology Stack

The following technologies are used in this project:

* **Python 3.9**
* **Flask**
* **PostgreSQL**
* **Docker**
* **Kubernetes / OpenShift**
* **GitHub Actions**
* **Tekton Pipelines**
* **Flake8**
* **Nose Tests**
* **Coverage**

## Project Structure

The project follows the **Model-View-Controller (MVC)** design pattern.

```
service/
│
├── common/          # Common logging and error handlers
├── config.py        # Flask configuration
├── models.py        # Database models and business logic
└── routes.py        # REST API routes

tests/
├── factories.py
├── test_cli_commands.py
├── test_models.py
└── test_routes.py
```

## Development Environment

This project is designed to run in the **IBM Developer Skills Network Cloud IDE with OpenShift**.

To initialize the development environment:

```bash
source bin/setup.sh
```

This script will:

* Install Python 3.9
* Configure a virtual environment
* Install required dependencies

After setup, your prompt should look like:

```
(venv) theia:project$
```

## Useful Commands

### Activate the Python Virtual Environment

```bash
source ~/venv/bin/activate
```

### Install Project Dependencies

```bash
make install
```

### Start PostgreSQL Docker Container

```bash
make db
```

Verify that the container is running:

```bash
docker ps
```

## Testing

The project uses **nose tests** and **coverage** to ensure code quality.

Run tests with:

```bash
nosetests
```

Check test coverage:

```bash
coverage report
```

The project maintains **at least 95% test coverage**.

## License

This project is developed as part of the **IBM DevOps Professional Certificate Capstone Project**.
