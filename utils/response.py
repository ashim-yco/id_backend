from rest_framework.response import Response


def res(message="", data={}, status=None, errors={}):
    return Response({"mesage": message, "data": data, "errors": errors}, status=status)
