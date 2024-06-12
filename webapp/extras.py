"""Extra consts and functions for server."""

WELCOME_PAGE = """
<h1>Hello world! This is welcome page, there is nothing interesting to look at</h1>
"""


def body_check(body, fields_list):
    """Body of request checker.

    Args:
        body: request body
        fields_list: fields to check

    Raises:
        FieldNotFoundInRequest: error if field not given in request
    """
    for field in fields_list:
        if field not in body:
            raise FieldNotFoundInRequest(field)


class FieldNotFoundInRequest(Exception):
    """Simple rename for exception for usage when requiered field was not specified in request."""

    pass


DEFAULT_PORT = 5050
