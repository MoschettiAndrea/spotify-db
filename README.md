# Spotify Database

A relational database built from Spotify Extended Streaming History exports.

The project parses Spotify's JSON streaming history and organizes it into a MySQL database using SQLAlchemy. The database separates artists, albums, songs, platforms, users, and individual listening events.

## Project structure

```text
spotify-db/
├── docs/
│   └── simplified_ER_schema.png
├── notebooks/
│   └── listening_stats.ipynb
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

* **`config.py`** — reads database, user, and Spotify data folder settings from environment variables.
* **`database.py`** — handles database creation, table creation, and data insertion.
* **`models.py`** — defines the database schema using SQLAlchemy ORM models.
* **`parser.py`** — loads the Spotify JSON export files and transforms the data into the structures used by the database.
* **`pipeline.py`** — coordinates the parsing, reconciliation, and database update steps.
* **`sync.py`** — compares parsed data with existing database records and identifies new records to insert.

### `scripts/`

* **`sync_database.py`** — main entry point for creating the database or updating an existing one with new Spotify data.

### `notebooks/`

* **`listening_stats.ipynb`** — loads data from the database and provides statistics and visualizations of listening activity.

### `docs/`

* **`simplified_ER_schema.png`** — simplified Entity-Relationship diagram of the database schema.

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

An example configuration is provided in `.env.example`: copy it to `.env` and fill in real values. `config.py` loads `.env` automatically on import; variables already set in the real environment take priority over it.

## Usage

Once the environment variables are configured, run:

```bash
python -m scripts.sync_database
```

The script validates the configuration, loads the Spotify JSON files, and creates or updates the database as needed.

On the first run, it creates the database and its tables and imports the available listening history.

On subsequent runs, it compares the parsed data with the existing database and inserts records that are not already stored.

The same command is therefore used both for the initial database creation and for later updates. To add new Spotify export data, point `SPOTIFY_FOLDER_PATH` to the folder containing the export and run the script again.

## Listening Statistics

The `notebooks/listening_stats.ipynb` notebook loads data from the tables created by `scripts/sync_database.py`. It only reads from the database; it does not use the original JSON files or modify the database.

The analysis includes:

* Listening activity over time
* Most played artists, albums, and songs
* Listening duration and playback patterns
* Platform usage
* Temporal listening patterns
* Other statistics derived from the relational database
