from __future__ import print_function

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from github import Github
import string
import requests
from os import environ

ENDPOINT = "webhook"

TOKEN = environ['GITHUB_TOKEN']

@view_defaults(
    route_name=ENDPOINT, renderer="json", request_method="POST"
)
class PayloadView(object):
    """
    View receiving of Github payload. By default, this view it's fired only if
    the request is json and method POST.
    """

    def __init__(self, request):
        self.request = request
        # Payload from Github, it's a dict
        self.payload = self.request.json

    @view_config(header="X-Github-Event:pull_request")
    def payload_pull_request(self):
        """This method is a continuation of PayloadView process, triggered if
        header HTTP-X-Github-Event type is Pull Request"""
        req_title = self.payload['pull_request']['title']
        
        remove_label_name = ""
        add_label_name = "" 
        if "[WIP]" in req_title:
            req_title = req_title.replace("[WIP]", "")
            remove_label_name = "Ready"
            add_label_name = "WIP"
        elif "[READY]" in req_title:
            req_title = req_title.replace("[READY]", "")
            remove_label_name = "WIP"
            add_label_name = "Ready" 
        if remove_label_name:
            print("Response on removing label: ",requests.delete(self.payload['pull_request']['issue_url'] + "/labels/" + remove_label_name, headers={'Authorization': 'token %s' % TOKEN}).text)
            print("Response on adding label: ", requests.post(self.payload['pull_request']['issue_url']+'/labels', json={"labels" : [add_label_name]}, headers={'Authorization': 'token %s' % TOKEN}).text)
            print("Response on changing title: ", requests.patch(self.payload['pull_request']['url'], json={"title" : req_title}, headers={'Authorization': 'token %s' % TOKEN}).text)

        return Response("success")




if __name__ == "__main__":
    config = Configurator()

    config.add_route(ENDPOINT, "/{}".format(ENDPOINT))
    config.scan()

    app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 4431, app)
    server.serve_forever()