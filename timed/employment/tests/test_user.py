"""Tests for the users endpoint."""

from django.core.urlresolvers import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN)

from timed.employment.factories import UserFactory
from timed.jsonapi_test_case import JSONAPITestCase


class UserTests(JSONAPITestCase):
    """Tests for the users endpoint.

    This endpoint should be read only.
    """

    def setUp(self):
        """Setup the environment for the tests."""
        super().setUp()

        self.users = UserFactory.create_batch(10)

    def test_user_list(self):
        """Should respond with a list of users."""
        url = reverse('user-list')

        noauth_res = self.noauth_client.get(url)
        user_res   = self.client.get(url)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_200_OK

        result = self.result(user_res)

        # 3 is the count of users which are created in the setup hook
        assert len(result['data']) + len(self.users) + 3

    def test_user_detail(self):
        """Should respond with a single user."""
        user = self.users[0]

        url = reverse('user-detail', args=[
            user.id
        ])

        noauth_res = self.noauth_client.get(url)
        user_res   = self.client.get(url)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_200_OK

    def test_user_create(self):
        """Should not be able to create a user."""
        data = {}
        url  = reverse('user-list')

        noauth_res        = self.noauth_client.post(url, data)
        user_res          = self.client.post(url, data)
        project_admin_res = self.project_admin_client.post(url, data)
        system_admin_res  = self.system_admin_client.post(url, data)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_403_FORBIDDEN
        assert project_admin_res.status_code == HTTP_403_FORBIDDEN
        assert system_admin_res.status_code == HTTP_403_FORBIDDEN

    def test_user_update(self):
        """Should not be able to update a user."""
        user = self.users[1]
        data = {}

        url = reverse('user-detail', args=[
            user.id
        ])

        noauth_res        = self.noauth_client.patch(url, data)
        user_res          = self.client.patch(url, data)
        project_admin_res = self.project_admin_client.patch(url, data)
        system_admin_res  = self.system_admin_client.patch(url, data)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_403_FORBIDDEN
        assert project_admin_res.status_code == HTTP_403_FORBIDDEN
        assert system_admin_res.status_code == HTTP_403_FORBIDDEN

    def test_user_delete(self):
        """Should not be able to delete a user."""
        user = self.users[1]
        data = {}

        url = reverse('user-detail', args=[
            user.id
        ])

        noauth_res        = self.noauth_client.delete(url, data)
        user_res          = self.client.delete(url, data)
        project_admin_res = self.project_admin_client.delete(url, data)
        system_admin_res  = self.system_admin_client.delete(url, data)

        assert noauth_res.status_code == HTTP_401_UNAUTHORIZED
        assert user_res.status_code == HTTP_403_FORBIDDEN
        assert project_admin_res.status_code == HTTP_403_FORBIDDEN
        assert system_admin_res.status_code == HTTP_403_FORBIDDEN