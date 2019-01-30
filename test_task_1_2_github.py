import json

import requests

from delayed_assert import expect, assert_expectations
from generators import generate_string

api_base_url = 'https://api.github.com/repos/'
api_repo_url = 'ursusrepublic/django_test'


class TestDataPostGitHub(object):
    def test_create_issue(self):
        """
            Проверка создания задачи
        """

        # Чтение токена доступа

        f = open("data/github.token")
        oauth_access_token = f.readline().strip()

        # Проверка создания задачи

        req_url = api_base_url + api_repo_url + '/issues'

        headers = {
            "Content-Type": "application/json",
            "Authorization": "token %s" % oauth_access_token
        }

        issue_title = generate_string(8)
        issue_body = generate_string(32)

        payload = json.dumps({
            "title": issue_title,
            "body": issue_body,
        })

        resp = requests.post(
            req_url,
            headers=headers,
            data=payload
        )

        assert resp.status_code == 201, "Не получилось создать задачу (%i)" % resp.status_code

        # Проверка того, что задача создана

        data = resp.json()
        req_url = api_base_url + api_repo_url + '/issues/%s' % data['number']

        resp = requests.get(req_url)

        assert resp.status_code == 200, "Не получилось найти только что созданную задачу (%i)" % resp.status_code

        data = resp.json()

        expect(
            data['title'] == issue_title,
            "Не совпал заголовок задачи (ожидание: {0}, получено: {1})".format(issue_title, data['title'])
        )

        expect(
            data['body'] == issue_body,
            "Не совпал текст задачи (ожидание: {0}, получено: {1})".format(issue_body, data['body'])
        )

        assert_expectations()
