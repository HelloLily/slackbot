import requests


def is_valid_branch(branch_name):
    url = 'https://api.github.com/repos/hellolily/hellolily/branches'
    request = requests.get(url)

    branch_list = [branch.get('name') for branch in request.json()]

    if branch_name in branch_list:
        return True

    return False


def get_latest_commit_data(branch_name):
    url = 'https://api.github.com/repos/hellolily/hellolily/commits/{}'.format(branch_name)
    request = requests.get(url)

    return request.json()
