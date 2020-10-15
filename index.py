import logging
import pickle
from time import time
from hashlib import md5
from base64 import urlsafe_b64encode
from os import urandom

import redis
from flask import Flask, request, render_template

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='public')
r = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    password='heslo'
)

TTL = 3600
UA_BLACKLIST = ['Slackbot']

@app.route('/set', methods=['post'])
def set_pass():
    assert request.method == 'POST'
    password = request.form['pass']
    iv = request.form['iv']
    uuid = urlsafe_b64encode(md5(urandom(128)).digest())[:8].decode('utf-8')

    with r.pipeline() as pipe:
        data = {'status': 'ok', 'iv': iv, 'pass': password}
        pipe.set(uuid, pickle.dumps(data))
        pipe.expire(uuid, TTL)
        pipe.execute()

    return '/get/{}'.format(uuid)


def _is_blacklisted(user_agent):
    if 'skip-blacklist' in request.args:  # User is probably human
        return False

    try:
        user_agent = user_agent.lower()
        for keyword in UA_BLACKLIST:
            if keyword in user_agent:
                return True

    except AttributeError:  # Blacklist is not configured
        return False

    return False


@app.route('/get/<uuid>', methods=['get'])
def get_pass(uuid):
    if _is_blacklisted(request.user_agent.string):
        return render_template('blacklisted.html'),  403

    with r.pipeline() as pipe:
        raw_data = r.get(uuid)

        if not raw_data:
            return render_template('expired.html')

        data = pickle.loads(raw_data)
        if data['status'] == 'ok':
            new_data = {'status': 'withdrawn', 'time': int(time()), 'ip': request.remote_addr}
            r.set(uuid, pickle.dumps(new_data))
            return render_template('get.html', data=data['iv'] + '|' + data['pass'])

        if data['status'] == 'withdrawn':
            return render_template('withdrawn.html')


@app.route('/', methods=['get'])
def index():
    ttl = int(TTL/60)
    return render_template('index.html', ttl=ttl)


@app.route('/robots.txt', methods=['get'])
def robots():
    return app.send_static_file('robots.txt')


if __name__ == '__main__':
    port = 5000
    host = '0.0.0.0'

    app.run(host=host, port=port, debug=True)
