# Leveraging Data to Enforce Short-Term Rental Rules

## Introduction:
In response to Vancouver's housing affordability crisis, regulations now require Airbnb hosts to live on the property they rent out. To enforce these rules, we are developing a data-driven approach using Airbnb data.


## Setup

Create virtual environment:

```
python -m venv venv
```

Activate the virtual environment:
* On Windows:
```
venv\Scripts\activate
```
* On macOS and Linux:

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Install new package if needed:

```
pip install {package_name}
pip freeze > requirements.txt
```

Deactivate the virtual environment:
```
deactivate
```

Don't forget to activate the virtual environment every time you enter the project again.

## How to get data

1. Activate the virtual environment as described above
2. Move to the folder with scraping files and run downloading of listing htmls and their jsons:
```
cd src/data_loading/
python download_listing_jsons.py
```
3. Parse downloaded listing jsons to get listing description, amenities and house rules in .jsonl file:
```
python parse_listings_info.py
```

## (optional) How to dump listing information with RapidAPI


1. Activate the virtual environment as described above

2. Add `.env` file to the root directory and insert your RapidAPI key there RAPIDAPI_KEY="your key". Should look like `.env_example` file

3. Move to the folder with dumping file and run the file:
```
cd src/data_loading/
python dump_listings_with_rapidapi.py 
```

## To run tests

1. Activate the virtual environment as described above

3. Move to the folder with tests and run pytest:
```
cd src/tests/
pytest -v
```


## Project Organization
```
├── LICENSE
├── README.md          <- The top-level README for developers using this project.
|
├── data               <- Sample data,
├── logs               <- Where logs are stored
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
|   |                     the creator's initials, and a short `-` delimited description, e.g.
|   |                     `1.0_jqp_initial-data-exploration`.
│   ├── exploratory    <- Notebooks for initial exploration.
│   └── reports        <- Polished notebooks for presentations or intermediate results.
│
├── requirements.txt   <- File containing the requirements.
├── .env               <- File containing environment variables (please create it the same way as `.env_example`).
│
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── data_loading   <- Scripts to download and parce data
│   │
│   ├── preprocessing  <- Scripts to turn raw data into clean data and features for modeling
|   |
│   ├── models         <- Scripts to train models and then use trained models to make
│   │                     predictions
│   │
│   └── tests          <- Scripts for unit tests of your functions
│
└── setup.cfg          <- setup configuration file for linting rules
