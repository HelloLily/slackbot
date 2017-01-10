import os


try:
    curfile = os.path.abspath(os.path.dirname(__file__))
    with open(curfile + '/.env') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0 and not line.startswith('#'):
                index = line.index('=')
                key = line[0:index]
                value = line[index + 1:]
                os.environ[key] = value
except:
    pass


API_TOKEN = os.environ.get('SLACK_API_TOKEN')
HEROKU_API_TOKEN = os.environ.get('HEROKU_API_TOKEN')
ERRORS_TO = os.environ.get('ERRORS_TO')
PLUGINS = [
    'lily.plugins',
]
