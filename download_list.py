import requests
import time
import os

from utils import BUILDING_TYPES, QUEUES, get_raw_list_file_path, YEARS, QUEUE_TIME_GROUPS


def _ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def fetch(queue, year, building_type, group):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.post(
        'https://bostad.stockholm.se/statistik/RenderApartmentList/',
        json={
            "rooms": "",
            "area": "",
            "apartmentType": "Alla",
            "buildingType": BUILDING_TYPES[building_type],
            "queue": QUEUES[queue],
            "year": str(year),
            "group": group
        },
        headers=headers,
        stream=True
    )

    # Kasta fel om statuskod inte är 200
    response.raise_for_status()
    file_path = get_raw_list_file_path(queue, year, building_type, group)
    print(f"Sparar fil: {file_path}")
    _ensure_dir(file_path)
    with open(file_path, 'wb+') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


if __name__ == "__main__":
    for queue in QUEUES.keys():
        for year in YEARS:
            for building_type in BUILDING_TYPES.keys():
                for group in QUEUE_TIME_GROUPS:
                    fetch(queue, year, building_type, group)
                    time.sleep(0.2)
