# HLS-scraper

This project is a webscraper for the [Historical Dictionary of Switzerland (HDS)](https://hls-dhs-dss.ch/).

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