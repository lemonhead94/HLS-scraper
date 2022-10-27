import time
from typing import Any, Dict, List, Optional

import pandas as pd
import requests

from hls_dump.logging_utils import log_exception, setup_logging_to_file


def get_hhb_ids(json: List[Dict[str, Any]]) -> Optional[str]:
    hhb_ids: List[int] = []
    for data in json:
        try:
            hhb_ids.append(data["hhb_id"])
        except (KeyError, TypeError):
            pass
    return ",".join([str(i) for i in hhb_ids]) if hhb_ids else None


def get_forename(json: List[Dict[str, Any]]) -> Optional[str]:
    for data in json:
        try:
            return str(data["forename"])
        except (KeyError, TypeError):
            pass
    return None


def get_surname(json: List[Dict[str, Any]]) -> Optional[str]:
    for data in json:
        try:
            return str(data["surname"])
        except (KeyError, TypeError):
            pass
    return None


def get_sex(json: List[Dict[str, Any]]) -> Optional[str]:
    for data in json:
        try:
            if len(data["sex"]) > 0:
                return str(data["sex"][0]["term"]["labels"]["eng"])
        except (KeyError, TypeError):
            pass
    return None


def get_birth_date(json: List[Dict[str, Any]]) -> Optional[str]:
    for data in json:
        try:
            if len(data["existences"]) > 0:
                return str(data["existences"][0]["start"]["date"])
        except (KeyError, TypeError):
            pass
    return None


def get_death_date(json: List[Dict[str, Any]]) -> Optional[str]:
    for data in json:
        try:
            if len(data["existences"]) > 0:
                return str(data["existences"][0]["end"]["date"])
        except (KeyError, TypeError):
            pass
    return None


def get_relation_id(json: List[Dict[str, Any]]) -> Optional[int]:
    for data in json:
        try:
            if len(data["relations"]) > 0:
                return int(data["relations"][0]["person"]["id"])
        except (KeyError, TypeError):
            pass
    return None


def get_relation_name(json: List[Dict[str, Any]]) -> Optional[str]:
    for data in json:
        try:
            if len(data["relations"]) > 0:
                return str(data["relations"][0]["person"]["name"])
        except (KeyError, TypeError):
            pass
    return None


def get_relation_type(json: List[Dict[str, Any]]) -> Optional[str]:
    for data in json:
        try:
            if len(data["relations"]) > 0:
                return str(data["relations"][0]["relation"]["labels"]["eng"])
        except KeyError:
            pass
    return None


def main() -> None:
    setup_logging_to_file("hist-hub.log")
    df = pd.read_csv("hls_dump/22_10_22_hls_people.csv", sep=";")

    url = "https://data.histhub.ch/api/search/"
    headers = {"Content-Type": "application/json"}
    for index, row in df.iterrows():
        print(f"Processing {index + 1} out of {len(df)}")
        data = {"version": 1, "external_ids.external_id": row.HLS_ID}
        response = requests.post(url, json=data, headers=headers)
        json = response.json()

        # backup in case there is a connection error
        if json is None:
            time.sleep(60)
            response = requests.post(url, json=data, headers=headers)

        try:
            df.loc[index, "hhb_ids"] = get_hhb_ids(json)
            df.loc[index, "hhb_forename"] = get_forename(json)
            df.loc[index, "hhb_surname"] = get_surname(json)
            df.loc[index, "hhb_sex"] = get_sex(json)
            df.loc[index, "hhb_birth_date"] = get_birth_date(json)
            df.loc[index, "hhb_death_date"] = get_death_date(json)
            df.loc[index, "hhb_relation_id"] = get_relation_id(json)
            df.loc[index, "hhb_relation_name"] = get_relation_name(json)
            df.loc[index, "hhb_relation_type"] = get_relation_type(json)
        except Exception as e:
            log_exception(e)
            time.sleep(60)
            pass

        time.sleep(1)

    df.to_csv("hls_dump/22_10_22_hls_people_hist_hub_V2.csv", sep=";", index=False)


if __name__ == "__main__":
    main()
