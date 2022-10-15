import os
from typing import List

import requests
import structlog
from requests import Response

from ..decorator.logit import logit

SYSTEM_PREFIX = "api-v1/"
BODY_PREFIX = "api-system-v1/"

SYSTEM_ENTITY = "system"
BODY_ENTITY = "bodies"


class EdsmClient:
    _base_url: str
    _api_key: str
    _commander_name: str

    def __init__(self, api_key: str, commander_name: str):
        self._api_key = api_key
        self._commander_name = commander_name
        self._base_url = os.getenv("EDSM_BASE_URL", default="https://www.edsm.net/")
        self._log = structlog.get_logger()

    def __get_url(self, prefix: str, entity: str) -> str:
        return f'{self._base_url}{prefix}{entity}'

    def __get_generic_by_entity(self, entity: str) -> dict:
        if entity == SYSTEM_ENTITY:
            return {
                'showCoordinates': 1,
                'showPermit': 1,
                'showPrimaryStar': 1,
                'showInformation': 1,
                'includeHidden': 1,
                'showId': 1,
            }
        else:
            return {}

    @logit
    def get_system_from_system_id(self, system_id: int) -> dict:
        params = self.__get_generic_by_entity(SYSTEM_ENTITY)
        params.update({'systemId': system_id})
        url = self.__get_url(SYSTEM_PREFIX, SYSTEM_ENTITY)
        response: Response = requests.get(url, params)

        if response.status_code != 200:
            raise requests.HTTPError(f'Unable to retrieve {SYSTEM_ENTITY} : {response.text}')
        else:
            return response.json()

    @logit
    def get_system_from_system_name(self, system_name: str) -> dict:
        params = self.__get_generic_by_entity(SYSTEM_ENTITY)
        params.update({'systemName': system_name})
        url = self.__get_url(SYSTEM_PREFIX, SYSTEM_ENTITY)
        response: Response = requests.get(url, params)

        if response.status_code != 200:
            raise requests.HTTPError(f'Unable to retrieve {SYSTEM_ENTITY} : {response.text}')
        else:
            return response.json()

    @logit
    def get_bodies_from_system_id(self, system_id: int) -> List[dict]:
        params = self.__get_generic_by_entity(BODY_ENTITY)
        params.update({'systemId': system_id})
        url = self.__get_url(BODY_PREFIX, BODY_ENTITY)
        response: Response = requests.get(url, params)

        if response.status_code != 200:
            raise requests.HTTPError(f"Unable to retrieve {BODY_ENTITY} : {response.text}")
        else:
            if 'bodies' in response.json():
                return response.json()['bodies']
            else:
                return []

    @logit
    def get_body_from_system_name(self, system_name: str) -> List[dict]:
        params = self.__get_generic_by_entity(BODY_ENTITY)
        params.update({'systemName': system_name})
        url = self.__get_url(BODY_PREFIX, BODY_ENTITY)
        response: Response = requests.get(url, params)

        if response.status_code != 200:
            raise requests.HTTPError(f"Unable to retrieve {BODY_ENTITY} : {response.text}")
        else:
            if 'bodies' in response.json():
                return response.json()['bodies']
            else:
                return []