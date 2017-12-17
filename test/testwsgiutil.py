from webnode.utils import content_type


def testresponsetype():

    CONTENT_TYPE = "application/json"

    @content_type(CONTENT_TYPE)
    def handler():
        return "handler", "B"

    ret, response_type = handler()

    assert response_type == CONTENT_TYPE
