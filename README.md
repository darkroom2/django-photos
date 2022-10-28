## Photo managing backend application

The task content is in the [`TASK.md`](TASK.md) file.

### Requirements

* `python`
* [`requirements.txt`](requirements.txt)

#### Install libraries / dependencies

```shell
pip install -U pip
pip install -r requirements.txt
```

#### Run server

```shell
./manage.py migrate
./manage.py runserver
```

#### Run tests

Install `dev` requirements:

```shell
pip install -r requirements-dev.txt
```

Run tests:

```shell
./manage.py test
```

Run tests with coverage:

```shell
coverage run --source='.' manage.py test
coverage report
```

### Endpoints

#### `/api/photos/`

* GET: List all photos
* POST: Create a new photo

#### `/api/photos/{int:id}`

* GET: Retrieve a photo
* PUT: Update a photo
* PATCH: Partial update a photo
* DELETE: Delete a photo

#### `photos/import/`

* POST: Upload photos from external api

Example requests are included in [test_api.http](api/tests/test_api.http) file.

## CLI

To show help:

```shell
./manage.py load_batch --help
```

Example usage:

```shell
./manage.py load_batch --url https://jsonplaceholder.typicode.com/photos
```

```shell
./manage.py load_batch --file /path/to/file.json
```
