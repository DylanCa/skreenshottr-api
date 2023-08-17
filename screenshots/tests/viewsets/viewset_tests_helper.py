from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework_simplejwt.tokens import RefreshToken


class ViewsetTestsHelper:
    @staticmethod
    def __get_response_for_method(client, method, path, data, content_type):
        match method.upper():
            case "GET":
                response = client.get(path, content_type=content_type)
            case "POST":
                response = client.post(path, data=data, content_type=content_type)
            case "PUT":
                response = client.put(path, data=data, content_type=content_type)
            case "PATCH":
                response = client.patch(path, data=data, content_type=content_type)
            case "DELETE":
                response = client.delete(path, content_type=content_type)
            case _:
                raise NotImplementedError

        return response

    @staticmethod
    def __assert_not_auth(client, method, path, data, content_type):
        response = ViewsetTestsHelper.__get_response_for_method(
            client, method, path, data, content_type
        )

        expected_error = ErrorDetail(
            string="Authentication Credentials Were Not Provided.",
            code="not_authenticated",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"].title() == expected_error.title()
        assert response.data["detail"].code == expected_error.code

    @staticmethod
    def get_response_for_logged_request(
        client, method, path, user, data=None, content_type=None
    ):
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        return ViewsetTestsHelper.__get_response_for_method(
            client, method, path, data, content_type
        )

    @staticmethod
    def get_response(client, method, path, user, data=None, content_type=None):
        ViewsetTestsHelper.__assert_not_auth(client, method, path, data, content_type)
        return ViewsetTestsHelper.get_response_for_logged_request(
            client, method, path, user, data, content_type
        )
