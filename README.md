# HLS-scraper

This project is a webscraper for the [Historical Dictionary of Switzerland (HDS)](https://hls-dhs-dss.ch/).

## Installation

````bash
pip install hlsscraper
````

## Usage

Please use the already scraped [hls_base.csv](https://github.com/lemonhead94/HLS-scraper/blob/main/data/hls_base.csv) from 12.12.2022 as basis so only updates and new records need to be fetched.
This will help not to stress HLS servers to much.

````python
import hlsscraper

hlsscraper.scrape(
    base_csv_path=f"{os.getcwd()}/data/hls_base.csv",
    update_csv_path=f"{os.getcwd()}/data/hls_updates.csv",
    new_csv_path=f"{os.getcwd()}/data/hls_new.csv",
    last_scraping="12.12.2022",
    crawl_delay=20,  # as per https://hls-dhs-dss.ch/robots.txt
)
````

## Development

```bash
# download a fresh python 3.9
conda create -n py39 python=3.9
# create a .venv inside the project and link against the Python 3.9 version installed through conda
poetry env use ~/.conda/envs/py39/bin/python
# install required packages defined in pyproject.toml into .venv
poetry install
# set up git hooks for autoformatting and linting (black, isort8, flake8) --> .pre-commit-config.yaml
pre-commit install
```