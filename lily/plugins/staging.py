import json
import re

from slackbot.bot import respond_to
from lily.utils import github, slack, heroku


@respond_to('deploy$', re.IGNORECASE)
@respond_to('deploy (.*)$', re.IGNORECASE)
def deploy(message, branch_name='master'):
    message.reply('Deploying {} branch to staging.'.format(branch_name))

    if branch_name is not 'master' and not github.is_valid_branch(branch_name):
        message.reply('The branch `{}` is not known to me, have you made a typo?'.format(branch_name))
        return None

    build_info = heroku.start_build(branch_name)
    message.reply('<{}|Build started> - sit back and relax!'.format(build_info.get('output_stream_url')))

    message.send_webapi(
        'Ok, I\'ve started a build for you!',
        json.dumps([{
            'fallback': 'Build started - {}'.format(build_info.get('output_stream_url')),
            'text': 'Sit back and relax! Or go and <{}|check on the progress>.'.format(build_info.get('output_stream_url')),
            'color': 'good',
        }])
    )

    heroku.wait_for_build(build_info.get('id'))
    user = slack.get_name(message.body.get('user'))

    heroku.set_config({
        'DEPLOYER_NAME': user,
    })
    heroku.set_env()
    message.reply('The deploy has finished.')


@respond_to('status$', re.IGNORECASE)
def status(message):
    # See: https://api.slack.com/docs/message-attachments
    attachments = [
        {
            'fallback': 'Fallback text',
            'author_name': 'Author',
            'author_link': 'http://www.github.com',
            'text': 'Some text',
            'color': 'good'
        }
    ]
    message.send_webapi(
        'Heroku staging currently has the following status:',
        json.dumps(attachments)
    )
