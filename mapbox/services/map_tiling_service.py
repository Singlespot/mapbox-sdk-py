import json
from typing import Dict

from uritemplate import URITemplate

from mapbox.services.base import Service


class MTS(Service):
    """Access to the Style Map API V1"""

    api_name = 'tilesets'
    api_version = 'v1'

    def create_tileset_source(self, username, source_id, source_file_path):
        """/tilesets/v1/sources/{username}/{source_id}"""
        pth = '/sources/{username}/{source_id}'

        files = {'file': (source_file_path, open(source_file_path, 'rb'))}

        values = dict(username=username, source_id=source_id)

        print(self.baseuri)

        uri = URITemplate(self.baseuri + pth).expand(**values)
        res = self.session.post(uri, files=files)
        self.handle_http_error(res)
        return res

    def create_tileset(self, tileset_id, recipe_file_path):
        """/tilesets/v1/{tileset_id}"""
        pth = '/{tileset_id}'
        headers = {'Content-Type': 'application/json'}
        values = dict(tileset_id=tileset_id)
        with open(recipe_file_path) as json_file:
            data = json.load(json_file)
            print(json.dumps(data))

        uri = URITemplate(self.baseuri + pth).expand(**values)
        res = self.session.post(uri, headers=headers, data=json.dumps(data))
        self.handle_http_error(res)
        return res

    def publish_tileset(self, tileset_id):
        """/tilesets/v1/{tileset_id}/publish"""
        pth = f'/{tileset_id}/publish'
        uri = URITemplate(self.baseuri + pth)
        res = self.session.post(uri)
        self.handle_http_error(res)
        return res
