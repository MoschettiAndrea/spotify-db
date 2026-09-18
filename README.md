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
│   └── sync_database.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### `src/`

* **`config.py`** — loads database, user, and Spotify data folder configuration from environment variables.
* **`database.py`** — handles database creation, table creation, and data insertion.
* **`models.py`** — defines the database schema using SQLAlchemy ORM models.
* **`parser.py`** — loads the Spotify JSON export files and transforms them into the tables used by the database.
* **`pipeline.py`** — coordinates the parsing, reconciliation, and insertion steps for both initial database creation and subsequent updates.
* **`sync.py`** — compares newly parsed data with existing database tables and identifies rows that need to be inserted.

### `scripts/`

* **`sync_database.py`** — creates the database if it does not exist, or updates the existing database by adding records from the Spotify export that are not already present.

### `docs/`

* **`simplified_ER_schema.png`** — simplified Entity-Relationship diagram of the database schema.

### Configuration files

* **`.env.example`** — template showing the environment variables required by the project.
* **`.gitignore`** — excludes local environment files, virtual environments, and Python cache files from version control.

## Database schema

The database currently consists of the following tables:

* `users`
* `artists`
* `albums`
* `songs`
* `platforms`
* `listens`

The simplified Entity-Relationship schema is shown below:

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

Configure the required environment variables, then run:
```bash
python -m scripts.sync_database
```

The script validates the configuration, loads the Spotify JSON files, creates the MySQL database and tables if they don't already exist, and inserts only the data that isn't already stored.

The same command works for the first run and for every subsequent one. Point `SPOTIFY_FOLDER_PATH` at a folder with new export data and re-run it to bring the database up to date.
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
