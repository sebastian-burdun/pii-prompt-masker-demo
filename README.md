# PII Prompt Masker DEMO


## Requirements
- Linux (tested on Ubuntu 22.04)
- Docker (tested on 24.0.6)
- Docker Compose (tested on 2.21.0)


## Set up

1. Clone the repository:
```bash
$ git clone git@github.com:sebastian-burdun/pii-prompt-masker-demo.git
```

2. Run:
```bash
$ cd pii-prompt-masker-demo
$ docker-compose up
```

3. Use the http://localhost:8000/generate-answer POST endpoint in accordance to the documentation.


## Usage

API reference can be found at http://localhost:8000/docs after starting the application.


## Documentation

There are basically three sources of those:

1. Folder `/docs` in the repository, containing:
- original challenge description
- notes on made design choices
- notes on particular phone masking issue

2. Mentioned API reference.

3. In code docstrings and comments.
