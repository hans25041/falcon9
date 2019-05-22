# Falcon9 Coding Challenge

The models.py file contains a set of classes that model the Falcon9 rocket.
Tests are contained in the tests.py file.

## Installation

The only requirement is the `inflect` package which is used for pluralization.
You can pip install the requirements file directly or in a virtualenv. There
is also a Dockerfile with docker-compose.yml which allow you to run the files
within docker. Simply build the container:

```
$ docker-compose up
```

Then run a bash shell within the container:

```
$ docker-compose run app bash
```

From there, you can run the tests or the sample flight from the models.py file.

## Run the sample flight

```
$ python models.py
```

## Run the tests

```
$ python tests.py
```

