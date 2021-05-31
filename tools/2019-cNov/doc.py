from urllib.parse import urlencode
from json import dumps
from requests import get


ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"
AREA_TYPE = "nation"
AREA_NAME = "england"

filters = [
    f"areaType={ AREA_TYPE }",
    f"areaName={ AREA_NAME }"
]

structure = {
    "date": "date",
    "name": "areaName",
    "code": "areaCode",
    "cases": {
        "daily": "newCasesByPublishDate",
        "cumulative": "cumCasesByPublishDate"
    },
    "deaths": {
        "daily": "newDeathsByDeathDate",
        "cumulative": "cumDeathsByDeathDate"
    }
}

api_params = {
    "filters": str.join(";", filters),
    "structure": dumps(structure, separators=(",", ":")),
    "latestBy": "newCasesByPublishDate"
}

encoded_params = urlencode(api_params)

response = get(f"{ ENDPOINT }?{ encoded_params }", timeout=10)

if response.status_code >= 400:
    raise RuntimeError(f'Request failed: { response.text }')

data = response.json()

print(data)
