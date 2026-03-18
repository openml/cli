# OpenML CLI

A command-line interface for interacting with the [OpenML](https://www.openml.org/) platform. Built using the [Click](https://click.palletsprojects.com/) framework and wrapping the official [openml-python](https://github.com/openml/openml-python) API.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# show help
openml --help

# display version
openml --version
```

### Configure

```bash
# view current server URL
openml configure get server

# set API key
openml configure set apikey YOUR_API_KEY

# set cache directory
openml configure set cachedir /path/to/cache
```

### Flows

```bash
# list all flows
openml flows list

# list flows with filters
openml flows list --size 20 --tag sklearn

# get detailed info about a flow
openml flows info 6969

# search flows by name
openml flows search "RandomForest"
```

### Datasets

```bash
# list datasets
openml datasets list --size 10 --status active

# get detailed info about a dataset
openml datasets info 61

# search datasets by name
openml datasets search "iris"
```

### Tasks

```bash
# list tasks
openml tasks list --size 10 --status active

# filter by task type or dataset
openml tasks list --task-type 1 --data-name iris

# get detailed info about a task
openml tasks info 1
```

### Runs

```bash
# list runs
openml runs list --size 10

# filter by task and flow
openml runs list --task 1 --flow 6969

# get detailed info about a run
openml runs info 100
```

## Development

### Setup

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## License

BSD-3-Clause
