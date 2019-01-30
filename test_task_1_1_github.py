import requests

from delayed_assert import expect, assert_expectations

api_base_url = 'https://api.github.com/repos/'
api_repo_url = 'ursusrepublic/django_test'


class TestDataRetrieveGitHub(object):
    def test_pullreq(self):
        """
            Проверка количества открытых и закрытых Pull Requests
        """
        pr_open = 0
        pr_closed = 0

        req_url = api_base_url + api_repo_url + '/pulls?state=all'
        next_page = True

        while next_page:
            # Запрос

            resp = requests.get(req_url)
            assert resp.status_code == 200, \
                "Ответ от API GitHub пришёл не 200 OK ({0}): {1}".format(resp.status_code, resp.content)

            data = resp.json()

            # Обработка данных
            for pr in data:
                if pr['state'] == 'open':
                    pr_open += 1
                elif pr['state'] == 'closed':
                    pr_closed += 1

            # Проверка наличия следующей страницы
            next_page, req_url = self.check_next_page(req_url, resp.headers)

        expect(
            pr_open == 2,
            "Не совпадает количество открытых Pull Request (ожидалось: {0}, результат: {1})".format(2, pr_open)
        )

        expect(
            pr_closed == 1,
            "Не совпадает количество закрытых Pull Request (ожидалось: {0}, результат: {1})".format(1, pr_closed)
        )

        assert_expectations()

    def test_branches_retrieve(self):
        """
            Проверка списка веток репозитория
        """

        req_url = api_base_url + api_repo_url + '/branches'
        next_page = True
        branches_count = 0
        actual_branches = []

        while next_page:
            # Запрос

            resp = requests.get(req_url)
            assert resp.status_code == 200, \
                "Ответ от API GitHub пришёл не 200 OK ({0}): {1}".format(resp.status_code, resp.content)

            data = resp.json()

            # Обработка данных
            branches_count += len(data)
            for br in data:
                actual_branches.append(br['name'])

            # Проверка наличия следующей страницы
            next_page, req_url = self.check_next_page(req_url, resp.headers)

        # Сверки
        assert branches_count == 48, "Не совпадает количество полученных веток! ({0})".format(branches_count)

        f = open("data/test_1_branches_list.txt")
        expected_branches = []
        for line in f:
            expected_branches.append(line.strip())

        for act_br in actual_branches:
            assert act_br in expected_branches, \
                "Ветки '{0}' нет в списке ожидаемых веток!".format(act_br)
            expected_branches.remove(act_br)

        assert len(expected_branches) == 0, \
            "Веток '{0}' нет или они не были получены с сервера".format(expected_branches)

    #
    #
    #         ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    #
    #

    def check_next_page(self, req_url, headers):
        next_page = False

        link_header = headers.get("link")
        if link_header is not None:
            for link in link_header.split(','):
                if 'rel="next"' in link:
                    next_page = True
                    req_url = link.split(';')[0].strip()[1:-1]

        return next_page, req_url
