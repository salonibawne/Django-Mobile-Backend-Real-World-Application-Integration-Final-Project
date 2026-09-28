from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        return response

    error_code = "API_ERROR"

    if response.status_code == 400:
        error_code = "VALIDATION_ERROR"

    elif response.status_code == 401:
        error_code = "AUTHENTICATION_REQUIRED"

    elif response.status_code == 403:
        error_code = "PERMISSION_DENIED"

    elif response.status_code == 404:
        error_code = "NOT_FOUND"

    elif response.status_code == 405:
        error_code = "METHOD_NOT_ALLOWED"

    elif response.status_code >= 500:
        error_code = "SERVER_ERROR"

    return Response(
        {
            "success": False,
            "message": "Request failed.",
            "error_code": error_code,
            "data": response.data,
        },
        status=response.status_code,
        headers=response.headers,
    )