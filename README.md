[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# UP42 parameter validator

API that can help you validate parameters for UP42 blocks

## Requirements

Python 3.8

[Poetry](https://python-poetry.org/docs/#installation)

_Optional:_
Create [virtualenv](https://virtualenv.pypa.io/en/latest/) for this project.

## Installation

``` $ poetry install --no-dev```

## Usage

### Run FastAPI server locally

``` $ uvicorn main:app --reload ```

### Interactive API documentation

[Swagger](http://127.0.0.1:8000/docs) __or__  [ReDoc](http://127.0.0.1:8000/redoc)

## Development

### Install development requirements

``` $ poetry install ```

### Install pre-commit hooks

``` $ pre-commit install ```

### Run tests

``` $ pytest ```
