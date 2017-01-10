import requests
from slackbot import settings


def get_name(user_id):
    url = 'https://slack.com/api/users.info'
    data = {
        'token': settings.API_TOKEN,
        'user': user_id,
    }

    request = requests.post(url, data=data)
    response = request.json()

    return response['user'].get('real_name', 'user id: {}'.format(user_id))
