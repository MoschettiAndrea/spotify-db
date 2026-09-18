# Spotify Database

A relational database built from Spotify Extended Streaming History exports.

The project parses Spotify's JSON streaming history and organizes the data into a relational schema using MySQL and SQLAlchemy. The database separates artists, albums, songs, listening platforms, users, and individual listening events.

## Project structure

```text
spotify-db/
├── docs/
│   └── simplified_ER_schema.png
├── src/
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── parser.py
│   ├── pipeline.py
│   └── sync.py
├── scripts/
│   ├── create_database.py
│   └── update_database.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### `src/`

* **`config.py`** — loads database, Spotify data folder, and user configuration from environment variables and validates the required settings.
* **`database.py`** — handles database creation, table creation, reading existing tables, data type alignment, and insertion of new rows.
* **`models.py`** — defines the database schema using SQLAlchemy ORM models.
* **`parser.py`** — loads Spotify Extended Streaming History JSON files and transforms the data into the tables used by the database.
* **`pipeline.py`** — coordinates the parsing, reconciliation, and insertion steps for both initial database creation and subsequent updates.
* **`sync.py`** — provides the reconciliation logic used to compare newly parsed data with records already stored in the database.

### `scripts/`

* **`create_database.py`** — creates the MySQL database and populates it with data from a Spotify export.
* **`update_database.py`** — updates an existing database with Spotify export data without recreating the database.

### `docs/`

* **`simplified_ER_schema.png`** — simplified Entity-Relationship diagram of the database schema.

### Configuration files

* **`.env.example`** — template showing the environment variables required by the project.
* **`.gitignore`** — excludes local environment files, virtual environments, and Python cache files from version control.

## Database schema

The database consists of six tables:

* `users`
* `artists`
* `albums`
* `songs`
* `platforms`
* `listens`

The relationships between these tables are shown in the simplified Entity-Relationship diagram below:

![Simplified ER schema](docs/simplified_ER_schema.png)

## Requirements

* Python 3
* MySQL Server
* Python packages listed in `requirements.txt`

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

A running MySQL Server installation is also required.

## Configuration

The project uses environment variables for database credentials and other machine-specific settings.

The following variables are supported:

```text
SPOTIFY_DB_USER
SPOTIFY_DB_PASSWORD
SPOTIFY_DB_HOST
SPOTIFY_DB_NAME
SPOTIFY_FOLDER_PATH
SPOTIFY_USERNAME
```

An example configuration is provided in `.env.example`.

The current implementation reads these values directly from the environment. The `.env.example` file is provided as a template and is not loaded automatically.

## Usage

### Create the database

To create a new database from the Spotify export, configure the required environment variables and run:

```bash
python -m scripts.create_database
```

The script validates the configuration, loads the Spotify JSON files, creates the MySQL database if it does not already exist, creates the database tables, and imports the parsed data.

### Update an existing database

Once the database has been created, new Spotify export data can be added without rebuilding the database.

Run:

```bash
python -m scripts.update_database
```

## Data exploration and visualization

Notebooks for exploring the resulting database and analyzing listening habits are planned.

Planned analyses include:

* Listening activity over time
* Most played artists, albums, and songs
* Listening duration and playback patterns
* Platform usage
* Temporal listening patterns
* Other statistics derived from the relational database

## Work in progress

This project is currently being developed as a personal data engineering and analysis project.

The database creation and incremental update pipelines are implemented. Data exploration and visualization notebooks are planned.
