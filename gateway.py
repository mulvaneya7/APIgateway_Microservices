#
# Simple API gateway in Python
#
# Inspired by <https://github.com/vishnuvardhan-kumar/loadbalancer.py>
#
#   $ python3 -m pip install Flask python-dotenv
#

import sys

import flask
import requests, itertools, logging
from flask_basicauth import BasicAuth

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')

#Overriding of the check credentials function
#We make an authorize request to the users service
class BasicAuthOverride(BasicAuth):
    def check_credentials(self, username, password):
        r = requests.get('http://localhost:5100/api/v1/users/authuser', auth=(username, password))
        #app.logger.info(f'request: {r.json()}')
        return r.json()['authorized']

#basic authorization
basic_auth = BasicAuthOverride(app)
#app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_REALM'] = 'Authorize'

#obtaining Port list converting into an iterable list
usersPort = app.config['USERS']
timelinesPort = app.config['TIMELINES']
userNodes = itertools.cycle(usersPort)
timelineNodes = itertools.cycle(timelinesPort)



@app.errorhandler(404)
@basic_auth.required
def route_page(err):

    try:
        url = flask.request.path
        if 'users' in url:
            curr_node = next(userNodes)
            reqPath = curr_node + flask.request.full_path
        elif 'timelines' in url:
            curr_node = next(timelineNodes)
            reqPath = curr_node + flask.request.full_path
        else:
            reqPath = ''
        
        response = requests.request(
            flask.request.method,
            reqPath,
            data=flask.request.get_data(),
            headers=flask.request.headers,
            cookies=flask.request.cookies,
            stream=True,
        )
    except requests.exceptions.RequestException as e:
        app.log_exception(sys.exc_info())
        return flask.json.jsonify({
            'method': e.request.method,
            'url': e.request.url,
            'exception': type(e).__name__,
        }), 503

    headers = remove_item(
        response.headers,
        'Transfer-Encoding',
        'chunked'
    )

    return flask.Response(
        response=response.content,
        status=response.status_code,
        headers=headers,
        direct_passthrough=True,
    )


def remove_item(d, k, v):
    if k in d:
        if d[k].casefold() == v.casefold():
            del d[k]
    return dict(d)
