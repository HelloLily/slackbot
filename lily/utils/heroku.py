import requests
from slackbot import settings
from json.decoder import JSONDecodeError


def set_config(data):
    url = 'https://api.heroku.com/apps/hellolily-staging/config-vars'
    headers = {
        'Authorization': 'Bearer {}'.format(settings.HEROKU_API_TOKEN),
        'Accept': 'application/vnd.heroku+json; version=3',
        'Content-Type': 'application/json',
    }

    request = requests.patch(url, json=data, headers=headers)

    try:
        response = request.json()
    except JSONDecodeError:
        response = None

    return response


def set_env():
    def run_command(cmd):
        url = 'https://api.heroku.com/apps/hellolily-staging/ps'
        data = {
            'command': cmd,
        }
        headers = {
            'Authorization': 'Bearer {}'.format(settings.HEROKU_API_TOKEN),
            'Accept': 'application/vnd.heroku+json; version=3',
            'Content-Type': 'application/json',
        }

        request = requests.post(url, json=data, headers=headers)

        try:
            response = request.json()
        except JSONDecodeError:
            response = None

        return response

    commands = [
        'python manage.py flush',
        'python manage.py migrate',
        'python manage.py index -f',
        'python manage.py collectstatic --noinput',
        'python manage.py testdata -b 100',
    ]

    return run_command(' && '.join(commands))


def start_build(branch_name):
    url = 'https://api.heroku.com/apps/hellolily-staging/builds'
    data = {
        'source_blob': {
            'url': 'https://github.com/hellolily/hellolily/archive/{}.tar.gz'.format(branch_name),
        },
    }
    headers = {
        'Authorization': 'Bearer {}'.format(settings.HEROKU_API_TOKEN),
        'Accept': 'application/vnd.heroku+json; version=3',
        'Content-Type': 'application/json',
    }

    request = requests.post(url, json=data, headers=headers)

    try:
        response = request.json()
    except JSONDecodeError:
        response = None

    return response


def wait_for_build(build_id):
    is_building = True
    response = None
    url = 'https://api.heroku.com/apps/hellolily-staging/builds/{}'.format(build_id)
    headers = {
        'Authorization': 'Bearer {}'.format(settings.HEROKU_API_TOKEN),
        'Accept': 'application/vnd.heroku+json; version=3',
        'Content-Type': 'application/json',
    }

    while is_building:
        request = requests.get(url, headers=headers)

        try:
            response = request.json()

            if response.get('status') != 'pending':
                is_building = False

        except JSONDecodeError:
            response = None
            is_building = False

    return response
