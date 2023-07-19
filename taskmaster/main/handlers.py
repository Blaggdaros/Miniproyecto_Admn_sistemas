from rest_framework import status
from rest_framework.exceptions import UnsupportedMediaType, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        response_data = {
            "status": {
                "type": "error",
                "code": status.HTTP_409_CONFLICT,
                "message": "A task with the same name and due date already exists",
            }
        }
        return Response(response_data, status=status.HTTP_409_CONFLICT)

    if isinstance(exc, UnsupportedMediaType):
        response_data = {
            "status": {
                "type": "error",
                "code": exc.status_code,
                "message": "Malformed body: only valid JSON is accepted",
            }
        }
        return Response(response_data, status=exc.status_code)

    # Llamar al manejador de excepciones predeterminado para el resto de las excepciones
    return exception_handler(exc, context)
