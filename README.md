# Spotify Database

A relational database built from Spotify Extended Streaming History exports.

The project parses Spotify's JSON streaming history and organizes the data into a relational schema using MySQL and SQLAlchemy. The database separates artists, albums, songs, listening platforms, users, and individual listening events.

## Project structure

```text
spotify-db/
├── docs/
│   └── er-schema.png
├── src/
│   ├── database.py
│   ├── models.py
│   └── parser.py
├── scripts/
│   └── create_database.py
├── requirements.txt
└── README.md
```

### `src/`

* **`parser.py`** — loads the Spotify JSON export and transforms it into the tables used by the database.
* **`models.py`** — defines the database schema using SQLAlchemy ORM models.
* **`database.py`** — handles database creation, table creation, and data insertion.

### `scripts/`

* **`create_database.py`** — runs the complete pipeline to create and populate the database from a Spotify export.

### `docs/`

* **`er-schema.png`** — simplified Entity-Relationship diagram of the database schema.

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
* MySQL
* Python packages listed in `requirements.txt`

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

A running MySQL Server installation is also required.

## Usage

Place your Spotify Extended Streaming History JSON files somewhere accessible to the project and configure the input path in `scripts/create_database.py`.

Then run:

```bash
python -m scripts.create_database
```

This creates the MySQL database, creates the tables, and imports the parsed Spotify data.

## Planned features

### Database updates

Add `update_database.py` to support importing new Spotify Extended Streaming History exports without rebuilding the database from scratch.

The update process will identify new artists, albums, songs, platforms, and listening events and add only the data that is not already present.

### Data exploration and visualization

Add notebooks for exploring the resulting database and analyzing listening habits through statistics and visualizations.

Planned analyses include:

* Listening activity over time
* Most played artists, albums, and songs
* Listening duration and playback patterns
* Platform usage
* Temporal listening patterns
* Other statistics derived from the relational database

## Work in progress

This project is currently being developed as a personal data engineering and analysis project. The database creation pipeline is implemented, while incremental database updates and data exploration/visualization notebooks are planned.
