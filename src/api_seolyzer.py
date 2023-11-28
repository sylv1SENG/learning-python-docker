import json
import os
import urllib.parse
from http import HTTPStatus
from typing import Dict, List, Optional

import requests

SEOLYZER_TOKEN = os.environ["SEOLIZER_TOKEN"]
SEOLIZER_BASE_URL = "https://api.seolyzer.io"
SEOLIZER_ENDPOINT_VERSION = "v1"
SEOLIZER_DATA_ENDPOINT = "data/61b834961b3a1b70c6ba2a9279f2fbf4/log/googlebot-status-code"
SEOLIZER_ENDPOINT_PARAMS = {
    "segmentationId": 1,
    "size": 50,
    "sort": "timestamp",
    "order": "desc",
    "utcOffset": -120,
    "page": "1",
    "start": 1693778400000,  # Timestamp in miliseconds -> 2023-09-03 22:00:00GMT+02:00
    "end": 1696456799999  # Timestamp in miliseconds -> 2023-09-04 23:59:59.999GMT+02:00
}
SEOLIZER_HEADERS = {'Authorization': f'Bearer {SEOLYZER_TOKEN}'}

OUTPUT_FOLDER = os.environ["OUTPUT_FOLDER"]


def extract_seolizer_logs(
    base_url: str = SEOLIZER_BASE_URL,
    endpoint_version: str = SEOLIZER_ENDPOINT_VERSION,
    endpoint: str = SEOLIZER_DATA_ENDPOINT,
    url_params: str = SEOLIZER_ENDPOINT_PARAMS) -> requests.models.Response:

    full_url = os.path.join(base_url,
                            endpoint_version,
                            endpoint,
                            urllib.parse.urlencode(url_params))

    response = requests.request("GET",
                                url=full_url,
                                headers=SEOLIZER_HEADERS,
                                params=
                                data={})
    response.raise_for_status()

    data = response.json()

    return data

def get_seolizer_log_records_headers(data: Dict, custom_fields: Optional[List[str]] = None) -> List[str]:
    headers = list(data["data"][1].keys())
    
    if custom_fields:
        headers.extend(custom_fields)

    headers = ';'.join(headers)+ '\n'

    return headers


def transform_seolizer_log_records(seolizer_log_records: List) -> List[List]:
    transformed_log_records = []

    for log_record in seolizer_log_records:
        # Transform the records into a list
        log_record_values = list(log_record.values())

        # Parse record values to create a new field and add this new value to the record list values
        log_record_http_status = list(log_record.values())[1]
        if log_record_http_status == HTTPStatus.OK: 
            log_record_values.append("Bon_200")
        else:
            log_record_values.append("Pas_200")

        transformed_log_records.append(log_record_values)

    return transformed_log_records


def write_data_to_local_json(data: Dict, output_folder: str = OUTPUT_FOLDER):

    output_path = os.path.join(output_folder, "json_file.json")

    with open(output_path, "w") as json_output_file:
        json_output_file.write(json.dumps(data))


def write_data_to_local_csv(data, headers: Optional[str] = None, output_folder: str = OUTPUT_FOLDER):

    output_path = os.path.join(output_folder, "file3.csv")

    with open(output_path, "w") as csv_output_file:

        # Write headers
        if headers:
            csv_output_file.write(headers)

        # Write rows
        for row in data:
            valeur = ['"' + str(item) + '"' for item in row]
            valeur = ';'.join(valeur)+ '\n'
            csv_output_file.write(valeur)


def run():
    # Extract
    data = extract_seolizer_logs()

    # Transform
    headers = get_seolizer_log_records_headers(data=data, custom_fields=["Verif_statut"])
    transformed_log_records = transform_seolizer_log_records(seolizer_log_records=data["data"])
    # Load
    write_data_to_local_json(data=transformed_log_records)
    write_data_to_local_csv(data=transformed_log_records, headers=headers)

if __name__ == "__main__":
    run()
