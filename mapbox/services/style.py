from typing import Dict

from uritemplate import URITemplate

from mapbox.services.base import Service


class Style(Service):
    """Access to the Style Map API V1"""

    api_name = 'styles'
    api_version = 'v1'

    def create(self, username, style_json: Dict):
        """/styles/v1/{username}"""
        pth = '/{username}/{style_id}'

        values = dict(username=username)

        uri = URITemplate(self.baseuri + pth).expand(**values)
        res = self.session.post(uri, json=style_json)
        self.handle_http_error(res)
        return res

    def retrieve(self, username, style_id, fresh=True):
        """/styles/v1/{username}/{style_id}"""
        pth = '/{username}/{style_id}'

        values = dict(username=username, style_id=style_id)

        uri = URITemplate(self.baseuri + pth).expand(**values)
        res = self.session.get(uri, params=dict(fresh=fresh))
        self.handle_http_error(res)
        return res

    def update(self, username, style_id, style_json: str):
        """/styles/v1/{username}/{style_id}"""
        pth = '/{username}/{style_id}'

        values = dict(username=username, style_id=style_id)

        uri = URITemplate(self.baseuri + pth).expand(**values)
        self.session.headers['Content-Type'] = 'application/json'
        res = self.session.patch(uri, data=style_json)
        self.handle_http_error(res)
        return res
